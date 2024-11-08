import streamlit as st
import database, interact, iot_module
import csv
from datetime import datetime

st.set_page_config(page_title="AjurrumAI", page_icon="💬")

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
# Sidebar with options and controls
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
    st.session_state.selected_mode = st.selectbox("Which mode would you like? | أي وضع تود استخدامه", mode_options, key='mode_select')

    level_mastery = st.select_slider(
        "Select the level of the explanation",
        options=["Beginner", "Intermediate", "Expert"],
    )
    st.write("You selected the level", level_mastery)

    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# -------------------------------
# Main Content Area
# -------------------------------
st.write("AjurrumAI is a personalized, interactive language assistant that adapts to your learning style, making Arabic grammar and cultural nuances accessible and engaging for learners at any level.")
st.markdown("---")

# Display chapter selection if in "Continue the course" mode
if st.session_state.selected_mode == "Continue the course | متابعة الدرس":
    selected_chapter = st.selectbox('Select a Chapter | اختر فصلاً:', chapters_list_with_placeholder)

    if selected_chapter != "Please select a chapter | اختر فصلاً" and selected_chapter != st.session_state.selected_chapter:
        st.session_state.selected_chapter = selected_chapter
        st.session_state.messages.append({"role": "assistant", "content": f"You chose to study **{selected_chapter}** with the level: {level_mastery}. Let me think...!"})

        with st.spinner("Thinking..."):
            prompt = f"You are an expert Arabic Grammar teacher."
            content_chapter = interact.extract_passage("./data/content_chapter.csv", selected_chapter)
            prompt += f"The content of the chapter that you will explain is : {content_chapter}. Explain it in a clear and engaging manner. Write to someone who has the level {level_mastery} in {language}."
            
            response = interact.generate_llm(prompt)
            full_response = ''.join(response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input and assistant response
if prompt := st.chat_input("Write your text here | اكتب نصك هنا"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    content_chapter = interact.extract_passage("./data/content_chapter.csv", st.session_state.selected_chapter)
    user_prompt = f"Answer to this request: {prompt}. Remember, you are an Arabic Grammar teacher and the content of the subject is : {content_chapter}. Explain in {language}."
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = interact.generate_llm(user_prompt)
            full_response = ''.join(response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.markdown(full_response)

    # User feedback on assistant's response
    st.write("Was this response helpful?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes"):
            save_feedback(prompt, full_response, is_helpful=True)
            st.success("Thank you for your feedback!")
    with col2:
        if st.button("No"):
            save_feedback(prompt, full_response, is_helpful=False)
            st.warning("Thank you for your feedback!")

# Function to save feedback to CSV
def save_feedback(question, response, is_helpful):
    feedback_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "response": response,
        "is_helpful": is_helpful
    }
    with open("feedback.csv", mode="a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "question", "response", "is_helpful"])
        if file.tell() == 0:  # Write header if file is empty
            writer.writeheader()
        writer.writerow(feedback_data)
