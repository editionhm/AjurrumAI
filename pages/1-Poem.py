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
        "Basit | البسيط",
        "Sari' | السريع",

    ],
)

length_poem = st.select_slider(
    "Select the lenght of your poem",
    options=[
        "3",
        "5",
        "10",
        "15"
    ],
)


# Fonction pour générer le prompt en fonction du type de poème
def create_prompt(text, poem_style):
    if poem_style == "Rajaz | الرجز":
        prompt = f"""Please create a poem in arabic preserving the rules of arabic poetry that contains what is in this content {text}.

For example, here is an example of an Arabic text:
وَهُوَ عَلَى أَرْبَعَةِ أَقْسَامٍ بَدَلُ اَلشَّيْءِ مِنْ اَلشَّيْءِ، وَبَدَلُ اَلْبَعْضِ مِنْ اَلْكُلِّ، وَبَدَلُ اَلِاشْتِمَالِ، وَبَدَلُ اَلْغَلَطِ.
Nَحْوَ قَوْلِكَ "قَامَ زَيْدٌ أَخُوكَ، وَأَكَلْتُ اَلرَّغِيفَ ثُلُثَهُ، وَنَفَعَنِي زَيْدٌ عِلْمُهُ، وَرَأَيْتُ زَيْدًا اَلْفَرَسَ"، أَرَدْتَ أَنْ تَقُولَ رَأَيْتُ اَلْفَرَسَ فَغَلِطْتَ فَأَبْدَلْتَ زَيْدًا مِنْه.ُ

Here’s a version of this text rephrased in the rhythmic 'Rajaz' poetry style:
أَقْسَامُهُ أَرْبَعَةٌ فَإِنْ تُرِدْ *** إِحْصَاءَهَا فَاسْمَعْ لِقَولِي تَسْتَفِدْ
\n
فَبَدَلُ الشَّيءِ مِنَ الشَّيءِ كَجَا *** زَيدٌ أَخُوكَ ذَا سُرُورٍ بَهِجَا
\n
وَبَدَلُ البَعْضِ مِنَ الكُلِّ كَمَنْ *** يَأْكُلْ رَغِيْفًا نِصْفَهُ يُعْطِ الثَّمَنْ
\n
وَبَدَلُ اشْتِمَالٍ نَحْوُ رَاقَنِي *** مُحَمَّدٌ جَمَالُهُ فَشَاقَنِي
\n
وَبَدَلُ الغَلَطِ نَحْوُ قَدْ رَكِبْ *** زَيدٌ حِمَارًا فَرَسًا يَبْغِي اللَّعِبْ

Remember the instruction is : Please create a poem in arabic preserving the rules of arabic poetry that contains what is in this content {text}. Output should write each verse on one line""" 
    elif poem_style == "Basit | البسيط":
        prompt = f""" Create an Arabic poem in 'Basit' meter with smooth, balanced verses based on the theme: {text}. I will show you examples of text transformed in a Basit poem : 

Here is an example of arabic text : 
وأما الاجتهاد فهو بذل الوسع في بلوغ الغرض، فالمجتهد إن كان كامل الآلة في الاجتهاد، فإن اجتهد في الفروع فأصاب فله أجران، وإن اجتهد فيها وأخطأ فله أجر . 
ومنهم من قال: كل مجتهد في الفروع مصيب . 
ولا يجوز أن يقال: كل مجتهد في الأصول الكلامية مصيب، لأن ذلك يؤدي إلى تصويب أهل الضلالة من النصارى والمجوس والكفار والملحدين . 
ودليل من قال: ليس كل مجتهد في الفروع مصيباً، قوله صلى الله عليه وآله وسلم: (( من اجتهد وأصاب فله أجران، ومن اجتهد وأخطأ فله أجر واحد )) . 
وجه الدليل أن النبي صلى الله عليه وآله وسلم خطأ المجتهد وصوبه أخرى . 

And now here is a of this text versified in arabic in the style “Basit” : 
"والاجتهادُ لِبذلِ الوُسعِ في غَرَضٍ *** وُسْعُ الفقيهِ لظنِّ الحكمِ مبذولُ
وذو اجتهادٍ متى تَكمُلْ أدلّتُهُ *** إذا أصابَ فللأجرينِ تكميلُ
وقال قومٌ: مصيبٌ كلُّ مجتهدٍ *** في الفرعِ، فادْرُسْ، فَرَوْضُ العلمِ مخضولُ
لا في أصول كلامٍ، إذ يجرُّ إلى *** تصويبِ قولٍ به كفرٌ وتضليلُ
دليلُ نافيه ما قد جاء في خَبَرٍ *** رَوَوْهُ عمَّن به تُشْفَى العقابيلُ
إذْ كان خطَّأه طورًا، وصوَّبَه *** طورًا، وقد تمَّ للمقصودِ تكميلُ"
 
Here is another example of arabic text : 
والتقليد قبول قول القائل بلا حجة، فعلى هذا قبول قول النبي صلى الله عليه وآله وسلم يسمى تقليداً . 
ومنهم من قال: التقليد قبول قول القائل وأنت لا تدري من أين قاله، فإن قلنا: إن النبي صلى الله عليه وآله وسلم كان يقول بالقياس، فيجوز أن يسمى قبول قوله تقليداً . 

And now here is a of this text versified in arabic in the style “Basit” : 
"قَبولُ قولٍ بلا علمٍ بمأخذِهِ *** حدٌّ لَدَى الغُرِّ للتَّقليدِ مقبولُ
والاقتدا برسولِ اللهِ يَربَأُ عن *** هذا المقامِ به وحيٌ وتنزيلُ
ولو فَرَضْنَا اجتهادَ المصطفى فكفى *** به دليلًا، وما في الأصلِ تطويلُ"

Here is another example of arabic text : 
وأما القياس فهو رد الفرع إلى الأصل بعلة تجمعهما في الحكم . 
وهو ينقسم إلى ثلاثة أقسام: إلى قياس علة، وقياس دلالة، وقياس شبه . 
فقياس العلة ما كانت العلة فيه موجبة الحكم . 
وقياس الدلالة هو الاستدلال بأحد النظرين على الآخر، وهو أن تكون العلة دالة على الحكم ولا تكون موجبة للحكم . 
وقياس الشبه هو الفرع المتردد بين أصلين، فيلحق بأكثرهما شبهاً . 
ومن شرط الفرع أن يكون مناسباً للأصل، ومن شرط الأصل أن يكون ثابتاً بدليل متفق عليه بين الخصمين . 
ومن شرط العلة أن تطرد في معلولاتها، فلا تنتقض لفظاً ولا معنى . 
ومن شرط الحكم أن يكون مثل العلة في النفي والإثبات . 
والعلة هي الجالبة، والحكم هو المجلوب للعلة . 

And now here is a of this text versified in arabic in the style “Basit” : 
"أَمَّا القياسُ فَرَدُّ الفرعِ فادْرِ إلى *** أصلٍ يَضُمُّهُما في الحكمِ تَعلِيلُ
فمنْه ذو عِلَّةٍ، ومنه ذو شَبَهٍ *** وذو الدَّلالةِ أنواعٌ أبابيلُ
مَا كان عِلَّتُهُ للحكمِ مُوجِبةً *** ذو عِلَّةٍ، بل لِعَيْنِ اللَّفظِ مدلولُ
وذو الدَّلالةِ ما دلَّ النَّظيرُ به *** على النظِيرِ ولم يُوجِبْه تعليلُ
وما تجاذَبَه أصْلانِ ذو شَبَهٍ *** كالعبدِ يُشبِهُ مالا وهْوَ مقتولُ
وشرطُ أصلٍ ثبوتٌ بالدليلِ بما *** عليهِ في نَظَرِ الخصمَيْن تعويلُ
وعلَّةُ الحكمِ في معلولِهَا اطَّرَدَتْ *** لفظًا ومعنًى، فما بالنَّقضِ تعطيلُ
والحكمُ نفيًا وإثباتًا كَعلَّتِهِ  *** إن تُنفَ أو تُلْفَ يَجْرِي ما جَرَى النَّيلُ

Analyse how between "***" the last word has always the same sound. And analyze how between each "***" the structure of the phrase is.
"""

    elif poem_style == "Sari' | السريع":
        prompt = f"""Create an Arabic poem in 'Sari'' meter with smooth, balanced verses based on the theme: {text}. I will show you examples of text transformed in a Sari' poem : 
Here is an example of arabic text : 
وَلِلْخَفْضِ ثَلَاثُ عَلَامَاتٍ:
فَأَمَّا الْكَسْرَةُ: فَتَكُونُ عَلَامَةً لِلْخَفْضِ فِي ثَلَاثَةِ مَوَاضِعَ: فِي الْاِسْمِ الْمُفْرَدِ الْمُنْصَرِفِ، وَجَمْعِ التَّكْسِيرِ الْمُنْصَرِفِ، وَفِي جَمْعِ الْمُؤَنَّثِ السَّالِمِ.
وَأَمَّا الْيَاءُ: فَتَكُونُ عَلَامَةً لِلْخَفْضِ فِي ثَلَاثَةِ مَوَاضِعَ: فِي الْأَسْمَاءِ الْخَمْسَةِ، وَفِي التَّثْنِيَةِ، وَالْجَمْعِ.
وَأَمَّا الْفَتْحَةُ: فَتَكُونُ عَلَامَةً لِلْخَفْضِ فِي الْاِسْمِ الَّذِي لَا يَنْصَرِفُ.

And now here is a of this text versified in arabic in the style “Sari” : 
علامة الخفض ثلاث تعتبر *** کسر وفتحة وياء تستطر
فالكسر للخفض علامة عرف *** في مفرد وجمع تكسير صرف
وجمع تأنيث صحيح المفرد *** نحو عن الهندات فاعرض تنجد
والياء في المثنى والجمع الصحيح *** وخمسة الاسماء لخفضها تبيح
والفتح للخفض علامة وضع *** فيما من الاسماء صرفه منع

Here is another example of arabic text : 
اَلْمُعْرَبَاتُ قِسْمَانِ قِسْمٌ يُعْرَبُ بِالْحَرَكَاتِ، وَقِسْمٌ يُعْرَبُ بِالْحُرُوفِ
فَاَلَّذِي يُعْرَبُ بِالْحَرَكَاتِ أَرْبَعَةُ أَنْوَاعٍ اَلِاسْمُ اَلْمُفْرَدُ، وَجَمْعُ اَلتَّكْسِيرِ، وَجَمْعُ اَلْمُؤَنَّثِ اَلسَّالِمِ، وَالْفِعْلُ اَلْمُضَارِعُ اَلَّذِي لَمْ يَتَّصِلْ بِآخِرِهِ شَيْءٌ.
وَالْفِعْلُ اَلْمُضَارِعُ اَلَّذِي لَمْ يَتَّصِلْ بِآخِرِهِ شَيْءٌ.
وَكُلُّها تُرفَعُ بِالضَّمَّةِ، وتُنصَبُ بالفَتْحَةِ، وتُخْفَضُ بِالكَسْرَةِ، وتُجْزَمُ بالسُّكُونِ.
وخَرَجَ عَنْ ذلكَ ثَلاثَةُ أَشْيَاءَ: جَمْعُ المُؤنَّثِ السَّالمُ يُنصَبُ بالكَسْرَةِ، والِاسْمُ الَّذِي لا يَنْصِرفُ يُخْفَضُ بِالفَتْحَةِ، والفِعْلُ المُضَارِعُ الْمُعْتَلُّ الآخِرِ يُجْزَمُ بِحَذْفِ آخِرِهِ.

And now here is a of this text versified in arabic in the style “Sari’” : 
قسمين جا في الاصطلاح المعرب *** فأول بالحركات يعرب
مفرد الاسماء وجمع کسرا ***  وجمع سالم مؤنث يرى
كذا المضارع الذي لم ينقل ***  بلامه شئ كيعطى ويصل
ورفع كلها بضمة يرى ***  ونصبه ايضا بفتحة جرى
والخفض بالكسر وجزمه اتی *** بما سكون فادر هذا المثبتا
واستثن جمعا سالما مؤنثا *** فنصبه بكسرة تشبثا
واسما لشبه الفعل لا ينصرف *** ختمه بالفتح حتما يعرف
كذا المضارع المعل الاخر ***  فجزمه بالحذف عندهم دری

Analyse how between "***" the last word has always the same sound. And analyze how between each "***" the structure of the phrase is.
"""
    else:
        prompt = f"Generate a poem based on the theme: {text}"
    return prompt

# Bouton pour générer le poème
if st.button("Generate Poem | ولّد القصيدة"):
    if arabic_text:
        # Créer le prompt en fonction du type de poème
        prompt = create_prompt(arabic_text, poem_type)
        # Appeler la fonction generate_llm pour créer le poème
        prompt += f"""The poem should not exceed {length_poem} verses. Always analyse how a poem is 2 hemistichs, the sound of the end of the first is the same as the end of the second one. Analyse and remember everything in examples i gave you to make a poem with the same aspect and rules. Output will be like 
واسما لشبه الفعل لا ينصرف *** ختمه بالفتح حتما يعرف
كذا المضارع المعل الاخر ***  فجزمه بالحذف عندهم دری"""
        poem = generate_llm(prompt)
        
        # Afficher le poème généré
        with st.chat_message("assistant"):
            st.write(poem)
    else:
        st.warning("Please enter text in Arabic to generate a poem | يرجى إدخال نص بالعربية لتوليد القصيدة.")
