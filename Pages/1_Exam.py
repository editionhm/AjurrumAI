import streamlit as st
import json
from bson.objectid import ObjectId
import database
import interact  # Ensure interact.py has the necessary functions

# -------------------------------
# Exam Page
# -------------------------------
def exam_page():
    st.header("Exam / امتحان")

    # Ensure the user is logged in
    if not st.session_state.user["connected"]:
        st.warning("Please log in to access the Exam feature. / الرجاء تسجيل الدخول للوصول إلى ميزة الامتحان.")
        return

    # Input for selecting the chapter
    chapter = st.text_input("Enter the chapter to be examined: / أدخل الفصل المراد امتحانه:")

    # Button to start the exam
    if st.button("Start Exam / بدء الامتحان"):
        if not chapter.strip():
            st.error("Please enter a chapter. / الرجاء إدخال فصل.")
        else:
            with st.spinner("Generating exam questions... / جارٍ توليد أسئلة الامتحان..."):
                questions = generate_exam_questions(chapter, num_questions=5)
                if questions:
                    st.session_state['exam_questions'] = questions
                    st.session_state['user_answers'] = {}
                    st.success("Exam questions generated successfully! / تم توليد أسئلة الامتحان بنجاح!")

    # Display exam questions if generated
    if 'exam_questions' in st.session_state:
        questions = st.session_state['exam_questions']
        user_answers = st.session_state.get('user_answers', {})
        st.markdown(f"**Chapter:** {chapter}")
        st.markdown("### Answer the following questions / أجب على الأسئلة التالية:")

        with st.form(key='exam_form'):
            for idx, q in enumerate(questions, 1):
                st.write(f"**Question {idx}: {q['question_text']}**")
                options = q['options']
                user_answers[q['question_id']] = st.radio(
                    f"Choose an option for Question {idx} / اختر خيارًا للسؤال {idx}:",
                    options=["1", "2", "3", "4"],
                    format_func=lambda x: f"{x}. {options[int(x)-1]}",
                    key=f"exam_q_{q['question_id']}"
                )

            submit_exam = st.form_submit_button("Submit Answers / إرسال الإجابات")

        if submit_exam:
            if not user_answers:
                st.error("Please answer all questions. / الرجاء الإجابة على جميع الأسئلة.")
            else:
                with st.spinner("Grading your answers... / جارٍ تصحيح إجاباتك..."):
                    responses, score_percentage, passed = grade_answers(questions, user_answers)

                    # Store the exam in the database
                    exam_id = database.add_exam(
                        user_id=st.session_state.user['username'],  # Assuming username is unique
                        chapter=chapter,
                        questions=[{"question_id": ObjectId(), "question_text": q['question_text']} for q in questions],
                        responses=responses,
                        score=int(score_percentage),
                        passed=passed
                    )

                    st.success(f"Exam Submitted! / تم إرسال الامتحان! **Your Score:** {score_percentage}%")
                    if passed:
                        st.success("Congratulations! You have passed the exam. / تهانينا! لقد نجحت في الامتحان.")
                    else:
                        st.warning("You did not pass the exam. Please try again. / لم تنجح في الامتحان. يرجى المحاولة مرة أخرى.")

                    # Optionally, display detailed results
                    with st.expander("View Detailed Results / عرض النتائج التفصيلية"):
                        for idx, q in enumerate(questions, 1):
                            response = responses[idx-1]
                            correctness = "✅ Correct" if response['correct'] else "❌ Incorrect"
                            st.write(f"**Question {idx}: {q['question_text']}**")
                            st.write(f"**Your Answer:** {response['user_answer']}")
                            st.write(f"**Result:** {correctness}")

# Function to generate exam questions
def generate_exam_questions(chapter, num_questions=5):
    prompt = f"""
    Generate {num_questions} multiple-choice questions for the following chapter. Each question should have one correct answer and three incorrect answers. Provide the questions in JSON format with the following structure:

    [
        {{
            "question_id": "<unique_identifier>",
            "question_text": "<question_text>",
            "options": ["<option1>", "<option2>", "<option3>", "<option4>"],
            "correct_option": "<option_number>"  # e.g., "1", "2", "3", or "4"
        }},
        ...
    ]
    """
    response = interact.generate_llm(prompt)
    try:
        questions = json.loads(response)
        # Validate the structure
        for q in questions:
            assert "question_id" in q
            assert "question_text" in q
            assert "options" in q and len(q["options"]) == 4
            assert "correct_option" in q and q["correct_option"] in ["1", "2", "3", "4"]
        return questions
    except (json.JSONDecodeError, AssertionError) as e:
        st.error("Failed to parse questions from AI. Please try again. / فشل في تحليل الأسئلة من الذكاء الاصطناعي. يرجى المحاولة مرة أخرى.")
        return []

# Function to grade user answers
def grade_answers(questions, user_answers):
    responses = []
    correct_count = 0
    total_questions = len(questions)

    for q in questions:
        q_id = q['question_id']
        question_text = q['question_text']
        correct_option_num = q['correct_option']
        correct_option = q['options'][int(correct_option_num)-1]
        user_option_num = user_answers.get(q_id, "")
        user_option = q['options'][int(user_option_num)-1] if user_option_num.isdigit() and 1 <= int(user_option_num) <=4 else ""

        # Determine correctness
        is_correct = (user_option_num == correct_option_num)

        if is_correct:
            correct_count += 1

        responses.append({
            "question_id": ObjectId(),
            "user_answer": user_option,
            "correct": is_correct
        })

    # Calculate score percentage
    score_percentage = (correct_count / total_questions) * 100
    passed = score_percentage >= 70  # Define pass threshold as 70%

    return responses, score_percentage, passed

# Run the exam page
exam_page()
