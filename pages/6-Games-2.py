import streamlit as st
import random

# Sample Arabic phrases and their English translations
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

# Shuffle phrases and create buttons with hidden text
st.title("Match the Arabic Phrase with its English Translation")

# Initialize or reset game state variables
if "shuffled_phrases" not in st.session_state or st.button("Reset Game"):
    st.session_state.shuffled_phrases = phrases + [(eng, arabic) for arabic, eng in phrases]
    random.shuffle(st.session_state.shuffled_phrases)
    st.session_state.revealed = [False] * len(st.session_state.shuffled_phrases)
    st.session_state.selected_buttons = []
    st.session_state.matched_pairs = []

# Display the buttons and handle game logic
for idx, (text, translation) in enumerate(st.session_state.shuffled_phrases):
    if st.session_state.revealed[idx] or idx in st.session_state.matched_pairs:
        # Show the text if it's already matched or revealed
        st.button(text if text in [p[0] for p in phrases] else translation, key=idx, disabled=True)
    else:
        if st.button("?", key=idx):
            # Reveal the selected button
            st.session_state.revealed[idx] = True
            st.session_state.selected_buttons.append((idx, text, translation))

            # Check for pair matching logic
            if len(st.session_state.selected_buttons) == 2:
                # Get both selected buttons
                (idx1, text1, translation1), (idx2, text2, translation2) = st.session_state.selected_buttons

                # Check if they match
                if (text1 == text2 and translation1 == translation2) or (text1 == translation2 and translation1 == text2):
                    # If matched, store their indices to keep them revealed
                    st.session_state.matched_pairs.extend([idx1, idx2])
                    st.write(f"Matched: {text1} - {translation1} 🎉")
                else:
                    # If not matched, reset their reveal status after a short delay
                    st.warning("Not a match! Try again.")
                    st.session_state.revealed[idx1] = False
                    st.session_state.revealed[idx2] = False

                # Clear the selected buttons for the next attempt
                st.session_state.selected_buttons = []

# Check if all pairs are matched to end the game
if len(st.session_state.matched_pairs) == len(st.session_state.shuffled_phrases):
    st.success("Congratulations! You've matched all pairs.")
