import streamlit as st
import database, interact, iot_module

st.set_page_config(page_title="AjurrumAI", page_icon="💬")

iot = iot_module.IterationOfThought(max_iterations=5, timeout=45, temperature=0.65)
age = 20  # Modifier pour récupérer depuis la base de données si nécessaire
language = "english"

# -------------------------------
# CSS perso
# -------------------------------
st.markdown("""
    <style>
    .sticky-menu {
        position: -webkit-sticky;
        position: sticky;
        top: 0;
        z-index: 100;
        background-color: white;
        padding: 10px 0;
        border-bottom: 1px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)


# -------------------------------
# Initialize Session State
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "What do you want to study? | ماذا تريد أن تدرس؟"}]

if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = None

if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = ""

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Free discussion / مناقشة حرة"

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

if "show_correction" not in st.session_state:
    st.session_state.show_correction = False

chapters_list = interact.extract_chapters('./data/content_chapter.csv')
chapters_list_with_placeholder = ["Please select a chapter | اختر فصلاً"] + chapters_list

# -------------------------------
# Sidebar with options and controls
# -------------------------------
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "What do you want to study? | ماذا تريد أن تدرس؟"}]
    st.session_state.current_question_index = 0
    st.session_state.questions = []
    st.session_state.show_correction = False

with st.sidebar:
    st.markdown("#### Mode | الوضع")
    mode_options = [
        "Continue the course | متابعة الدرس",
        "Review a lesson | مراجعة درس",
        "Free discussion | مناقشة حرة"
    ]
    selected_mode = st.selectbox("Which mode would you like? | أي وضع تود استخدامه", mode_options, key='mode_select')
    st.session_state.selected_mode = selected_mode

    level_mastery = st.select_slider(
        "Select the level of the explanation",
        options=["Beginner", "Intermediate", "Advanced", "Expert"],
    )
    st.write("You selected the level", level_mastery)

    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# -------------------------------
# Main Content Area
# -------------------------------
st.markdown("---")

# -------------------------------
# Sticky Chapter Selection
# -------------------------------
with st.container():
    st.markdown('<div class="sticky-menu">', unsafe_allow_html=True)
    if st.session_state.selected_mode == "Continue the course | متابعة الدرس":
        selected_chapter = st.selectbox('Select a Chapter | اختر فصلاً:', chapters_list_with_placeholder)

        if selected_chapter != "Please select a chapter | اختر فصلاً" and selected_chapter != st.session_state.selected_chapter:
            st.session_state.selected_chapter = selected_chapter
            st.session_state.messages.append({"role": "assistant", "content": f"You chose to study **{selected_chapter}** with the level: {level_mastery}. Let me think...!"})

            with st.spinner("Thinking..."):
                prompt = f"""You are an expert Arabic Grammar teacher."""
                content_chapter = interact.extract_passage("./data/content_chapter.csv", selected_chapter)
                prompt += f"""The content of the chapter that you will explain is : {content_chapter}. 
                Please explain it in a clear and engaging manner. Remember the examples in the previous content. Write to someone who has the level {level_mastery}. 
                Always stay in the context of this chapter. Write in {language}. """

                response = interact.generate_llm(prompt)
                full_response = ''.join(response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.markdown('</div>', unsafe_allow_html=True)


# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Write your text here | اكتب نصك هنا"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    context = st.session_state.conversation_context
    content_chapter = interact.extract_passage("./data/content_chapter.csv", st.session_state.selected_chapter)
    user_prompt = f"""Answer to this request: {prompt}. Remember, you are an Arabic Grammar teacher and the content of the subject is : {content_chapter}. Explain in {language}."""
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = interact.generate_llm(user_prompt)
            full_response = ''.join(response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.markdown(full_response)

st.markdown("---")
# st.markdown("<h2 style='text-align: center;'>Start interacting with the chatbot to learn more! | ابدأ التفاعل مع الروبوت للتعلم أكثر!</h2>", unsafe_allow_html=True)
