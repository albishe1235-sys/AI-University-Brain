
import json
import os
import hashlib
import secrets
import hmac

ROLES = {
    "student": ["ask_question", "search_lectures"],
    "doctor": [
        "ask_question",
        "search_lectures",
        "upload_lecture",
        "view_own_lectures"
    ],
    "admin": [
        "ask_question",
        "search_lectures",
        "upload_lecture",
        "manage_users",
        "manage_lectures",
        "upload_official_info"
    ]
}


def get_permissions(role):
    return ROLES.get(role, [])


def has_permission(role, action):
    return action in get_permissions(role)


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        200000
    )

    return salt, hashed.hex()


def register_user(user, database_path):
    if user["role"] != "student":
        raise ValueError("Only student registration is allowed.")

    return _save_user(user, database_path)


def create_managed_user(token, user, database_path):

    actor = authorize_session(
        token,
        database_path,
        "manage_users"
    )

    if user["role"] not in ["doctor", "admin"]:
        raise ValueError("Invalid managed role.")

    if user["role"] == "admin" and not actor.get("is_super_admin", False):
        raise PermissionError(
            "Only the main admin can create another admin."
        )

    return _save_user(user, database_path)


def _save_user(user, database_path):
    users = []

    if os.path.exists(database_path):
        with open(database_path, "r", encoding="utf-8") as file:
            users = json.load(file)

    if any(u["email"] == user["email"] for u in users):
        raise ValueError("Email already registered")

    salt, password_hash = hash_password(user["password"])

    new_user = {
        key: value
        for key, value in user.items()
        if key != "password"
    }

    new_user["salt"] = salt
    new_user["password_hash"] = password_hash

    users.append(new_user)

    with open(database_path, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

    return "User registered successfully"


def login_user(email, password, database_path):
    if not os.path.exists(database_path):
        return None

    with open(database_path, "r", encoding="utf-8") as file:
        users = json.load(file)

    for user in users:
        if user["email"] == email:
            salt = user.get("salt")
            saved_hash = user.get("password_hash")

            if not salt or not saved_hash:
                return None

            _, entered_hash = hash_password(password, salt)

            if hmac.compare_digest(saved_hash, entered_hash):
                return user

    return None


def delete_user(token, target_email, database_path):

    actor = authorize_session(
        token,
        database_path,
        "manage_users"
    )

    if not actor.get("is_super_admin", False):
        raise PermissionError(
            "Only the main admin can delete users."
        )

    with open(database_path, "r", encoding="utf-8") as file:
        users = json.load(file)

    target = next(
        (u for u in users if u["email"] == target_email),
        None
    )

    if not target:
        raise ValueError("User not found.")

    if target.get("is_super_admin", False):
        raise PermissionError(
            "The main admin account cannot be deleted."
        )

    users.remove(target)

    with open(database_path, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

    return "User deleted successfully"


def change_user_role(
    token,
    target_email,
    new_role,
    database_path
):

    actor = authorize_session(
        token,
        database_path,
        "manage_users"
    )

    if not actor.get("is_super_admin", False):
        raise PermissionError(
            "Only the main admin can change user roles."
        )

    if new_role not in ROLES:
        raise ValueError("Invalid role.")

    with open(database_path, "r", encoding="utf-8") as file:
        users = json.load(file)

    target = next(
        (u for u in users if u["email"] == target_email),
        None
    )

    if not target:
        raise ValueError("User not found.")

    if target.get("is_super_admin", False):
        raise PermissionError(
            "The main admin role cannot be changed."
        )

    target["role"] = new_role

    with open(database_path, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

    return "User role updated successfully"

# Active login sessions
ACTIVE_SESSIONS = {}


def create_session(email, password, database_path):

    user = login_user(email, password, database_path)

    if user is None:
        return None

    token = secrets.token_urlsafe(32)

    ACTIVE_SESSIONS[token] = user["email"]

    return token


def get_session_user(token, database_path):

    email = ACTIVE_SESSIONS.get(token)

    if email is None:
        return None

    with open(database_path, "r", encoding="utf-8") as file:
        users = json.load(file)

    for user in users:
        if user["email"] == email:
            return user

    ACTIVE_SESSIONS.pop(token, None)
    return None


def authorize_session(token, database_path, permission):

    user = get_session_user(token, database_path)

    if user is None:
        raise PermissionError("Invalid or expired session.")

    if not has_permission(user["role"], permission):
        raise PermissionError("You do not have this permission.")

    return user
