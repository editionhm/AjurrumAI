import streamlit as st
import interact

# Initialize session state variables
if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = None
    st.session_state.content_chapter = None
    st.session_state.flashcards_response = None
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
    prompt = f"Generate questions and answers based on the content of this chapter: {st.session_state.content_chapter}"
    flashcards_response = interact.generate_llm(prompt)
    st.session_state.flashcards_response = flashcards_response
    with st.chat_message("assistant"):
        st.write(flashcards_response)


# Add chat input for user responses
if prompt := st.chat_input("Write your answers here !"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    content_chapter = interact.extract_passage("./data/content_chapter.csv", st.session_state.selected_chapter)
    user_prompt = f" Here is the questions {st.session_state.flashcards_response}. The user gave those answers {prompt}. The context to check if answers are correct is : {content_chapter}. Check every answers given by the user and provide detailled explanation when it is false."

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
