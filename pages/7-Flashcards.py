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
    st.session_state.flashcard_mode = True  # To toggle between flashcard and explanation modes

# Load chapters list and display selection box
chapters_list = interact.extract_chapters('./data/content_chapter.csv')
selected_chapter = st.selectbox('Select a Chapter | اختر فصلاً:', ["Please select a chapter | اختر فصلاً"] + chapters_list)

if selected_chapter != "Please select a chapter | اختر فصلاً" and selected_chapter != st.session_state.selected_chapter:
    # Update selected chapter
    st.session_state.selected_chapter = selected_chapter
    
    # Display selected chapter content
    st.session_state.content_chapter = interact.extract_passage("./data/content_chapter.csv", selected_chapter)
    
    # Generate bilingual flashcards for the chapter content using the LLM
    prompt = f"Elaborate some Questions and Answers based on the content of this chapter : {st.session_state.content_chapter}. Format each flashcard as 'True or False: <Arabic statement> | <English statement>'."
    flashcards_response = interact.generate_llm(prompt)
    flashcards = [line.strip() for line in flashcards_response.splitlines() if line.strip()]
    st.session_state.flashcards = flashcards
    st.session_state.current_flashcard = 0
    st.session_state.feedback = ""
    st.session_state.flashcard_mode = True  # Reset to flashcard mode

# Display current flashcard
if st.session_state.flashcards and st.session_state.flashcard_mode:
    current_flashcard_text = st.session_state.flashcards[st.session_state.current_flashcard]
    st.write(f"**Flashcard {st.session_state.current_flashcard + 1}:** {current_flashcard_text}")

    # True/False buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("True"):
            # Check answer and provide feedback
            prompt = f"""Is the following statement true or false? {current_flashcard_text} Please answer in both Arabic and English. Only answer based on this context : '{st.session_state.content_chapter}'"""
            answer_response = interact.generate_llm(prompt).strip().lower()
            if "true" in answer_response:
                st.session_state.feedback = "Correct! ✅ | صحيح! ✅"
                st.session_state.current_flashcard += 1
                st.write(f"**Flashcard {st.session_state.current_flashcard + 1}:** {current_flashcard_text}")
            else:
                explanation_prompt = f"Explain why the following statement is false in both Arabic and English: '{current_flashcard_text}' using this context : {st.session_state.content_chapter}"
                explanation_response = interact.generate_llm(explanation_prompt)
                st.session_state.feedback = f"Incorrect. ❌ | غير صحيح ❌\n\nExplanation | التوضيح: {explanation_response}"
                st.session_state.flashcard_mode = False  # Switch to explanation mode

    with col2:
        if st.button("False"):
            # Check answer and provide feedback
            prompt = f"Is the following statement true or false? '{current_flashcard_text}' Please answer in both Arabic and English. Only answer based on this context : {st.session_state.content_chapter}"
            answer_response = interact.generate_llm(prompt).strip().lower()
            if "false" in answer_response:
                st.session_state.feedback = "Correct! ✅ | صحيح! ✅"
                st.session_state.current_flashcard += 1
            else:
                explanation_prompt = f"Explain why the following statement is true in both Arabic and English: '{current_flashcard_text}'"
                explanation_response = interact.generate_llm(explanation_prompt)
                st.session_state.feedback = f"Incorrect. ❌ | غير صحيح ❌\n\nExplanation | التوضيح: {explanation_response}"
                st.session_state.flashcard_mode = False  # Switch to explanation mode
        

# Show feedback or explanation
if st.session_state.feedback:
    st.write(st.session_state.feedback)

# Switch back to flashcard mode after explanation
if not st.session_state.flashcard_mode:
    if st.button("Next Flashcard | التالي"):
        st.session_state.flashcard_mode = True
        st.session_state.feedback = ""

# Check if all flashcards are done
if st.session_state.current_flashcard >= len(st.session_state.flashcards):
    st.success("Congratulations! You've completed all flashcards. 🎉")
    st.session_state.current_flashcard = 0  # Reset for another round if desired
    st.session_state.flashcard_mode = True
