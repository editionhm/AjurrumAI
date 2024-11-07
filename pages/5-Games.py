import streamlit as st
import interact

# Initialize session state variables if they don't exist
if 'attempts' not in st.session_state:
    st.session_state.attempts = set()
if 'errors' not in st.session_state:
    st.session_state.errors = 0
if 'max_errors' not in st.session_state:
    st.session_state.max_errors = 10
if 'word' not in st.session_state:
    # Fetch a new word via the LLM if it's the first game
    level = "Beginner"  # Example level; replace with actual level selection logic if needed
    prompt = f"Choose an Arabic word of {level} level for a hangman game. Output should be ONE WORD ONLY AND NOTHING ELSE."
    st.session_state.word = interact.generate_llm(prompt)
    st.session_state.guessed_letters = ["_"] * len(st.session_state.word)

# Display the game state
st.write("### Guess the Arabic word / خمن الكلمة بالعربية")
st.write("Word / الكلمة: " + " ".join(st.session_state.guessed_letters))
st.write(f"Remaining Attempts / المحاولات المتبقية: {st.session_state.max_errors - st.session_state.errors}")

# Input box to enter a letter
prompt = st.chat_input("Propose an Arabic letter / اقترح حرفا بالعربية")
if prompt:
    letter = prompt.strip()  # Ensure `letter` is defined if prompt is provided
    if letter:
        if letter in st.session_state.attempts:
            st.write("You have already tried this letter / لقد جربت هذا الحرف من قبل.")
        elif letter in st.session_state.word:
            # Reveal the letter in the guessed word
            for idx, char in enumerate(st.session_state.word):
                if char == letter:
                    st.session_state.guessed_letters[idx] = letter
            
            # Display updated guessed word
            with st.chat_message("assistant"):
                st.write("Correct letter! / حرف صحيح!")
                st.write("Current word: " + " ".join(st.session_state.guessed_letters))
        else:
            # Increase the error count if the letter is incorrect
            st.session_state.errors += 1
            with st.chat_message("assistant"):
                st.write(f"Incorrect letter. {st.session_state.max_errors - st.session_state.errors} attempts left / حرف غير صحيح. تبقى لك {st.session_state.max_errors - st.session_state.errors} محاولات.")
        
        # Add the letter to attempts
        st.session_state.attempts.add(letter)
