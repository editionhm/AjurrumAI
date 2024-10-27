import streamlit as st
import database, interact, iot_module

iot = iot_module.IterationOfThought(max_iterations=5,timeout=45,temperature=0.7)
age = 20 ## a modifier pr reucp dans la database

user_db = database.connect_db()
# -------------------------------
# SECRETS
# -------------------------------
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

       with st.form("login"):
            # st.write("<h3 style='text-align: center;'>Log In | تسجيل الدخول.</h3>")
            st.markdown("<h3 style='text-align: center;'>Log In | تسجيل الدخول.</h3>", unsafe_allow_html=True)
            username = st.text_input("Username | اسم المستخدم", key="login_username")
            password = st.text_input("Password | كلمة المرور", type="password", key="login_password")
            # Every form must have a submit button.
            submitted = st.form_submit_button("Log In - تسجيل الدخول")
            if submitted:
                if user_db.find_one({'username' : username, 'password' : password}):
                    st.session_state.user = {
                    "connected": True,
                    "username": username,
                    "age": age
                    }
                    st.success(f"You are logged in as {username.upper()}", icon="✅")
                    del user_pas
                else:
                    st.session_state.user = {
                    "connected": False,
                    "username": None,
                    "age": age
                    }
                    login = login_form.form_submit_button(label='Sign In')
                    if login:
                        st.sidebar.error("Username or Password is incorrect.")
                

# -------------------------------
# Main Content Area
# -------------------------------
# Initialize session state for storing the selected chapter and messages
# Initialize session state for storing the selected chapter, messages, and conversation context
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "What do you want to study? | ماذا تريد أن تدرس؟"}]

if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = None

if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = ""

chapters_list = interact.extract_chapters('./data/ajurrumiyyah.txt')  # Update file path as needed

# Add a placeholder option to the chapters list to prevent auto-selection
chapters_list_with_placeholder = ["Please select a chapter | اختر فصلاً"] + chapters_list

if st.session_state.user["connected"]:
    st.markdown("---")

    # Dropdown menu for chapter selection, with the placeholder at the top
    selected_chapter = st.selectbox('Select a Chapter | اختر فصلاً:', chapters_list_with_placeholder)

    # Proceed only if the user has selected a valid chapter (not the placeholder)
    if selected_chapter != "Please select a chapter | اختر فصلاً" and selected_chapter != st.session_state.selected_chapter:
        # Update session state with the new selected chapter
        st.session_state.selected_chapter = selected_chapter
        st.session_state.conversation_context = f"The user has selected the chapter: {selected_chapter}. This chapter is about {selected_chapter}. You are an expert in Arabic Grammar."

        # Display the message informing the user about their choice
        st.session_state.messages.append({"role": "assistant", "content": f"You chose to study **{selected_chapter}**. Let me think...!"})

        # Generate a new response based on the selected chapter
        with st.spinner("Thinking..."):
            # Prepare the prompt for LLM with added context
            prompt = f"""You are an expert Arabic Grammar teacher. The user has selected the following chapter: {selected_chapter}. Please explain it in a clear and engaging manner, and include examples. Also, stay in the context of this chapter for further discussions. Never forget that the response has to do with Arabic Grammar explanation."""
            
            # Interact with LLM (replace with the proper method for LLM response)
            response = iot_module.run_iot(iot, prompt)

            # Display LLM response progressively
            full_response = ''
            for item in response:
                full_response += item

            # Add the assistant's response to session state to store chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Display existing chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User-provided prompt (allowing free conversation after the initial response)
    if prompt := st.chat_input("Write your text here | اكتب نصك هنا"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Prepare the updated prompt with conversation context and user question
        context = st.session_state.conversation_context
        user_prompt = f"{context} The user asked: {prompt}"

        # Interact with LLM to continue the conversation based on the context
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = iot_module.run_iot(iot, user_prompt)

                # Display LLM response progressively
                full_response = ''
                for item in response:
                    full_response += item

                # Store the assistant's response in the session state to continue chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                st.markdown(full_response)
else:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>Please log in or sign up to start interacting with the chatbot.</h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>الرجاء تسجيل الدخول أو إنشاء حساب لبدء التفاعل مع الروبوت.</h2>", unsafe_allow_html=True)

