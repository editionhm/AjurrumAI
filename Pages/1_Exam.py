import streamlit as st
import json
from bson.objectid import ObjectId
import database
import interact  # Assurez-vous que ce module contient la fonction generate_llm(prompt)

# -------------------------------
# Page Examen
# -------------------------------
def page_examen():
    st.header("Examen / امتحان")

    # Vérifier si l'utilisateur est connecté
    if not st.session_state.user["connected"]:
        st.warning("Veuillez vous connecter pour accéder à la fonctionnalité d'examen. / الرجاء تسجيل الدخول للوصول إلى ميزة الامتحان.")
        return

    # Entrée pour sélectionner le chapitre
    chapitre = st.text_input("Entrez le chapitre à examiner : / أدخل الفصل المراد امتحانه:")

    # Bouton pour démarrer l'examen
    if st.button("Démarrer l'examen / بدء الامتحان"):
        if not chapitre.strip():
            st.error("Veuillez entrer un chapitre. / الرجاء إدخال فصل.")
        else:
            with st.spinner("Génération des questions de l'examen... / جارٍ توليد أسئلة الامتحان..."):
                questions = generer_questions_examen(chapitre, nombre_questions=5)
                if questions:
                    st.session_state['questions_examen'] = questions
                    st.session_state['reponses_utilisateur'] = {}
                    st.success("Questions de l'examen générées avec succès! / تم توليد أسئلة الامتحان بنجاح!")

    # Afficher les questions de l'examen si elles ont été générées
    if 'questions_examen' in st.session_state:
        questions = st.session_state['questions_examen']
        reponses_utilisateur = st.session_state.get('reponses_utilisateur', {})
        st.markdown(f"**Chapitre :** {chapitre}")
        st.markdown("### Répondez aux questions suivantes / أجب على الأسئلة التالية:")

        with st.form(key='form_examen'):
            for idx, q in enumerate(questions, 1):
                st.write(f"**Question {idx} : {q['question_text']}**")
                options = q['options']
                reponses_utilisateur[q['question_id']] = st.radio(
                    f"Choisissez une option pour la Question {idx} / اختر خيارًا للسؤال {idx}:",
                    options=["1", "2", "3", "4"],
                    format_func=lambda x: f"{x}. {options[int(x)-1]}",
                    key=f"examen_q_{q['question_id']}"
                )

            submit_examen = st.form_submit_button("Soumettre les réponses / إرسال الإجابات")

        if submit_examen:
            if not reponses_utilisateur:
                st.error("Veuillez répondre à toutes les questions. / الرجاء الإجابة على جميع الأسئلة.")
            else:
                with st.spinner("Correction de vos réponses... / جارٍ تصحيح إجاباتك..."):
                    reponses, score_pourcentage, reussi = corriger_reponses(questions, reponses_utilisateur)

                    # Enregistrer l'examen dans la base de données
                    examen_id = database.ajouter_examen(
                        user_id=st.session_state.user['username'],  # Supposant que le nom d'utilisateur est unique
                        chapitre=chapitre,
                        questions=[{"question_id": ObjectId(), "question_text": q['question_text']} for q in questions],
                        reponses=reponses,
                        score=int(score_pourcentage),
                        reussi=reussi
                    )

                    st.success(f"Examen soumis! / تم إرسال الامتحان! **Votre Score :** {score_pourcentage}%")
                    if reussi:
                        st.success("Félicitations! Vous avez réussi l'examen. / تهانينا! لقد نجحت في الامتحان.")
                    else:
                        st.warning("Vous n'avez pas réussi l'examen. Veuillez réessayer. / لم تنجح في الامتحان. يرجى المحاولة مرة أخرى.")

                    # Optionnellement, afficher les résultats détaillés
                    with st.expander("Voir les résultats détaillés / عرض النتائج التفصيلية"):
                        for idx, q in enumerate(questions, 1):
                            reponse = reponses[idx-1]
                            correct = "✅ Correct" if reponse['correct'] else "❌ Incorrect"
                            st.write(f"**Question {idx} : {q['question_text']}**")
                            st.write(f"**Votre Réponse :** {reponse['user_answer']}")
                            st.write(f"**Résultat :** {correct}")

# Fonction pour générer les questions de l'examen
def generer_questions_examen(chapitre, nombre_questions=5):
    prompt = f"""
    Génère {nombre_questions} questions à choix multiple pour le chapitre suivant. Chaque question doit avoir une réponse correcte et trois réponses incorrectes. Fournis les questions au format JSON avec la structure suivante :

    [
        {{
            "question_id": "<identifiant_unique>",
            "question_text": "<texte_de_la_question>",
            "options": ["<option1>", "<option2>", "<option3>", "<option4>"],
            "correct_option": "<numéro_option_correcte>"  # ex: "1", "2", "3", ou "4"
        }},
        ...
    ]
    """
    reponse = interact.generate_llm(prompt)
    try:
        questions = json.loads(reponse)
        # Valider la structure
        for q in questions:
            assert "question_id" in q
            assert "question_text" in q
            assert "options" in q and len(q["options"]) == 4
            assert "correct_option" in q and q["correct_option"] in ["1", "2", "3", "4"]
        return questions
    except (json.JSONDecodeError, AssertionError) as e:
        st.error("Échec de l'analyse des questions générées par l'IA. Veuillez réessayer. / فشل في تحليل الأسئلة من الذكاء الاصطناعي. يرجى المحاولة مرة أخرى.")
        return []

# Fonction pour corriger les réponses de l'utilisateur
def corriger_reponses(questions, reponses_utilisateur):
    reponses = []
    correct_count = 0
    total_questions = len(questions)

    for q in questions:
        q_id = q['question_id']
        question_text = q['question_text']
        option_correcte_num = q['correct_option']
        option_correcte = q['options'][int(option_correcte_num)-1]
        option_utilisateur_num = reponses_utilisateur.get(q_id, "")
        option_utilisateur = q['options'][int(option_utilisateur_num)-1] if option_utilisateur_num.isdigit() and 1 <= int(option_utilisateur_num) <=4 else ""

        # Déterminer la justesse
        est_correct = (option_utilisateur_num == option_correcte_num)

        if est_correct:
            correct_count += 1

        reponses.append({
            "question_id": ObjectId(),
            "user_answer": option_utilisateur,
            "correct": est_correct
        })

    # Calculer le pourcentage de score
    score_pourcentage = (correct_count / total_questions) * 100
    reussi = score_pourcentage >= 70  # Seuil de réussite à 70%

    return reponses, score_pourcentage, reussi

# Exécuter la page examen
page_examen()
