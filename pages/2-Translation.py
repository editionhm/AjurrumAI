import streamlit as st
from interact import generate_llm  

# Configurer la page
st.set_page_config(page_title="Translation Tool - Outil de Traduction", page_icon="💬")
st.title("Translator English ↔️ Arabic | مترجم إنجليزي ↔️ عربي")

# Définir la fonction de traduction en utilisant `generate_llm`
def translate(text, source_lang, target_lang, translation_type):
    prompt = f"Translate this text from {source_lang} to {target_lang}: {text}. You should use this translation type : {translation_type}. Only output the translation."
    response = generate_llm(prompt)
    return response

# Interface Streamlit


# Choix du type de traduction
translation_type = st.radio(
    "Choose Translation Type | اختر نوع الترجمة",
    [
        "Literal Translation | الترجمة الحرفية",
        "Contextual Translation | الترجمة السياقية",
        "Formal/Academic Translation | الترجمة الرسمية/الأكاديمية",
    ],
    help="Select the type of translation style you prefer | اختر نوع الترجمة الذي تفضله",
)

# Zone de texte pour l'anglais (en haut)
english_text = st.text_area("English Text | النص الإنجليزي", height=150)

# Zone de texte pour l'arabe (en bas)
arabic_text = st.text_area("Arabic Text | النص العربي", height=150)

# Bouton pour lancer la traduction
if st.button("Translate | ترجمة"):
    if english_text and not arabic_text:
        # Traduction de l'anglais vers l'arabe
        translated_text = translate(english_text, "English", "Arabic", translation_type)
        st.write("Arabic Translation | الترجمة إلى العربية:")
        st.text_area("النص العربي | Arabic Text", translated_text, height=150)
    elif arabic_text and not english_text:
        # Traduction de l'arabe vers l'anglais
        translated_text = translate(arabic_text, "Arabic", "English", translation_type)
        st.write("English Translation | الترجمة إلى الإنجليزية:")
        st.text_area("النص الإنجليزي | English Text", translated_text, height=150)
    else:
        st.warning("Please enter text in one of the boxes to translate. | يرجى إدخال النص في إحدى الحقول للترجمة.")
