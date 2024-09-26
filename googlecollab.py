# Step 1: Retrieve User Data

def get_unmastered_topics_and_courses(user_id):
    """
    Fetch unmastered topics and courses for the user from MongoDB.
    """
    client = MongoClient(CONNECTION_STRING)
    db = client[DB_NAME]
    user = db.users.find_one({"_id": user_id})
    
    if not user:
      st.error("User not found.")
      return [], []
    
    unmastered_topics = [topic for topic in user.get('topics', []) if not topic.get('mastery', False)]
    unmastered_courses = [course for course in user.get('courses', []) if not course.get('mastery', False)]    
    
    client.close()
    return unmastered_topics, unmastered_courses


def get_courses_for_topic(user_id, topic_id):
    """
    Fetch courses under a specific topic that are not mastered.
    """
    client = MongoClient(CONNECTION_STRING)
    db = client[DB_NAME]
    user = db.users.find_one({"_id": user_id})
    
    if not user:
        st.error("User not found.")
        return []
    
    # Assuming each course has a 'topic_id' field
    courses = [course for course in user.get('courses', []) if course.get('topic_id') == topic_id and not course.get('mastery', False)]
    
    client.close()
    return courses

def get_lessons_for_course(user_id, course_id):
    """
    Fetch lessons under a specific course that are not mastered.
    """
    client = MongoClient(CONNECTION_STRING)
    db = client[DB_NAME]
    user = db.users.find_one({"_id": user_id})
    
    if not user:
        st.error("User not found.")
        return []
    
    # Assuming each lesson has a 'course_id' field
    lessons = [lesson for lesson in user.get('lessons', []) if lesson.get('course_id') == course_id and not lesson.get('mastery', False)]
    
    client.close()
    return lessons


# Step 3: Generate Lesson Plan

prompt_teacher = f"""You are an expert teacher. 
Explain the objectives of the lesson in simple terms.
Elaborate on this section in an engaging and understandable manner step-by-step.

Chapter Title: {chapter_title}
Content Summary: {chapter_content}

Format the lesson plan in a clear, organized manner.

Here is an example of the output :

Lesson Plan: Understanding Speech and its Types

Objectives:
1. Define speech in both linguistic and grammatical senses.
2. Identify the four traits of speech in the grammatical sense.
3. Understand the difference between speech and utterance.
4. Recognize examples of comprehensible and non-comprehensible speech.
5. Appreciate the importance of Arabic language in speech.

Section 1: Speech in Linguistic Sense
Explain that speech in the linguistic sense refers to any expression that brings forth benefit, regardless of whether it is verbalized or not (e.g., scripting, writing, or gesticulation).

Section 2: Speech in Grammatical Sense
Discuss the four traits of speech in the grammatical sense: (i) it must be an oral utterance, (ii) it must be compound, (iii) it must be comprehensible, and (iv) it must be established in the medium of the Arabic language.

Section 3: Understanding Utterance
Explain that utterance refers to an oral sound formed from the Arabic alphabet, starting with alif and ending with yā. Provide examples of utterances and discuss why gesticulation is not considered speech according to grammarians.

Section 4: Understanding Compound Speech
Explain that compound speech must be composed of two words or more. Provide examples of compound speech and discuss why a singular word is not considered speech until it is connected to another word.

Section 5: Comprehensible Speech
Explain that comprehensible speech is understood by the listener without requiring further explanation. Provide examples of comprehensible and non-comprehensible speech.

Section 6: Importance of Arabic Language
Discuss the importance of using the same lexicon that Arabs use to communicate in order to convey a message. Provide examples of words used by Arabs and those from other languages.
"""

def create_lesson_plan(chapter_title, chapter_content):
    """
    Generate a lesson plan using the LLM.
    """
    prompt = prompt_teacher
    return generate_llm(prompt)


print(create_lesson_plan(chapter_title,chapter_content))


def generate_subchapter_explanation(chapter_title, subchapter):
    """
    Generate an explanation for a subchapter using the LLM.
    """
    prompt = f""" You are an expert teacher. Elaborate on the following subchapter in an engaging and understandable manner.

Chapter Title: {chapter_title}
Subchapter: {subchapter}

Provide a clear explanation with examples if necessary.
"""
    return generate_llm(prompt)



# Step 5 : Examinator

## AJOUTER DES EXEMPLES

def create_assessment(chapter_title, chapter_content):
    prompt = f""" You are an exam creator. Generate a set of maximum 10 questions to assess the student's understanding of the following lesson.

Lesson Title: {chapter_title}
Content Summary: {chapter_content}

Ensure the questions cover all the objectives.

Here is an example of the expected output: 

Question 1: What is the definition of speech in the linguistic sense according to the lesson?

Question 2: What are the four traits that speech must possess in the grammatical sense?

Question 3: Why is a singular word not considered speech according to the grammarians? Provide an example.

Question 4: What is the meaning of "something which is comprehendible" in the context of speech? Provide an example.

Question 5: Why is it essential for speech to be established in the medium of the Arabic language? Provide an example of a non-Arabic language word that would not be considered speech.

Question 6: List three examples of speech that fulfill the conditions mentioned in the lesson.

Question 7: Provide two examples of singular words that are not considered speech.

Question 8: What are two examples of compound statements that are not comprehensible? Explain why they do not meet the comprehensibility requirement. 
"""
    return generate_llm(prompt)

print(create_assessment(chapter_title, chapter_content))



# Step 6 Verify Answer

## AJOUTER DES EXEMPLES


def verify_answers(chapter_content, question, answer):
    """
    Verify a single answer using the LLM.
    """
    qa_text = "\n".join([f"{i+1}. Q: {qa['question']}\n   A: {qa['answer']}" for i, qa in enumerate(exam_qas)])
    prompt = f""" You are an expert evaluator. Assess the following answers to the exam questions based on the lesson content provided.

Lesson Content : {chapter_content}

Question :{question}
Answer: {answer}

Provide a detailed evaluation of each answer, indicating whether it is correct or incorrect. Summarize the overall performance and state whether the student has demonstrated mastery of the chapter.
"""
    return generate_llm(prompt)



# Step 7 Update Mastery

def update_mastery(user_id, course_id, chapter_id):
    """
    Update the mastery status of a lesson in MongoDB.
    """
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    db.users.update_one(
        {"_id": user_id, "courses.course_id": course_id, "lessons.lesson_id": lesson_id},
        {"$set": {"courses.$.lessons.$[lesson].mastery": True}},
        array_filters=[{"lesson.lesson_id": lesson_id}]
    )
    client.close()
