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

# -------------------------------
# Top Navigation Bar with Greeting and Logout
# -------------------------------
def top_navbar():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Show the greeting message above the main title
        if st.session_state.user["connected"]:
            st.markdown(f"<h2>Hello, {st.session_state.user['username']}! / مرحبًا، {st.session_state.user['username']}!</h2>", unsafe_allow_html=True)

        # Application title and description
        st.markdown("<h1 style='text-align: left; color: #2e7bcf;'>📚 AjurrumAI | Teaching Chatbot</h1>", unsafe_allow_html=True)
        st.markdown("### Chat with the greatest Arabic grammar expert! \n تحدث مع أكبر متخصص في قواعد اللغة العربية!")

    # Right side: Only show a "Log Out" button when the user is logged in
    with col2:
        if st.session_state.user["connected"]:
            if st.button("Log Out / تسجيل الخروج", key="logout_button", use_container_width=True):
                st.session_state.user = {
                    "connected": False,
                    "username": None,
                    "age": None
                }
                st.success("You have been logged out. / تم تسجيل خروجك.")

# Call the top navigation bar
top_navbar()

# -------------------------------
# Sidebar with Pages from "Pages" Folder
# -------------------------------
if st.session_state.user["connected"]:
    # Dynamically load pages from the "Pages" folder
    with st.sidebar:
        st.header("Pages / الصفحات")
        
        # Assuming the "Pages" folder is in the current directory and contains .py files for each page
        pages_folder = "Pages"
        if os.path.exists(pages_folder):
            page_files = [f for f in os.listdir(pages_folder) if f.endswith('.py')]
            page_names = [os.path.splitext(f)[0] for f in page_files]  # Remove the .py extension
            selected_page = st.selectbox("Select a page / اختر صفحة", page_names)
        else:
            st.warning(f"Folder '{pages_folder}' not found.")

    # Mode selection before the system message
    st.sidebar.header("Mode / الوضع")
    mode_options = [
        "Continue the course / متابعة الدرس",
        "Review a lesson / مراجعة درس",
        "Free discussion / مناقشة حرة",
        "Exam / امتحان"
    ]
    selected_mode = st.sidebar.selectbox("Which mode would you like? / أي وضع تود استخدامه", mode_options)

# -------------------------------
# Main Content Area
# -------------------------------
if st.session_state.user["connected"]:
    st.markdown("---")
    
    # Display a system message for the chatbot
    st.markdown("**System Message:** _Hello, tell us what you want!_")
    
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
            # Determine interaction mode
            interaction_mode = selected_mode.split(" / ")[0]  # Extract English part

            # Adapt the prompt based on the selected mode and user's age
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
                prompt = user_input  # Default fallback prompt
            
            # Get the model response using the interact module
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
