import streamlit as st
import interact
from datetime import datetime
import csv

# Configurer la page
st.set_page_config(page_title="AjurrumAI: Interactive Arabic Learning", page_icon="💬")

# Title
st.title("AjurrumAI: Interactive Arabic Learning")
st.markdown("Select a chapter to begin learning with interactive Q&A! | اختر فصلاً لتبدأ التعلم بأسئلة وإجابات تفاعلية!")
st.markdown("---")

# -------------------------------
# Initialize Session State
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "What would you like to study? | ماذا تريد أن تدرس؟"}]

if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = None

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

# Load chapters list
chapters_list = interact.extract_chapters('./data/content_chapter.csv')
chapters_list_with_placeholder = ["Please select a chapter | اختر فصلاً"] + chapters_list

# -------------------------------
# Sidebar with options and controls
# -------------------------------
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "What would you like to study? | ماذا تريد أن تدرس؟"}]
    st.session_state.questions = []
    st.session_state.current_question_index = 0

with st.sidebar:
    st.markdown("#### Mode | الوضع")
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# -------------------------------
# Main Content Area
# -------------------------------
# Chapter Selection
selected_chapter = st.selectbox('Select a Chapter | اختر فصلاً:', chapters_list_with_placeholder)

if selected_chapter != "Please select a chapter | اختر فصلاً" and selected_chapter != st.session_state.selected_chapter:
    st.session_state.selected_chapter = selected_chapter
    st.session_state.messages.append({"role": "assistant", "content": f"You chose to study **{selected_chapter}**. Let's start!"})

    # Load content and generate questions from selected chapter
    content_chapter = interact.extract_passage("./data/content_chapter.csv", selected_chapter)
    prompt = f"You are an Arabic language tutor. Generate a series of questions based on the following content: {content_chapter}. Write the explanation in english but examples and phrases in both arabic and english"
    questions = interact.generate_questions(prompt, file_path="./data/content_chapter.csv", level_mastery="Beginner")
    
    # Assign questions directly if it’s already a list
    st.session_state.questions = questions
    st.session_state.current_question_index = 0

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interactive Q&A based on questions generated from the chapter
if st.session_state.questions:
    current_question = st.session_state.questions[st.session_state.current_question_index]
    st.markdown(f"**Question:** {current_question}")

    # User response
    user_answer = st.text_input("Your answer | إجابتك هنا")
    if user_answer:
        # Append user's answer to messages
        st.session_state.messages.append({"role": "user", "content": user_answer})
        
        # Verify user's answer
        verification_prompt = f"As an Arabic tutor, verify if this answer is correct: '{user_answer}' based on the question: '{current_question}'."
        verification_response = interact.verify_answer(verification_prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": verification_response})
        
        # Move to next question
        if st.session_state.current_question_index < len(st.session_state.questions) - 1:
            st.session_state.current_question_index += 1
        else:
            st.markdown("End of questions for this chapter! | انتهت الأسئلة لهذا الفصل.")
            st.session_state.questions = []

# User input and assistant response for custom questions
if prompt := st.chat_input("Ask a custom question or comment | اطرح سؤالاً أو تعليقاً"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    content_chapter = interact.extract_passage("./data/content_chapter.csv", st.session_state.selected_chapter)
    user_prompt = f"Answer this request as an Arabic Grammar teacher: '{prompt}'. Content from chapter: {content_chapter}."
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = interact.generate_llm(user_prompt)
            full_response = ''.join(response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.markdown(full_response)

# Function to save feedback
def save_feedback(question, response, is_correct):
    feedback_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "response": response,
        "is_correct": is_correct
    }
    with open("feedback.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "question", "response", "is_correct"])
        if file.tell() == 0:  # Write header if file is empty
            writer.writeheader()
        writer.writerow(feedback_data)
