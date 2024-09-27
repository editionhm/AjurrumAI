import streamlit as st
import os
import database  # Ensure this module handles MongoDB interactions
import interact   # Ensure this module handles LLM interactions (non-OpenAI)

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

if 'conversations' not in st.session_state:
    st.session_state.conversations = {}

if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = None

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = {}

if 'selected_mode' not in st.session_state:
    st.session_state.selected_mode = "Free discussion / مناقشة حرة"

# -------------------------------
# Top Navigation Bar with Greeting
# -------------------------------
def top_navbar():
    col1, col2 = st.columns([3, 1])

    with col1:
        if st.session_state.user["connected"]:
            st.markdown(f"<h2>Hello, {st.session_state.user['username']}! | مرحبًا، {st.session_state.user['username']}!</h2>", unsafe_allow_html=True)

        st.markdown("<h1 style='text-align: left; color: #2e7bcf;'>📚 AjurrumAI | Teaching Chatbot</h1>", unsafe_allow_html=True)
        st.markdown("### Chat with the greatest Arabic grammar expert! \n تحدث مع أكبر متخصص في قواعد اللغة العربية!")

        if st.session_state.user["connected"]:
            st.markdown("#### Mode | الوضع")
            mode_options = [
                "Continue the course | متابعة الدرس",
                "Review a lesson | مراجعة درس",
                "Free discussion | مناقشة حرة",
                "Exam | امتحان"
            ]
            selected_mode = st.selectbox("Which mode would you like? | أي وضع تود استخدامه", mode_options, key='mode_select')
            st.session_state.selected_mode = selected_mode

top_navbar()

# -------------------------------
# Sidebar with Login or Conversations and Log Out
# -------------------------------
with st.sidebar:
    if st.session_state.user["connected"]:
        st.header("Conversations | المحادثات")

        if st.session_state.conversations:
            conversation_names = list(st.session_state.conversations.values())
            selected_conversation = st.selectbox(
                "Select a conversation | اختر محادثة", conversation_names, key='conversation_select')
            for conv_id, conv_name in st.session_state.conversations.items():
                if conv_name == selected_conversation:
                    st.session_state.current_conversation = conv_id
                    break
        else:
            st.info("No conversations yet. | لا توجد محادثات بعد.")

        if st.button("Start a new conversation | بدء محادثة جديدة", key='new_conversation_button'):
            conv_id = f"conv_{len(st.session_state.conversations) + 1}"
            conv_name = f"Conversation {len(st.session_state.conversations) + 1}"
            st.session_state.conversations[conv_id] = conv_name
            st.session_state.current_conversation = conv_id
            st.session_state.conversation_history[conv_id] = []

        st.markdown("---")
        st.subheader("Manage Conversations | إدارة المحادثات")
        if st.session_state.conversations:
            conv_to_rename = st.selectbox("Select conversation to rename | اختر محادثة لإعادة تسميتها",
                                          options=list(st.session_state.conversations.values()),
                                          key='rename_select')
            new_name = st.text_input("New name | اسم جديد", key='new_conv_name')
            if st.button("Rename / إعادة تسمية", key='rename_button'):
                for conv_id, conv_name in st.session_state.conversations.items():
                    if conv_name == conv_to_rename:
                        st.session_state.conversations[conv_id] = new_name
                        if st.session_state.current_conversation == conv_id:
                            st.session_state.current_conversation = conv_id
                        st.success(f"Conversation renamed to {new_name} / تم إعادة تسمية المحادثة إلى {new_name}")

        st.markdown("---")
        if st.button("Log Out | تسجيل الخروج", key="logout_button"):
            st.session_state.user = {
                "connected": False,
                "username": None,
                "age": None
            }
            st.session_state.conversations = {}
            st.session_state.current_conversation = None
            st.session_state.conversation_history = {}
            st.success("You have been logged out. | تم تسجيل خروجك.")
    else:
        st.header("Log In / تسجيل الدخول")
        username = st.text_input("Username | اسم المستخدم", key="login_username")
        password = st.text_input("Password | كلمة المرور", type="password", key="login_password")
        if st.button("Log In / تسجيل الدخول", key="login_button"):
            if username and password:
                st.session_state.user = {
                    "connected": True,
                    "username": username,
                    "age": 20
                }
                st.success("Logged in successfully! | تم تسجيل الدخول بنجاح!")
            else:
                st.error("Please enter both username and password. | الرجاء إدخال اسم المستخدم وكلمة المرور.")

# -------------------------------
# Main Content Area
# -------------------------------
if st.session_state.user["connected"]:
    st.markdown("---")

    conv_id = st.session_state.current_conversation
    if conv_id and conv_id in st.session_state.conversation_history:
        st.markdown("### Conversation History | تاريخ المحادثة")
        for message in st.session_state.conversation_history[conv_id]:
            st.markdown(f"**You:** {message['user_input']}")
            st.markdown(f"**Bot:** {message['response']}")
            st.markdown("---")
    else:
        st.info("No conversation selected or no messages yet. | لم يتم اختيار محادثة أو لا توجد رسائل بعد.")

    st.markdown("**System Message:** _Hello, tell us what you want!_")

    st.markdown("""
    <style>
        .chat-input {
            border: 2px solid #2e7bcf;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            width: 100%;
            box-sizing: border-box;
        }
        .submit-button {
            margin-top: 10px;
            float: right;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_area(
            "Write your message here: | اكتب رسالتك هنا",
            placeholder="Type your message like in a chat... | اكتب رسالتك هنا مثل الدردشة...",
            height=100,
            key="chat_input",
            label_visibility="collapsed",
            help="Chat with the AI in real-time"
        )
        submit_button = st.form_submit_button("Submit | إرسال")

    if submit_button:
        if user_input.strip() == "":
            st.error("Please enter something. | الرجاء إدخال شيء.")
        else:
            selected_mode = st.session_state.get('selected_mode', "Free discussion / مناقشة حرة")
            interaction_mode = selected_mode.split(" / ")[0]

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
                prompt = user_input

            try:
                response = interact.generate_llm(prompt)  # Use custom model or Hugging Face API
                if response:
                    st.success("Response / الرد:")
                    st.write(response)

                    conv_id = st.session_state.current_conversation
                    if conv_id:
                        if conv_id not in st.session_state.conversation_history:
                            st.session_state.conversation_history[conv_id] = []
                        st.session_state.conversation_history[conv_id].append({
                            'user_input': user_input,
                            'response': response
                        })
                else:
                    st.warning("No response received | لم يتم استلام رد")
            except Exception as e:
                st.error(f"An error occurred: {str(e)} | حدث خطأ: {str(e)}")

else:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>Please log in or sign up to start interacting with the chatbot. \n الرجاء تسجيل الدخول أو إنشاء حساب لبدء التفاعل مع الروبوت.</h2>", unsafe_allow_html=True)
