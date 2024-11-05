import streamlit as st
from interact import generate_llm  

# Configurer la page
st.set_page_config(page_title="Translation Tool - Outil de Traduction", page_icon="💬")
st.title("Translator English ↔️ Arabic | مترجم إنجليزي ↔️ عربي")

# Définir la fonction de traduction en utilisant `generate_llm`
def translate(text, source_lang, target_lang, translation_type):
    pre_prompt = """
Act as a translator from Arabic to French. You are an excellent translator who maintains the meaning and provides a high-quality translation that preserves the structure and every word in a sentence. You are specialized in Islamic texts. I will provide you with an example of an Arabic text and its translation:

أولياء الله () لا يتكلمون إلا بحقائق وهذا الأمر قد تستصعب
العقول القاصرة فهمه. لما نسمع أن الولي لا يتصرف ولا يتحرك ولا ينطق
إلا بإذن؛ عقولنا لا تستوعب هذا الأمر. أنا سمعتها من شيخي الشيخ رجب
(ه)، سمعته يقول: يا ابني الشيخ لا يتحرك ولا يتصرف ولا ينطق إلا
بإذن كل حركة وكل تصرف بإذن. وهذا فعل مشاهد المشاهد ليس
۹۳"
"كالمحجوب؛ المشاهد المفتوح عليه يتصرف بما يؤذن له وليس له التصرف
نفسه وإنما تصرفه بربّه فنأى عن نفسه فلم يبق لنفسه حظ، وأصبح
من
تصرفه ربانيًا من عند الله.
ومولاي عبد السلام بن مشيش لما يكلمنا ويحدثنا بهذه المقامات، وهذه
الفتوحات المعرفة بقَدْر رسول الله (ﷺ) ؛ إنما هو كلام وتعريف مشاهد. ولقد
لمسنا أن صلاة سيدي ابن مشيش كلّها مقامات.
فابتدأ ( الصَّلاة بأن قال: ""اللَّهُمَّ  َصلَّ على من منه انشقت الأسرار""،
وأعظم سر بالنسبة للشيخ: هو السر المستودع في قلب الشيخ الذي دله على
الله. فمولاي عبد السَّلام له شيخه الذي سلّكه وعرفه وعلمه ودله على ربه،
وذاك الشيخ لا يمكن أن يسلك ويعرف إلا إذا حمل سرا من أسرار رسول
الله (ﷺ). فلما قال الشيخ عبد السَّلام: ""اللَّهُمَّ صَلِّ على من منه انشقت
الأسرار""، فإن أول سر وأعظم سر : هو السر المستودع في قلب شيخه، فبدأ
بشيخه، ثم وصف ما صدر عن رسول الله (ﷺ) من أسرار وأنوار، ثم تكلم
عن رسول الله (ﷺ)؛ عن ذات رسول الله (ﷺ)، عن الذات المحمدية:
""اللَّهُمَّ إنه سرك الجامع الدال عليك، وحجابك الأعظم القائم لك بين
يديك"". ولما وقف على هذا الباب العظيم فقد وقف برفقة شيخه، فالمريد لا
يترك يد شيخه على كل حال، وفي كل حال، مهما وصل المريد في سلوكه لا
6
٩٤"
"بد أن يُبقي يده بيد الشيخ. إن نسي شيخه الذي دله على الله وآزره وعلمه
:
فهو عاق بالشيخ.
مهما فتح للمريد، ومهما رأى، ومهما شهد، ومهما ارتقى، فيده يجب أن
تكون بيد شيخه، وإليك إشارة من إشارات النبي ( ) في ليلة المعراج، ففي
تلك الليلة حين ارتقى رسول الله (ﷺ) إلى حيث لا يرتقي بشر ولا ملك، لا
يرتقي إلى هذا المقام إلا سيد الوجود؛ سيدي رسول الله (ﷺ)، لما وصل سمع
صوت أبي بكر فقال لربه قبل قدومي عليك سمعت مناديا ينادى بلغة تشبه
لغة أبى بكر ... فقال تعالى: «... لما كان أنسك بصاحبك أبي بكر وأنك خُلقت
أنت
وهو من طينة واحدة، وهو أنيسك فى الدنيا والآخرة، خلقنا ملكا على
صورته يناديك بلغته»]. هذا مقام لا يصله أبو بكر ولا سواه، لكن عَلِمَ الله أن
النبي (ﷺ) يُحب صاحبه فأراد أن يُسْمعه صوته. فمع أن سيدنا النبي (ﷺ) هو
شيخ أبي بكر، لكنها كانت إشارة إلى أن المريد لا ينسى حبيبه في الله وهو
شيخه الذي لا هم له إلا أن يدله على ربه ).
والشيخ لما وصل إلى الحضرة المحمدية وسماها بالحجاب
الأعظم ) ، يعني: الحاجب الدال على الله، الواقف على باب الله، بل هو
باب الله، لما وقف أمام الباب ما اكتفى الشيخ بالباب فهو يريد أن يصل
(۱) ذكره القسطلاني في المنح المحمدية . ج ۲، ص ٤٨٣ .
۹۵"
"إلى المحراب، إلى رب الأرباب، فقال : ""واحملني على سبيله إلى
حضرتك""، مخاطبًا الله بقوله : يا رب ! احملني على سبيل الحجاب الأعظم إلى
حضرتك، يعني: اسلك
: اسلك بى الطريق الذي أصل به إليك، لكن على سبيل رسول
الله ) ، وتحت كنف ورعاية رسول الله (ﷺ).
هنا الشيخ يطلب الله ؛ يطلب الولوج إلى الحضرة، لكن، تحت قيادة
ومظلة وجناح رسول الله (ﷺ) الحجاب الأعظم. وما اكتفى الشيخ وإنما يريد
ما وراء الحجاب وهو رب الأرباب سبحانه وتعالى، ثم قال: ""واجعل الحجاب
الأعظم حياة روحي"" لما قال: ""احملني على سبيله إلى حضرتك"" فهذا يعني أن
الشيخ دخل إلى الحضرة بقيادة رسول الله (ﷺ).
لكن حتى نفهم مقصود الشيخ هنا لما صاغ هذه الصَّلاة بصيغة الدعاء
فهو لا يطلب مجهولاً، وإنما يطلب مقامات هو بها عليم. كيف يطلب أن
يُنتَشَل من أوحال التوحيد ويغرق في عين بحر الوحدة، وأن يُحمل على سبيل
رسول الله (ﷺ) إلى حضرة الله. إذا هذا ليس بطلب، ولا دعاء، فالشيخ ما
تكلم عن هذه المقامات إلا وهو يعرفها ويدركها، لكنه يطلبها ويسردها بصيغة
الدعاء أدبا مع المقام؛ حتى لا يُظهر أنه تحقق وإنما بقي في مقام العبودية،
مقام السائل الداعي الطالب، فكل هذه المقامات التي ذكرها الشيخ إنما هو بها
عليم، وهو لها واصل، ويعلمها ويعرفها.

Allāh's chosen ones (awliyā') only speak the truth (ḥaqā’iq). However, this matter can be difficult for minds with limited understanding to grasp. When we hear that a saint does not act, move, or speak except with permission (idhn), our minds struggle to comprehend this. I heard my master, Shaykh Rajab (ra), say: "O my son! The master does not move, act, or speak except with permission. Every movement and action is by permission. This is the act of one who is a witness (mushāhid). The witness is not like the one who is veiled (maḥjūb). The witness, who has been granted [spiritual] opening (al-maftūḥ ʿalayh), acts with what he is permitted to do and does not act of his own accord; his action is by his Lord. He distances himself from his ego until no personal desire remains, and his action becomes divine, emanating from Allāh."
When Moulay ʿAbd al-Salām b. Mashīsh speaks to us and narrates these stations (maqāmāt) and these openings (futuḥāt) that allow understanding the value of the Messenger of Allāh (saws), they are the words and knowledge of someone who is witnessing. We noticed that the prayer of Sīdī Ibn Mashīsh is entirely composed of spiritual stations.
He (ra) began the prayer by saying: "O Allāh! Bless the one from whom secrets have emerged." The greatest secret for the Shaykh is the secret deposited in the heart of the master who guided him to Allāh. Moulay ʿAbd al-Salām had his master who trained him, taught him, and guided him to his Lord. This master cannot guide and make known unless he carries a secret among the secrets of the Messenger of Allāh (saws). Thus, when Shaykh ʿAbd al-Salām said: "O Allāh! Bless the one from whom secrets emerge," the first and greatest secret is the one deposited in the heart of his master. He began with his master, then described what emanated from the Messenger of Allāh (saws) in terms of secrets and lights. Then he spoke about the Messenger of Allāh (saws), about the very essence of the Messenger of Allāh (saws), the Muḥammadan essence: "O Allāh! He is Your encompassing secret that points to You, Your Supreme Veil standing before You."
When he stood before this great door, he stood with his master. The disciple never lets go of his master's hand, no matter the circumstance or situation. Regardless of the level reached by the disciple in his journey, he must keep his hand in that of his master. If he forgets the master who guided him to Allāh, supported him, and taught him, he becomes disobedient to the master.
No matter the opening granted to the disciple, what he sees, witnesses, or the degree he reaches, his hand must remain in that of his master. Here is an allusion from the Prophet (saws) during the night of Ascension: in that night when the Messenger of Allāh (saws) ascended to a place unreachable by any human or angel, to a station only the Master of existence, our master, the Messenger of Allāh (saws), could access. When he arrived, he heard the voice of Abū Bakr and said to his Lord: "Before reaching You, I heard someone calling with a voice similar to that of Abū Bakr..." Then He, the Exalted, said: "Since your intimacy is with your companion Abū Bakr and you were both created from the same essence, and he is your close companion in this world and the Hereafter, We created an angel in his image to call you with his voice." This station is not attained by Abū Bakr or anyone else, but Allāh knew that the Prophet (saws) loved his companion, so He wanted him to hear his voice. Even though our master the Prophet (saws) is the master of Abū Bakr, it was an allusion that the seeker does not forget his beloved in Allāh, who is his master whose only concern is to guide him to his Lord.
When the Shaykh reached the Muḥammadan Presence and named it "the Supreme Veil," meaning: the veil that indicates Allāh, standing at the gate of Allāh, or rather, it is itself (saws) the gate of Allāh. When he stood before this gate, the Shaykh did not stop at the gate for he wished to reach the sanctuary (miḥrāb), the Lord of Lords. He said: "Carry me on its path to Your Presence," addressing Allāh by saying: "O Lord! Carry me on the path of the Supreme Veil to Your Presence," meaning: lead me on the path that leads to You, but on the path of the Messenger of Allāh (saws), and under his protection and care.
Here, the Shaykh seeks Allāh; he seeks entry into the Presence but under the leadership, protection, and wing of the Messenger of Allāh (saws), the Supreme Veil. The Shaykh was not content with that but sought what lies beyond the veil, which is the Lord of Lords, exalted and glorified. Then he said: "And make the Supreme Veil the life of my spirit." When he said: "Carry me on its path to Your Presence," this means that the Shaykh entered the Presence under the leadership of the Messenger of Allāh (saws).
But to understand the Shaykh's intention here when he phrased this prayer in the form of a supplication, he was not asking for the unknown but for stations he was familiar with. How could he ask to be removed from the mire (awḥāl) of monotheism (tawḥīd) and immersed in the ocean of Oneness (aḥadiyyah), and be carried on the path of the Messenger of Allāh (saws) to the Presence of Allāh? This is therefore not a mere request or supplication, for the Shaykh only spoke of these stations because he knew and experienced them. He asked for them and expressed them in the form of a supplication out of respect for the station so as not to show that he had attained them, remaining in the station of servitude (ʿubudiyyah), the station of the supplicant, the seeker. All these stations mentioned by the Shaykh, he knew them, reached them, and fully understood them.
"""
    prompt = pre_prompt + f"Now translate this text from {source_lang} to {target_lang}: {text}. You should use this translation type : {translation_type}. Only output the translation."
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
