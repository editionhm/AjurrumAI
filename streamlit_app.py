import streamlit as st
import database  # Ensure this module handles MongoDB interactions
import interact   # Ensure this module handles LLM interactions (non-OpenAI)

age = 20 ## a modifier pr reucp dans la database

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="📚 AjurrumAI", layout="wide")

st.markdown("<h1 style='text-align: left; color: #2e7bcf;'>📚 AjurrumAI", unsafe_allow_html=True)
if not st.session_state.user["connected"]: 
    st.markdown("### Chat with the greatest Arabic Grammar expert!")
    st.markdown("### تحدث مع أكبر متخصص في قواعد اللغة العربية!")

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
            st.markdown("#### Mode | الوضع")
            mode_options = [
                "Continue the course | متابعة الدرس",
                "Review a lesson | مراجعة درس",
                "Free discussion | مناقشة حرة"
            ]
            selected_mode = st.selectbox("Which mode would you like ? | أي وضع تود استخدامه", mode_options, key='mode_select')
            st.session_state.selected_mode = selected_mode
    with col2:
        st.markdown("#### Col2 Test")
        
top_navbar()

# -------------------------------
# Sidebar with Login or Conversations and Log Out
# -------------------------------

with st.sidebar:
    if st.session_state.user["connected"]:
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
            else:
                st.error("Please enter both username and password. | الرجاء إدخال اسم المستخدم وكلمة المرور.")

# -------------------------------
# Main Content Area
# -------------------------------
if st.session_state.user["connected"]:
    st.markdown("---")

    # Store LLM generated responses
    if "messages" not in st.session_state: 
        st.session_state.messages = []
    
    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    # User-provided prompt
    
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = interact.generate_llm(prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
                        # st.write_stream(stream)
        
        message = {"role": "assistant", "content": full_response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
else:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>Please log in or sign up to start interacting with the chatbot.</h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>الرجاء تسجيل الدخول أو إنشاء حساب لبدء التفاعل مع الروبوت.</h2>", unsafe_allow_html=True)

