import os
import sys
from getpass import getpass

# تحديد مسار المشروع
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

sys.path.insert(0, SRC_DIR)

# استيراد دالة إنشاء المستخدم
from user_manager import _save_user

# تحديد مسار قاعدة بيانات المستخدمين
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

USERS_DB = os.path.join(DATA_DIR, "users.json")

print("=== إنشاء حساب المدير ===")

username = input("اسم المدير: ").strip()
email = input("البريد الإلكتروني: ").strip()
password = getpass("كلمة المرور: ")
confirm_password = getpass("تأكيد كلمة المرور: ")

if not username or not email or not password:
    print("يرجى ملء جميع الحقول")
elif password != confirm_password:
    print("كلمتا المرور غير متطابقتين")
else:
    admin = {
        "username": username,
        "email": email,
        "password": password,
        "role": "admin",
        "is_super_admin": True
    }

    try:
        result = _save_user(admin, USERS_DB)
        print(result)
        print("تم إنشاء حساب المدير بنجاح")
    except ValueError as e:
        print("تعذر إنشاء الحساب:", e)
