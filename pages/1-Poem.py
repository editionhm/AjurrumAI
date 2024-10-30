import streamlit as st
from interact import generate_llm  

# Configuration de la page
st.set_page_config(page_title="Arabic Poetry Generator | مولد الشعر العربي", page_icon="📜")
st.title("Arabic Poetry Generator | مولد الشعر العربي")

# Instructions
st.write("Enter a theme or line in Arabic, choose the style of poem, and generate an Arabic poem inspired by classical forms. | أدخل موضوعًا أو سطرًا باللغة العربية، ثم اختر نوع القصيدة، وولّد قصيدة عربية مستوحاة من الأشكال الكلاسيكية.")

# Saisie de texte en arabe
arabic_text = st.text_area("Enter text in Arabic | أدخل نصًا بالعربية", height=100)

# Sélection du type de poème
poem_type = st.radio(
    "Choose Poem Type | اختر نوع القصيدة",
    [
        "Rajaz | الرجز",
        "Tawil | الطويل",
        "Basit | البسيط",
    ],
)

# Fonction pour générer le prompt en fonction du type de poème
def create_prompt(text, poem_style):
    if poem_style == "Rajaz | الرجز":
        prompt = f"Compose a poem in the Arabic style of 'Rajaz' with rhythmic, short lines based on the theme: {text}. Examples of Rajaz style include expressive and straightforward verses."
    elif poem_style == "Tawil | الطويل":
        prompt = f"Compose a poem in the classical Arabic 'Tawil' meter, using long and flowing lines, inspired by the theme: {text}. Examples of Tawil are poetic and formal with rich imagery."
    elif poem_style == "Basit | البسيط":
        prompt = f"Create an Arabic poem in 'Basit' meter with smooth, balanced verses based on the theme: {text}. Basit is known for its flexibility in conveying thoughtful and emotional themes."
    else:
        prompt = f"Generate a poem based on the theme: {text}"
    return prompt

# Bouton pour générer le poème
if st.button("Generate Poem | ولّد القصيدة"):
    if arabic_text:
        # Créer le prompt en fonction du type de poème
        prompt = create_prompt(arabic_text, poem_type)
        # Appeler la fonction generate_llm pour créer le poème
        poem = generate_llm(prompt)
        
        # Afficher le poème généré
        st.write("Generated Poem | القصيدة المولدة:")
        st.text_area("Arabic Poem | القصيدة بالعربية", poem, height=200)
    else:
        st.warning("Please enter text in Arabic to generate a poem | يرجى إدخال نص بالعربية لتوليد القصيدة.")
