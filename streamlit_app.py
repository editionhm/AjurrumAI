import streamlit as st
import database  # Ensure this module handles MongoDB interactions
import interact   # Ensure this module handles LLM interactions (non-OpenAI)

age = 20 ## a modifier pr reucp dans la database

url = st.secrets["URL"] 
token_iam = st.secrets["TOKEN"]
projet_id = st.secrets["PROJECT_ID"]

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="AjurrumAI", layout="wide", page_icon='📚')

st.markdown("<h1 style='text-align: left; color: #2e7bcf;'>📚 AjurrumAI", unsafe_allow_html=True)

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
# Top Navigation Bar with Greeting= """ def top_navbar():   col1, col2 = st.columns([1, 3]) top_navbar()"""
# -------------------------------

if not st.session_state.user["connected"]: 
    st.markdown("### Chat with the greatest Arabic Grammar expert!")
    st.markdown("### تحدث مع أكبر متخصص في قواعد اللغة العربية!")


# -------------------------------
# Sidebar with Login or Conversations and Log Out
# -------------------------------
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "What do you want to study? | ماذا تريد أن تدرس؟"}]

with st.sidebar:
    if st.session_state.user["connected"]:
        
        st.markdown("#### Mode | الوضع")
        mode_options = [
                "Continue the course | متابعة الدرس",
                "Review a lesson | مراجعة درس",
                "Free discussion | مناقشة حرة"
            ]
        selected_mode = st.selectbox("Which mode would you like ? | أي وضع تود استخدامه", mode_options, key='mode_select')
        st.session_state.selected_mode = selected_mode
        

        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
        
        
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
            st.rerun()

# -------------------------------
# If user is not logged in. Left menu bar        
# -------------------------------
    else:
        st.markdown("<h3 style='text-align: center;'>Log In | تسجيل الدخول.</h3>", unsafe_allow_html=True)

        username = st.text_input("Username | اسم المستخدم", key="login_username")
        password = st.text_input("Password | كلمة المرور", type="password", key="login_password")
        
        if st.button("Log In | تسجيل الدخول", key="login_button"):
            if username and password:
                st.session_state.user = {
                    "connected": True,
                    "username": username,
                    "age": age
                }
                st.success("Logged in successfully ! \n تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("Please enter both username and password. | الرجاء إدخال اسم المستخدم وكلمة المرور.")

# -------------------------------
# Main Content Area
# -------------------------------

if st.session_state.user["connected"]:
    st.markdown("---")
    st.session_state.messages.append({"role": "assistant", "content": "TEST TEST")
    # Store LLM generated responses
    if "messages" not in st.session_state: 
        st.session_state.messages = []
    
    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User-provided prompt
    if prompt := st.chat_input("Write your text here | اكتب نصك هنا"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    # if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = interact.generate_llm(prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
                #st.write_stream(full_response)
        
        message = {"role": "assistant", "content": full_response}
        # Add assistant reponse in chat history
        st.session_state.messages.append(message)
    
else:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>Please log in or sign up to start interacting with the chatbot.</h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>الرجاء تسجيل الدخول أو إنشاء حساب لبدء التفاعل مع الروبوت.</h2>", unsafe_allow_html=True)

