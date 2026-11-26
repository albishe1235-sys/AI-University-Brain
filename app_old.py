<<<<<< HEAD

import streamlit as st

st.set_page_config(
    page_title="AI University Brain",
    page_icon="🎓"
)

st.title("AI University Brain")

st.write("مرحباً بك في منصة المعرفة الذكية للجامعة!")

st.info("النظام قيد التطوير")
=======
import streamlit as st
import sys
import os

sys.path.insert(0, "/content/AI_University_Brain/src")

from user_manager import create_session, get_session_user
from lecture_storage import load_lectures
from question_access import ask_question_for_user
from lecture_access import upload_lecture_for_user

BASE_DIR = "/content/AI_University_Brain"
USERS_DB = os.path.join(BASE_DIR, "data/users.json")
LECTURES_DB = os.path.join(BASE_DIR, "data/lecture_database.json")

st.set_page_config(
    page_title="AI University Brain",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI University Brain")
st.caption("منصة المعرفة الذكية للجامعة")

if "token" not in st.session_state:
    st.session_state.token = None

# تسجيل الدخول
if not st.session_state.token:

    st.subheader("تسجيل الدخول")

    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        token = create_session(email, password, USERS_DB)

        if token:
            st.session_state.token = token
            st.rerun()
        else:
            st.error("البريد الإلكتروني أو كلمة المرور غير صحيحة")

else:
    token = st.session_state.token
    user = get_session_user(token, USERS_DB)

    if user is None:
        st.session_state.token = None
        st.rerun()

    st.success(f"مرحباً {user['username']}")
    st.write(f"نوع الحساب: {user['role']}")

    if st.button("تسجيل الخروج"):
        from user_manager import ACTIVE_SESSIONS
        ACTIVE_SESSIONS.pop(token, None)
        st.session_state.token = None
        st.rerun()

    st.divider()

    # واجهة السؤال والبحث
    st.subheader("🔎 اسأل عن المحاضرات")

    question = st.text_input("اكتب سؤالك")

    if st.button("بحث"):
        if question.strip():
            try:
                lectures = load_lectures(LECTURES_DB)

                answer = ask_question_for_user(
                    token,
                    question,
                    lectures
                )

                if isinstance(answer, dict):
                    st.write("### الإجابة")
                    st.write(answer["answer"])

                    st.info(
                        f"المادة: {answer['subject']} | "
                        f"الدكتور: {answer['doctor']}"
                    )

                    st.caption(
                        f"المصدر: {answer['source']} | "
                        f"الصفحة: {answer['page_number']}"
                    )
                else:
                    st.warning(answer)

            except Exception as e:
                st.error(str(e))

    # واجهة رفع المحاضرات
    if user["role"] in ["doctor", "admin"]:

        st.divider()
        st.subheader("📤 رفع محاضرة")

        uploaded_file = st.file_uploader(
            "اختر ملف المحاضرة",
            type=["pdf", "docx", "pptx", "xlsx", "txt"]
        )

        university = st.text_input(
            "الجامعة",
            value="University of the Future"
        )

        department = st.text_input("القسم")
        stage = st.text_input("المرحلة")
        subject = st.text_input("المادة")

        doctor = user["username"]

        if st.button("رفع وحفظ المحاضرة"):

            if uploaded_file and department and stage and subject:

                import tempfile

                try:
                    with tempfile.TemporaryDirectory() as temp_dir:

                        file_path = os.path.join(
                            temp_dir,
                            uploaded_file.name
                        )

                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        metadata = {
                            "university": university,
                            "department": department,
                            "stage": stage,
                            "subject": subject,
                            "doctor": doctor,
                            "file_name": uploaded_file.name
                        }

                        result = upload_lecture_for_user(
                            token,
                            file_path,
                            metadata,
                            USERS_DB,
                            LECTURES_DB
                        )

                        st.success("تم رفع المحاضرة بنجاح")
                        st.json(result)

                except Exception as e:
                    st.error(str(e))

            else:
                st.warning("يرجى اختيار الملف وإكمال المعلومات")
>>>>>>> af8ca75 (Add Streamlit application and lecture upload access)
