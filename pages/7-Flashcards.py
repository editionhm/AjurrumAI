import streamlit as st
import interact

# Initialize session state variables
if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = None
    st.session_state.content_chapter = None
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "current_flashcard" not in st.session_state:
    st.session_state.current_flashcard = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "flashcard_mode" not in st.session_state:
    st.session_state.flashcard_mode = True
if "messages" not in st.session_state:
    st.session_state.messages = []  # For chat messages
if "qa_pairs" not in st.session_state:
    st.session_state.qa_pairs = []  # To save questions and answers

# Load chapters list and display selection box
chapters_list = interact.extract_chapters('./data/content_chapter.csv')
selected_chapter = st.selectbox('Select a Chapter | اختر فصلاً:', ["Please select a chapter | اختر فصلاً"] + chapters_list)

if selected_chapter != "Please select a chapter | اختر فصلاً" and selected_chapter != st.session_state.selected_chapter:
    # Update selected chapter
    st.session_state.selected_chapter = selected_chapter
    st.session_state.content_chapter = interact.extract_passage("./data/content_chapter.csv", selected_chapter)
    
    # Generate questions and answers for the chapter content using the LLM
    prompt = f"Generate questions and answers based on the content of this chapter: {st.session_state.content_chapter}. Format the response as follows: #1 question1 .. #2 question2 .. # answer1 .. # answer2 .."
    flashcards_response = interact.generate_llm(prompt)

    # Process the response to separate questions and answers
    qa_pairs = [line.strip() for line in flashcards_response.splitlines() if line.strip()]
    st.session_state.qa_pairs = qa_pairs  # Save the QA pairs for later validation

    # Extract questions only for displaying flashcards
    questions = [qa for qa in qa_pairs if qa.startswith("#")]
    st.session_state.flashcards = questions

    # Display all generated questions as flashcards for review
    st.write("Generated Questions:")
    for question in st.session_state.flashcards:
        st.write(question)

# Add chat input for user responses
if prompt := st.chat_input("Write your text here | اكتب نصك هنا"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    content_chapter = interact.extract_passage("./data/content_chapter.csv", st.session_state.selected_chapter)
    user_prompt = f"Answer to this request: {prompt}. Remember, you are an Arabic Grammar teacher and the content of the subject is: {content_chapter}. Explain in both Arabic and English."

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Generate assistant's response based on user input
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = interact.generate_llm(user_prompt)
            full_response = ''.join(response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.markdown(full_response)

# Check if user responses are close to saved QA pairs
user_answer_prompt = f"Check if the user's answer is close and correct to the saved questions and answers: {st.session_state.qa_pairs}"
if prompt:
    response = interact.generate_llm(user_answer_prompt)
    with st.chat_message("assistant"):
        st.write(response)
