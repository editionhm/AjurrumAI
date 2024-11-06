import streamlit as st
import database, interact, iot_module

iot = iot_module.IterationOfThought(max_iterations=5, timeout=45, temperature=0.65)
age = 20  # Modifier pour récupérer depuis la base de données si nécessaire
language = "english"

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

chapters_list = interact.extract_chapters('./data/content_chapter.csv')
chapters_list_with_placeholder = ["Please select a chapter | اختر فصلاً"] + chapters_list


# -------------------------------
# Sidebar with Login or Conversations and Log Out
# -------------------------------

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "What do you want to study? | ماذا تريد أن تدرس؟"}]

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

if st.session_state.selected_mode == "Review a lesson | مراجعة درس":
    # Mode "Review a lesson" pour poser des questions basées sur le chapitre sélectionné
    if st.session_state.selected_chapter:
        st.markdown("### Review Questions | أسئلة المراجعة")
        questions = interact.generate_questions(st.session_state.selected_chapter, "./data/content_chapter.csv")
        
        if questions:
            for i, question in enumerate(questions, start=1):
                user_answer = st.text_input(f"Q{i}: {question['question']}", key=f"question_{i}")
                if user_answer:
                    if user_answer.lower().strip() == question['answer'].lower().strip():
                        st.success("Correct! | صحيح!")
                    else:
                        st.error(f"Incorrect. The correct answer is: {question['answer']} | خطأ. الإجابة الصحيحة هي: {question['answer']}")
        else:
            st.warning("No questions available for this chapter. | لا توجد أسئلة متاحة لهذا الفصل.")
    else:
        # Afficher le menu déroulant si aucun chapitre n'est sélectionné
        st.markdown("### Please select a chapter to review | الرجاء اختيار فصل للمراجعة")
        selected_chapter = st.selectbox('Select a Chapter | اختر فصلاً:', chapters_list_with_placeholder)
        
        if selected_chapter != "Please select a chapter | اختر فصلاً":
            st.session_state.selected_chapter = selected_chapter
            st.experimental_rerun()  # Recharger la page pour afficher les questions après la sélection

else:
    selected_chapter = st.selectbox('Select a Chapter | اختر فصلاً:', chapters_list_with_placeholder)

    if selected_chapter != "Please select a chapter | اختر فصلاً" and selected_chapter != st.session_state.selected_chapter:
        st.session_state.selected_chapter = selected_chapter
        st.session_state.messages.append({"role": "assistant", "content": f"You chose to study **{selected_chapter}** with the level : {level_mastery}. Let me think...!"})

        with st.spinner("Thinking..."):
            prompt = f"""You are an expert in teaching Arabic Grammar. The user has selected the following chapter: {selected_chapter}.""" 
            content_chapter = interact.extract_passage("./data/content_chapter.csv", selected_chapter)
            prompt += f"""The content of the chapter is the following {content_chapter}. Please explain it in a clear and engaging manner, and include examples for someone who has the level {level_mastery}.
            Always stay in the context of this chapter. Write in {language}. Use Arabic for examples and terminology."""
            
            response = interact.generate_llm(prompt)
            full_response = ''
            for item in response:
                full_response += item
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Write your text here | اكتب نصك هنا"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    context = st.session_state.conversation_context
    user_prompt = f"{context} The user asked: {prompt}. Remember, you are an Arabic Grammar teacher. Explain in {language}, with examples in Arabic."
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = interact.generate_llm(user_prompt)
            full_response = ''.join(response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.markdown(full_response)

st.markdown("---")
st.markdown("<h2 style='text-align: center;'>Start interacting with the chatbot to learn more! | ابدأ التفاعل مع الروبوت للتعلم أكثر!</h2>", unsafe_allow_html=True)
