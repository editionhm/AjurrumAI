import streamlit as st
import os
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

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# Sidebar with Logout Button and Pages
# -------------------------------
def sidebar_with_logout():
    with st.sidebar:
        # Mode selection before the system message
        st.header("Mode / الوضع")
        mode_options = [
            "Continue the course / متابعة الدرس",
            "Review a lesson / مراجعة درس",
            "Free discussion / مناقشة حرة",
            "Exam / امتحان"
        ]
        selected_mode = st.selectbox("Which mode would you like? / أي وضع تود استخدامه", mode_options)

        # Dynamically load pages from the "Pages" folder
        st.header("Pages / الصفحات")
        pages_folder = "Pages"
        if os.path.exists(pages_folder):
            page_files = [f for f in os.listdir(pages_folder) if f.endswith('.py')]
            page_names = [os.path.splitext(f)[0] for f in page_files]  # Remove the .py extension
            st.selectbox("Select a page / اختر صفحة", page_names)

        # Log Out button at the bottom of the sidebar
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        if st.session_state.user["connected"]:
            if st.button("Log Out / تسجيل الخروج", key="logout_button"):
                st.session_state.user = {
                    "connected": False,
                    "username": None,
                    "age": None
                }
                st.success("You have been logged out. / تم تسجيل خروجك.")

# -------------------------------
# Top Navigation Bar without Greeting
# -------------------------------
def top_navbar():
    st.markdown("<h1 style='text-align: left; color: #2e7bcf;'>📚 AjurrumAI | Teaching Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("### Chat with the greatest Arabic grammar expert! \n تحدث مع أكبر متخصص في قواعد اللغة العربية!")

# Call the top navigation bar
top_navbar()

# Call the sidebar with the log out button
sidebar_with_logout()

# -------------------------------
# Scrollable Chatbox
# -------------------------------
def scrollable_chatbox():
    st.markdown("<h3>Chat History / سجل المحادثة</h3>", unsafe_allow_html=True)
    
    chat_box_style = """
    <style>
    .chat-box {
        height: 300px;
        overflow-y: scroll;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """
    
    st.markdown(chat_box_style, unsafe_allow_html=True)
    
    chat_content = ""
    for entry in st.session_state.chat_history:
        user_message, bot_response = entry["user_message"], entry["bot_response"]
        chat_content += f"<b>User:</b> {user_message}<br><b>Bot:</b> {bot_response}<hr>"
    
    st.markdown(f"<div class='chat-box'>{chat_content}</div>", unsafe_allow_html=True)

# -------------------------------
# Main Content Area - Chat Interaction
# -------------------------------
if st.session_state.user["connected"]:
    st.markdown("---")
    
    # Display the scrollable chatbox
    scrollable_chatbox()

    # Create a chat-style text input with a modern design
    st.markdown("""
    <style>
        .chat-input {
            border: 2px solid #2e7bcf;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    user_input = st.text_area(
        "Write your message here: / اكتب رسالتك هنا", 
        placeholder="Type your message like in a chat... / اكتب رسالتك هنا مثل الدردشة...",
        height=100, 
        key="chat_input", 
        label_visibility="collapsed",
        help="Chat with the AI in real-time"
    )

    # Submit button for the chat message
    if st.button("Submit / إرسال", key="submit_button"):
        if user_input.strip() == "":
            st.error("Please enter something. / الرجاء إدخال شيء.")
        else:
            # Get the selected mode
            interaction_mode = st.sidebar.selectbox("Which mode would you like? / أي وضع تود استخدامه", mode_options)

            # Adapt the prompt based on the selected mode and user's age
            prompt = f"Mode: {interaction_mode}. I am a {st.session_state.user['age']} year old user. Here is my question: {user_input}"

            # Get the model response using the interact module
            try:
                response = interact.get_model_response(prompt)
                if response:
                    st.session_state.chat_history.append({"user_message": user_input, "bot_response": response})
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
