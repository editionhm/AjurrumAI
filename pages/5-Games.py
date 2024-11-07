import streamlit as st
import interact

# Function to generate a hint every three errors
def generate_hint(word, errors):
    hint_prompt = f"Give a vague definition for the word '{word}' without MENTIONING IT AT ALL. NEVER MENTION THE WORD."
    if errors % 3 == 0 and errors != 0:  # Provide a hint every 3 errors
        return interact.generate_llm(hint_prompt)
    return None

# Sidebar for level selection and new game button
with st.sidebar:
    level = st.selectbox("Level / المستوى", ["Beginner / مبتدئ", "Intermediate / متوسط", "Expert / خبير"])
    if st.button("New Game / لعبة جديدة"):
        # Fetch a new word and reset game variables without clearing the session
        prompt = f"Choose an Arabic word of {level} level for a hangman game. Output should be ONE WORD ONLY AND NOTHING ELSE."
        word = interact.generate_llm(prompt)
        
        st.session_state.word = word
        st.session_state.guessed_letters = ["_"] * len(word)
        st.session_state.errors = 0
        st.session_state.max_errors = 10
        st.session_state.attempts = set()

# Game Initialization
if 'word' not in st.session_state:
    # Fetching the Arabic word via the LLM if it's the first game
    prompt = f"Choose a RANDOM Arabic word of {level} level for a hangman game between 3 and 8 letters. Output should be ONE WORD ONLY AND NOTHING ELSE."
    word = interact.generate_llm(prompt)
    
    st.session_state.word = word
    st.session_state.guessed_letters = ["_"] * len(word)
    st.session_state.errors = 0
    st.session_state.max_errors = 10
    st.session_state.attempts = set()

# Displaying the game state
st.write("### Guess the Arabic word / خمن الكلمة بالعربية")

with st.chat_message("assistant"):
    st.write("Word / الكلمة: " + " ".join(st.session_state.guessed_letters))
    st.write(f"The word is : {st.session_state.word}")
    st.write(f"Remaining Attempts / المحاولات المتبقية: {st.session_state.max_errors - st.session_state.errors}")

# Input box to enter a letter
prompt = st.chat_input("Propose an Arabic letter / اقترح حرفا بالعربية")
if prompt:
    letter = prompt.strip()
    with st.chat_message("user"):
        st.write(f"Proposed letter / الحرف المقترح: {letter}")
        
    if letter in st.session_state.attempts:
        st.write("You have already tried this letter / لقد جربت هذا الحرف من قبل.")
    elif letter in st.session_state.word:
        # Reveal the letter in the guessed word
        for idx, char in enumerate(st.session_state.word):
            if char == letter:
                st.session_state.guessed_letters[idx] = letter
        with st.chat_message("assistant"):
            st.write("Correct letter! / حرف صحيح!")
    else:
        # Increase the error count if the letter is incorrect
        st.session_state.errors += 1
        with st.chat_message("assistant"):
            st.write(f"Incorrect letter. {st.session_state.max_errors - st.session_state.errors} attempts left / حرف غير صحيح. تبقى لك {st.session_state.max_errors - st.session_state.errors} محاولات.")

    # Add the letter to attempts
    st.session_state.attempts.add(letter)

    # Show a hint if the user reaches a multiple of 3 errors
    hint = generate_hint(st.session_state.word, st.session_state.errors)
    if hint:
        with st.chat_message("assistant"):
            st.write(f"Hint / تلميح: {hint}")

    # Check the game status
    if "_" not in st.session_state.guessed_letters:
        st.success("Congratulations! You've found the word 🎉 / تهانينا! لقد وجدت الكلمة 🎉.")
        st.write(f"The word was / كانت الكلمة: {st.session_state.word}")
        # Reset only game-specific variables for a new game
        st.session_state.word = interact.generate_llm(f"Choose an Arabic word of {level} level for a hangman game. Output should be ONE WORD ONLY AND NOTHING ELSE.")
        st.session_state.guessed_letters = ["_"] * len(st.session_state.word)
        st.session_state.errors = 0
        st.session_state.attempts = set()
    elif st.session_state.errors >= st.session_state.max_errors:
        st.error("You lost 😢 / لقد خسرت 😢.")
        st.write(f"The word was / كانت الكلمة: {st.session_state.word}")
        # Reset only game-specific variables for a new game
        st.session_state.word = interact.generate_llm(f"Choose an Arabic word of {level} level for a hangman game. Output should be ONE WORD ONLY AND NOTHING ELSE.")
        st.session_state.guessed_letters = ["_"] * len(st.session_state.word)
        st.session_state.errors = 0
        st.session_state.attempts = set()
