import streamlit as st
import random
import time

# Sample phrases with Arabic and English pairs
phrases = [
    ("مرحبا", "Hello"),
    ("كيف حالك؟", "How are you?"),
    ("صباح الخير", "Good morning"),
    ("مساء الخير", "Good evening"),
    ("أين الحمام؟", "Where is the bathroom?"),
    ("أريد المساعدة", "I need help"),
    ("شكرا", "Thank you"),
    ("نعم", "Yes"),
    ("لا", "No"),
    ("أراك لاحقا", "See you later")
]

# Shuffle phrases and translations to display as buttons
if "shuffled_pairs" not in st.session_state or st.button("Reset Game"):
    # Duplicate and shuffle the list
    items = [(phrase, "arabic") for phrase, _ in phrases] + [(translation, "english") for _, translation in phrases]
    random.shuffle(items)
    
    # Initialize game state variables
    st.session_state.shuffled_pairs = items
    st.session_state.revealed = [False] * len(items)
    st.session_state.selected_buttons = []
    st.session_state.matched_buttons = []
    st.session_state.feedback = ""

# Callback to handle button click
def reveal_button(idx, text, lang):
    # Reveal the button temporarily
    st.session_state.revealed[idx] = True
    st.session_state.selected_buttons.append((idx, text, lang))
    
    # Check for matching pairs when two buttons are clicked
    if len(st.session_state.selected_buttons) == 2:
        (idx1, text1, lang1), (idx2, text2, lang2) = st.session_state.selected_buttons

        # Check if the two selected buttons form a correct pair
        if (lang1 != lang2) and ((text1, text2) in phrases or (text2, text1) in phrases):
            # Correct match; mark as permanently revealed
            st.session_state.matched_buttons.extend([idx1, idx2])
            st.session_state.feedback = f"Matched: {text1} - {text2} 🎉"
        else:
            # Incorrect match; hide both buttons after a short delay
            st.session_state.feedback = "Not a match! Try again."
            time.sleep(0.5)  # Pause for a brief moment to show both selections
            st.session_state.revealed[idx1] = False
            st.session_state.revealed[idx2] = False
        
        # Reset selected buttons for the next turn
        st.session_state.selected_buttons = []

# Display feedback message if any
if st.session_state.feedback:
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
