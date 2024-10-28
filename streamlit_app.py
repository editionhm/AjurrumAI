import streamlit as st
import database, interact, iot_module

iot = iot_module.IterationOfThought(max_iterations=5,timeout=45,temperature=0.65)
age = 20 ## a modifier pr reucp dans la database
language = "english"
user_db = database.connect_db()

# -------------------------------
# PAGES
# -------------------------------

st.page_link("streamlit_app.py", label="AjurrumAI Chatbot", icon="🏠")
st.page_link("./pages/3-irab.py", label="I'rab Tool", icon="1️⃣")
st.page_link("./pages/2-Translation.py", label="Translation Tool", icon="2️⃣", disabled=False)
st.page_link("http://www.google.com", label="Google", icon="🌎")

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

        ### Age render

        level_mastery = st.select_slider(
            "Select the level of the explanation",
            options=[
                "Beginner",
                "Intermediate",
                "Advanced",
                "Expert",
            ],
        )
        st.write("You selected the level", level_mastery)
        
        ### Clear Chat History
    
        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
        
        ### Log Out Button 
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
                    del password
                    st.rerun()
                else:
                    st.session_state.user = {
                    "connected": False,
                    "username": None,
                    "age": age
                    }
                    st.error("Username or Password is incorrect.", icon="🚨")
                

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

chapters_list = interact.extract_chapters('./data/content_chapter.csv')  # Update file path as needed

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
        
        # use?? 
        # st.session_state.conversation_context = f"The user has selected the chapter: {selected_chapter}. This chapter is about {selected_chapter}. You are an expert in Arabic Grammar."

        # Display the message informing the user about their choice
        st.session_state.messages.append({"role": "assistant", "content": f"You chose to study **{selected_chapter}**. Let me think...!"})

        # Generate a new response based on the selected chapter
        with st.spinner("Thinking..."):
            # Prepare the prompt for LLM with added context
            prompt = f"""You are an expert in teaching Arabic Grammar. The user has selected the following chapter : {selected_chapter}.""" 

            content_chapter = interact.extract_passage("./data/content_chapter.csv", selected_chapter)
            prompt += f"""The content of the chapter is the following {content_chapter}. Please explain it in a clear and engaging manner, and include examples for someone who have the level {level_mastery}.
            Also, stay in the context of this chapter for further discussions. Always write in {language}. Remember : you are an Arabic Grammar teacher."""
            
            # Interact with LLM (replace with the proper method for LLM response)
            #response = iot_module.run_iot(iot, prompt)
            response = interact.generate_llm(prompt)
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
        context = interact.generate_llm(f"Here is the chat history or resume between a user and a chatbot for Arabic Grammar. Make a resume of this the most concise possible without losing any informations. Here is the context : {context}")
        user_prompt = f"{context} The user asked: {prompt}. Remember, you are an Arabic Grammar teacher. Explain the best as possible with examples in arabic. Answer in {language} but with arabic text for examples and TERMINOLOGICAL terms"
        with st.chat_message("user"):
            st.write(f"{prompt }")

        # Interact with LLM to continue the conversation based on the context
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # response = iot_module.run_iot(iot, user_prompt)
                response = interact.generate_llm(user_prompt)

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

