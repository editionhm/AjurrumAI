import streamlit as st
from interact import generate_llm  # Assurez-vous que la fonction generate_llm est bien importée

# Configuration de la page
st.set_page_config(page_title="Arabic I'rab Analyzer | محلل إعراب النصوص العربية", page_icon="📖")
st.title("Arabic I'rab Analyzer | محلل إعراب النصوص العربية")

# Instructions pour l'utilisateur
st.write("Enter an Arabic text for grammatical analysis (I'rab), choose a style, and generate the I'rab details for the text. | أدخل نصًا عربيًا لتحليله إعرابيًا، ثم اختر الأسلوب، واحصل على تفاصيل الإعراب.")

# Saisie du texte en arabe
arabic_text = st.text_area("Enter Arabic Text | أدخل النص العربي", height=100)

# Choix du style d'I'rab
analysis_style = st.radio(
    "Choose Analysis Style | اختر أسلوب الإعراب",
    [
        "Detailed | الإعراب التفصيلي",
        "Simplified | الإعراب المبسط",
        "Academic | الإعراب الأكاديمي",
    ],
)

# Fonction pour créer le prompt en fonction du style d'I'rab et des exemples fournis
def create_irab_prompt(text, style):
    examples = """
    EXAMPLE 1:
    TEXT: {وَإِذا قِيلَ لَهُمْ لا تُفْسِدُوا فِي الْأَرْضِ قالُوا إِنَّما نَحْنُ مُصْلِحُونَ (11)}
    IRAB: "{وَإِذا}: (الواو): استئنافية. (إذا): ظرف لما يستقبل من الزمان، تضمن معنى الشرط، خافض لشرطه منصوب بجوابه... إلخ"

    EXAMPLE 2:
    TEXT: {مَثَلُهُمْ كَمَثَلِ الَّذِي اِسْتَوْقَدَ ناراً فَلَمّا أَضاءَتْ ما حَوْلَهُ ذَهَبَ اللهُ بِنُورِهِمْ وَتَرَكَهُمْ فِي ظُلُماتٍ لا يُبْصِرُونَ (17)}
    IRAB: "{مَثَلُهُمْ}: مبتدأ مرفوع و(الهاء) مضاف إليه. {كَمَثَلِ}: جار ومجرور، متعلق بمحذوف خبر..."

    EXAMPLE 3:
    TEXT: {أَوْ كَصَيِّبٍ مِنَ السَّماءِ فِيهِ ظُلُماتٌ وَرَعْدٌ وَبَرْقٌ يَجْعَلُونَ أَصابِعَهُمْ فِي آذانِهِمْ مِنَ الصَّواعِقِ حَذَرَ الْمَوْتِ وَاللهُ مُحِيطٌ بِالْكافِرِينَ (19)}
    IRAB: "{أَوْ}: عاطفة. {كَصَيِّبٍ}: جار ومجرور، متعلق بمحذوف خبر لمبتدأ محذوف..."

    """
    if style == "Detailed | الإعراب التفصيلي":
        prompt = f"{examples}\nPerform a detailed grammatical analysis (I'rab) for the following Arabic text:\n{text}"
    elif style == "Simplified | الإعراب المبسط":
        prompt = f"{examples}\nPerform a simplified grammatical analysis (I'rab) for the following Arabic text:\n{text}"
    elif style == "Academic | الإعراب الأكاديمي":
        prompt = f"{examples}\nPerform an academic-style grammatical analysis (I'rab) for the following Arabic text:\n{text}"
    else:
        prompt = f"{examples}\nAnalyze the following Arabic text:\n{text}"
    
    return prompt

# Bouton pour générer l'I'rab
if st.button("Generate I'rab | ولّد الإعراب"):
    if arabic_text:
        # Créer le prompt basé sur le style choisi
        prompt = create_irab_prompt(arabic_text, analysis_style)
        # Appeler la fonction generate_llm pour générer l'I'rab
        irab_result = generate_llm(prompt)
        
        # Afficher l'I'rab généré
        with st.chat_message("assistant"):
            st.write(irab_result)
    else:
        st.warning("Please enter Arabic text for analysis | يرجى إدخال نص عربي للتحليل.")
