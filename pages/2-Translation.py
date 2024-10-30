import utils
import streamlit as st
from interact import generate_llm  

st.set_page_config(page_title="Translation Tool", page_icon="💬")
st.title("Translator English ↔️ Arabic")
st.header('Translator English ↔️ Arabic')
st.write('Allows users to interact with the LLM')
st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/shashankdeshpande/langchain-chatbot/blob/master/pages/1_%F0%9F%92%AC_basic_chatbot.py)')

st.write("Translation Tool")


# Définir la fonction de traduction en utilisant `generate_llm`
def translate(text, source_lang, target_lang):
    prompt = f"Translate this text from {source_lang} to {target_lang}: {text}"
    response = generate_llm(prompt)
    return response

# Interface Streamlit

# Zone de texte pour l'anglais (en haut)
english_text = st.text_area("Texte en Anglais", height=150)

# Bouton pour lancer la traduction
if st.button("Translate"):
    if english_text:
        # Appel de la fonction de traduction de l'anglais vers l'arabe
        translated_text = translate(english_text, "English", "Arabic")
        st.write("Traduction en Arabe :")
        st.text_area("Texte en Arabe", translated_text, height=150)
    else:
        st.warning("Veuillez entrer du texte en anglais pour traduire.")
        
# Zone de texte pour l'arabe (en bas)
arabic_text = st.text_area("Texte en Arabe", height=150)

# Vérifier si l'utilisateur a saisi du texte en arabe
if arabic_text and not english_text:
    translated_text = translate(arabic_text, "Arabic", "English")
    st.write("Translation in English:")
    st.text_area("Texte en Anglais", translated_text, height=150)
