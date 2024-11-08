import streamlit as st
import random
import interact

# Function to generate English-Arabic pairs using LLM
def generate_pairs(num_pairs=10):
    """
    Generate English-Arabic word/phrase pairs using the LLM.
    
    Parameters:
        num_pairs (int): Number of pairs to generate. Default is 10.
        
    Returns:
        List[Tuple[str, str]]: A list of tuples where each tuple contains an Arabic phrase and its English translation.
    """
    pairs = []
    
    for _ in range(num_pairs):
        prompt = "Generate a common Arabic phrase and its English translation as a pair."
        result = interact.generate_llm(prompt)
        
        # Parse the response assuming it returns a pair like "مرحبا - Hello"
        try:
            arabic, english = result.split(" - ")
            pairs.append((arabic.strip(), english.strip()))
        except ValueError:
            print(f"Unexpected response format: {result}")

    return pairs

# Generate or reset game state only on "Reset Game" button click
if "shuffled_pairs" not in st.session_state or st.button("Reset Game"):
    # Generate new pairs when resetting the game
    phrases = generate_pairs()
    st.write("TEST GEN PAIRS:", phrases)
    # Duplicate and shuffle the list of pairs
    items = [(phrase, "arabic") for phrase, _ in phrases] + [(translation, "english") for _, translation in phrases]
    random.shuffle(items)
    
    # Initialize game state variables
    st.session_state.shuffled_pairs = items
    st.session_state.revealed = [False] * len(items)
    st.session_state.selected_buttons = []
    st.session_state.matched_buttons = []
    st.session_state.feedback = ""  # Initialize feedback

# Callback to handle button click
def reveal_button(idx, text, lang):
    # Reveal the button temporarily
    st.session_state.revealed[idx] = True
    st.session_state.selected_buttons.append((idx, text, lang))

    # Check if two buttons have been selected
    if len(st.session_state.selected_buttons) == 2:
        (idx1, text1, lang1), (idx2, text2, lang2) = st.session_state.selected_buttons

        # Check if the two selected buttons form a correct pair
        if (lang1 != lang2) and ((text1, text2) in phrases or (text2, text1) in phrases):
            # Correct match; mark as permanently revealed
            st.session_state.matched_buttons.extend([idx1, idx2])
            st.session_state.feedback = f"Matched: {text1} - {text2} 🎉"
            st.session_state.selected_buttons = []  # Clear selected buttons after a match
        else:
            # Incorrect match; wait for a third click to reset
            st.session_state.feedback = "Not a match! Click another card to try again."

    # On third click, reset revealed state if there was no match
    elif len(st.session_state.selected_buttons) == 3:
        idx1, _, _ = st.session_state.selected_buttons[0]
        idx2, _, _ = st.session_state.selected_buttons[1]
        if idx1 not in st.session_state.matched_buttons and idx2 not in st.session_state.matched_buttons:
            st.session_state.revealed[idx1] = False
            st.session_state.revealed[idx2] = False
        st.session_state.selected_buttons = [st.session_state.selected_buttons[2]]  # Keep only the third click

# Display feedback message if any
if st.session_state.feedback:
    with st.chat_message("assistant"):
        st.write(st.session_state.feedback)

# Display the buttons in a grid format
cols_per_row = 4
rows = [st.columns(cols_per_row) for _ in range((len(st.session_state.shuffled_pairs) + cols_per_row - 1) // cols_per_row)]
for idx, (text, lang) in enumerate(st.session_state.shuffled_pairs):
    row = rows[idx // cols_per_row]
    col = row[idx % cols_per_row]

    # Display the button text if it’s matched or temporarily revealed
    if st.session_state.revealed[idx] or idx in st.session_state.matched_buttons:
        col.button(text, key=idx, disabled=True)
    else:
        # Hidden button that reveals text on click
        col.button("?", key=idx, on_click=reveal_button, args=(idx, text, lang))

# End of game check
if len(st.session_state.matched_buttons) == len(st.session_state.shuffled_pairs):
    st.success("Congratulations! You've matched all pairs.")
