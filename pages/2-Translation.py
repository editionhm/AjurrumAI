import streamlit as st
from interact import generate_llm  

# Configurer la page
st.set_page_config(page_title="Translation Tool - Outil de Traduction", page_icon="💬")
st.title("Translator English ↔️ Arabic | مترجم إنجليزي ↔️ عربي")

# Définir la fonction de pré-analyse pour identifier le style et le registre
def analyze_text(text, source_lang):
    analysis_prompt = f"""
You are an expert in language analysis. Analyze the following {source_lang} text and provide a brief description of its topic, style, and register. Respond in this format: "Topic: ..., Style: ..., Register: ...".
Text: {text}
"""
    analysis_response = generate_llm(analysis_prompt)
    return analysis_response

# Définir la fonction de traduction en utilisant `generate_llm`
def translate(text, source_lang, target_lang, analysis_info):
    pre_prompt = f"""
Act as a translator from {source_lang} to {target_lang}. You are an excellent translator who maintains the meaning and provides a high-quality translation that preserves the structure and every word in a sentence. Take into account the following analysis: {analysis_info}.
Translate the following text:
{text}
Only output the translation.
"""
    response = generate_llm(pre_prompt)
    return response

# Interface Streamlit

# Zone de texte pour l'anglais (en haut)
english_text = st.text_area("English Text | النص الإنجليزي", height=150)

# Zone de texte pour l'arabe (en bas)
arabic_text = st.text_area("Arabic Text | النص العربي", height=150)

# Bouton pour lancer la traduction
if st.button("Translate | ترجمة"):
    if english_text and not arabic_text:
        # Analyse du texte en anglais
        analysis_info = analyze_text(english_text, "English")
        st.write("Analysis Information:")
        st.text(analysis_info)
        
        # Traduction de l'anglais vers l'arabe
        translated_text = translate(english_text, "English", "Arabic", analysis_info)
        with st.chat_message("assistant"):
            st.write(translated_text)
    elif arabic_text and not english_text:
        # Analyse du texte en arabe
        analysis_info = analyze_text(arabic_text, "Arabic")
        st.write("Analysis Information:")
        st.text(analysis_info)
        
        # Traduction de l'arabe vers l'anglais
        translated_text = translate(arabic_text, "Arabic", "English", analysis_info)
        with st.chat_message("assistant"):
            st.write(translated_text)
    else:
        st.warning("Please enter text in one of the boxes to translate. | يرجى إدخال النص في إحدى الحقول للترجمة.")
