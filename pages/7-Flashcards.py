import streamlit as st
import interact

# Initialize session state variables
if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = None
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "current_flashcard" not in st.session_state:
    st.session_state.current_flashcard = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Load chapters list and display selection box
chapters_list = interact.extract_chapters('./data/content_chapter.csv')
selected_chapter = st.selectbox('Select a Chapter | اختر فصلاً:', ["Please select a chapter | اختر فصلاً"] + chapters_list)

if selected_chapter != "Please select a chapter | اختر فصلاً" and selected_chapter != st.session_state.selected_chapter:
    # Update selected chapter
    st.session_state.selected_chapter = selected_chapter
    
    # Display selected chapter content
    content_chapter = interact.extract_passage("./data/content_chapter.csv", selected_chapter)
    st.write(f"**Content of Chapter:** {content_chapter}")
    
    # Generate flashcards for the chapter content using the LLM
    prompt = f"Create True or False questions based on this content: {content_chapter}. Format each flashcard as 'True or False: <statement>'."
    flashcards_response = interact.generate_llm(prompt)
    flashcards = [line.strip() for line in flashcards_response.splitlines() if line.strip()]
    st.session_state.flashcards = flashcards
    st.session_state.current_flashcard = 0
    st.session_state.feedback = ""

# Display current flashcard
if st.session_state.flashcards:
    current_flashcard_text = st.session_state.flashcards[st.session_state.current_flashcard]
    st.write(f"**Flashcard {st.session_state.current_flashcard + 1}:** {current_flashcard_text}")

    # True/False buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("True"):
            # Check answer and provide feedback
            prompt = f"Is the following statement true or false? '{current_flashcard_text}'"
            answer_response = interact.generate_llm(prompt).strip().lower()
            if "true" in answer_response:
                st.session_state.feedback = "Correct! ✅"
                st.session_state.current_flashcard += 1
            else:
                explanation_prompt = f"Explain why the following statement is false: '{current_flashcard_text}'"
                explanation_response = interact.generate_llm(explanation_prompt)
                st.session_state.feedback = f"Incorrect. ❌\n\nExplanation: {explanation_response}"
    
    with col2:
        if st.button("False"):
            # Check answer and provide feedback
            prompt = f"Is the following statement true or false? '{current_flashcard_text}'"
            answer_response = interact.generate_llm(prompt).strip().lower()
            if "false" in answer_response:
                st.session_state.feedback = "Correct! ✅"
                st.session_state.current_flashcard += 1
            else:
                explanation_prompt = f"Explain why the following statement is true: '{current_flashcard_text}'"
                explanation_response = interact.generate_llm(explanation_prompt)
                st.session_state.feedback = f"Incorrect. ❌\n\nExplanation: {explanation_response}"

    # Show feedback
    st.write(st.session_state.feedback)

    # Check if all flashcards are done
    if st.session_state.current_flashcard >= len(st.session_state.flashcards):
        st.success("Congratulations! You've completed all flashcards.")
        st.session_state.feedback = ""
        st.session_state.current_flashcard = 0  # Reset for another round if desired
