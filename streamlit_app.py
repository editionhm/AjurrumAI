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

if 'conversations' not in st.session_state:
    st.session_state.conversations = {}
    # Structure: {conversation_id: conversation_name}
    # TODO: Load user's conversations from MongoDB
    # st.session_state.conversations = database.get_user_conversations(st.session_state.user['username'])

if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = None

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = {}
    # Structure: {conversation_id: [message1, message2, ...]}
    # TODO: Load conversation histories from MongoDB
    # st.session_state.conversation_history = database.get_conversation_histories(st.session_state.user['username'])

# -------------------------------
# Top Navigation Bar with Greeting and Logout
# -------------------------------
def top_navbar():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Show the greeting message above the main title
        if st.session_state.user["connected"]:
            st.markdown(f"<h2>Hello, {st.session_state.user['username']}! | مرحبًا، {st.session_state.user['username']}!</h2>", unsafe_allow_html=True)

        # Application title and description
        st.markdown("<h1 style='text-align: left; color: #2e7bcf;'>📚 AjurrumAI | Teaching Chatbot</h1>", unsafe_allow_html=True)
        st.markdown("### Chat with the greatest Arabic grammar expert! \n تحدث مع أكبر متخصص في قواعد اللغة العربية!")

        # Mode selection when user is connected
        if st.session_state.user["connected"]:
            st.markdown("#### Mode | الوضع")
            mode_options = [
                "Continue the course | متابعة الدرس",
                "Review a lesson | مراجعة درس",
                "Free discussion | مناقشة حرة",
                "Exam | امتحان"
            ]
            selected_mode = st.selectbox("Which mode would you like? | أي وضع تود استخدامه", mode_options)
            st.session_state.selected_mode = selected_mode  # Store in session state for later use

    # Right side: Only show a "Log Out" button when the user is logged in
    with col2:
        if st.session_state.user["connected"]:
            if st.button("Log Out | تسجيل الخروج", key="logout_button", use_container_width=True):
                st.session_state.user = {
                    "connected": False,
                    "username": None,
                    "age": None
                }
                st.session_state.conversations = {}
                st.session_state.current_conversation = None
                st.session_state.conversation_history = {}
                st.success("You have been logged out. / تم تسجيل خروجك.")

# Call the top navigation bar
top_navbar()

# -------------------------------
# Sidebar with Login or Conversations
# -------------------------------
with st.sidebar:
    if st.session_state.user["connected"]:
        st.header("Conversations / المحادثات")

        if st.session_state.conversations:
            conversation_names = list(st.session_state.conversations.values())
            selected_conversation = st.selectbox("Select a conversation / اختر محادثة", conversation_names)
            # Set the current conversation based on selection
            for conv_id, conv_name in st.session_state.conversations.items():
                if conv_name == selected_conversation:
                    st.session_state.current_conversation = conv_id
                    break
        else:
            st.info("No conversations yet. / لا توجد محادثات بعد.")

        # Option to start a new conversation
        if st.button("Start a new conversation / بدء محادثة جديدة"):
            # Generate a new conversation ID
            conv_id = f"conv_{len(st.session_state.conversations) + 1}"
            conv_name = f"Conversation {len(st.session_state.conversations) + 1}"
            st.session_state.conversations[conv_id] = conv_name
            st.session_state.current_conversation = conv_id
            # Initialize empty conversation history
            st.session_state.conversation_history[conv_id] = []
            # TODO: Save new conversation to MongoDB
            # database.create_new_conversation(st.session_state.user['username'], conv_id, conv_name)
    else:
        st.header("Log In / تسجيل الدخول")
        # Create a login form in the sidebar
        username = st.text_input("Username / اسم المستخدم", key="login_username")
        password = st.text_input("Password / كلمة المرور", type="password", key="login_password")
        if st.button("Log In / تسجيل الدخول", key="login_button"):
            # For now, just set connected to True
            if username and password:
                st.session_state.user = {
                    "connected": True,
                    "username": username,
                    "age": 20  # Just an example
                }
                st.success("Logged in successfully! \n تم تسجيل الدخول بنجاح!")
                # TODO: Authenticate user using MongoDB
                # user = database.authenticate_user(username, password)
                # if user:
                #     st.session_state.user = {
                #         "connected": True,
                #         "username": user['username'],
                #         "age": user['age']
                #     }
                #     st.success("Logged in successfully! / تم تسجيل الدخول بنجاح!")
                # else:
                #     st.error("Invalid credentials. / بيانات اعتماد غير صالحة.")
            else:
                st.error("Please enter both username and password. / الرجاء إدخال اسم المستخدم وكلمة المرور.")

# -------------------------------
# Main Content Area
# -------------------------------
if st.session_state.user["connected"]:
    st.markdown("---")
    
    # Display the conversation history
    conv_id = st.session_state.current_conversation
    if conv_id and conv_id in st.session_state.conversation_history:
        st.markdown("### Conversation History / تاريخ المحادثة")
        for message in st.session_state.conversation_history[conv_id]:
            st.markdown(f"**You:** {message['user_input']}")
            st.markdown(f"**Bot:** {message['response']}")
            st.markdown("---")
    else:
        st.info("No conversation selected or no messages yet. / لم يتم اختيار محادثة أو لا توجد رسائل بعد.")
    
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
            selected_mode = st.session_state.get('selected_mode', "Free discussion / مناقشة حرة")
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

                    # Save the message and response to the conversation history
                    conv_id = st.session_state.current_conversation
                    if conv_id:
                        if conv_id not in st.session_state.conversation_history:
                            st.session_state.conversation_history[conv_id] = []
                        st.session_state.conversation_history[conv_id].append({
                            'user_input': user_input,
                            'response': response
                        })
                        # TODO: Save updated conversation history to MongoDB
                        # database.save_conversation(st.session_state.user['username'], conv_id, st.session_state.conversation_history[conv_id])
                    else:
                        st.warning("No conversation selected. / لم يتم اختيار محادثة.")
                else:
                    st.warning("No response received / لم يتم استلام رد")
            except Exception as e:
                st.error(f"An error occurred: {str(e)} / حدث خطأ: {str(e)}")

else:
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>Please log in or sign up to start interacting with the chatbot. \n الرجاء تسجيل الدخول أو إنشاء حساب لبدء التفاعل مع الروبوت.</h2>", unsafe_allow_html=True)
    # Optionally, you can add more content here for users who are not logged in

# -------------------------------
# Database and Interaction Modules
# -------------------------------
# Note: Ensure that the `database` and `interact` modules are properly implemented.
# The `database` module should handle user registration, login, and retrieval.
# The `interact` module should handle interactions with the LLM/API.
