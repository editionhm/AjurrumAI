import streamlit as st
import requests
from pymongo import MongoClient

import database  # Ensure this module handles MongoDB interactions
import interact   # Ensure this module handles LLM interactions

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="📚 AjurrumAI", layout="wide")

# -------------------------------
# Initialize Session State
# -------------------------------
if 'user' not in st.session_state:
    st.session_state.user = {
        "connected": False,
        "username": None,
        "age": None
    }

# -------------------------------
# Top Navigation Bar
# -------------------------------
def top_navbar():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1 style='text-align: left; color: #2e7bcf;'>📚 AjurrumAI | Interactive Teaching Chatbot</h1>", unsafe_allow_html=True)
        st.markdown("### Chat with the greatest Arabic grammar expert! / تحدث مع أكبر متخصص في قواعد اللغة العربية!")
    with col2:
        if st.session_state.user["connected"]:
            with st.expander(f"👤 {st.session_state.user['username']}"):
                if st.button("Logout / تسجيل الخروج"):
                    st.session_state.user = {
                        "connected": False,
                        "username": None,
                        "age": None
                    }
                    st.success("You have been logged out. / تم تسجيل خروجك.")
        else:
            menu = st.selectbox('Menu / القائمة', ['Login / تسجيل الدخول', 'Sign Up / تسجيل حساب'], key='menu_selection')
            if menu == 'Sign Up / تسجيل حساب':
                with st.expander("Create an Account / إنشاء حساب", expanded=True):
                    signup_username = st.text_input('Username / اسم المستخدم', key='signup_username')
                    signup_password = st.text_input('Password / كلمة المرور', type='password', key='signup_password')
                    signup_age = st.slider("Choose your age / اختر عمرك", 0, 100, 20, key='signup_age')
                    if st.button('Sign Up / تسجيل', key='signup_button'):
                        if signup_username and signup_password:
                            message = database.register(signup_username, signup_password, signup_age)
                            if message == "USERNAME_TAKEN":
                                st.error("You can't use this username - لا يمكنك استخدام هذا الإسم")
                            else:
                                st.success("Account created successfully! / تم إنشاء الحساب بنجاح!")
                                login_message = database.login(signup_username, signup_password)
                                if login_message == "LOGIN_SUCCESS":
                                    st.session_state.user["connected"] = True
                                    st.session_state.user["username"] = signup_username
                                    st.session_state.user["age"] = signup_age
                        else:
                            st.error("Please fill in all fields / الرجاء ملء جميع الحقول.")
            elif menu == 'Login / تسجيل الدخول':
                with st.expander("Login / تسجيل الدخول", expanded=True):
                    login_username = st.text_input('Username / اسم المستخدم', key='login_username')
                    login_password = st.text_input('Password / كلمة المرور', type='password', key='login_password')
                    if st.button('Login / تسجيل الدخول', key='login_button'):
                        if login_username and login_password:
                            message = database.login(login_username, login_password)
                            if message == "INCORRECT_CREDENTIALS":
                                st.error("Incorrect username or password - خطا في الاسم او كلمة المرور")
                            else:
                                st.success("Logged in successfully! / تم تسجيل الدخول بنجاح!")
                                st.session_state.user["connected"] = True
                                st.session_state.user["username"] = login_username
                                user = database.get_user_by_username(login_username)
                                if user:
                                    st.session_state.user["age"] = user.get("age", 0)
                        else:
                            st.error("Please enter both username and password / الرجاء إدخال الاسم وكلمة المرور.")

# Call the top navigation bar
top_navbar()

# -------------------------------
# Sidebar for Mode Selection
# -------------------------------
if st.session_state.user["connected"]:
    with st.sidebar:
        st.header("Mode / الوضع")
        mode_options = [
            "Continue the course / متابعة الدرس",
            "Review a lesson / مراجعة درس",
            "Free discussion / مناقشة حرة",
            "Exam / امتحان"
        ]
        selected_mode = st.radio("Which mode would you like? / أي وضع تود استخدامه", mode_options)
else:
    with st.sidebar:
        st.info("Please log in to access the modes. / الرجاء تسجيل الدخول للوصول إلى الأوضاع.")

# -------------------------------
# Main Content Area
# -------------------------------
if st.session_state.user["connected"]:
    st.markdown("---")
    st.header(f"Hello, {st.session_state.user['username']}! / مرحبًا، {st.session_state.user['username']}!")
    
    # Input text from user
    user_input = st.text_area("Ask your question or say what's on your mind: / اطرح سؤالك أو قل ما يدور في ذهنك:")
    
    # Button to send the request
    if st.button("Submit / إرسال"):
        if user_input.strip() == "":
            st.error("Please enter something. / الرجاء إدخال شيء.")
        else:
            # Determine interaction mode
            interaction_mode = selected_mode.split(" / ")[0]  # Extract English part
            
            # Adapt prompt based on interaction mode and age
            prompt = ""
            if interaction_mode == "Continue the course":
                prompt = f"I am a {st.session_state.user['age']} year old student who wants to continue the course. Here is my question: {user_input}"
            elif interaction_mode == "Review a lesson":
                prompt = f"I am reviewing a lesson. Here is my question: {user_input}"
            elif interaction_mode == "Free discussion":
                prompt = f"I would like to have a free discussion. Here is my topic: {user_input}"
            elif interaction_mode == "Exam":
                prompt = f"I am taking an exam. Here is my question: {user_input}"
            else:
                prompt = user_input  # Fallback to user input
            
            # Get the model response using interact.py
            try:
                response = interact.get_model_response(prompt)
                if response:
                    st.success("Response / الرد:")
                    st.write(response)
                else:
                    st.warning("No response received / لم يتم استلام رد")
            except Exception as e:
                st.error(f"An error occurred: {str(e)} / حدث خطأ: {str(e)}")
else:
    st.markdown("---")
    st.info("Please log in or sign up to start interacting with the chatbot. / الرجاء تسجيل الدخول أو إنشاء حساب لبدء التفاعل مع الروبوت.")

# -------------------------------
# Database and Interaction Modules
# -------------------------------
# Note: Ensure that the `database` and `interact` modules are properly implemented.
# The `database` module should handle user registration, login, and retrieval.
# The `interact` module should handle interactions with the LLM/API.
