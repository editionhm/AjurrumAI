# 💬 Chatbot template

A chatbot using ALLaM model to learn everything about Arabic Grammar.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ajurrumai.streamlit.app/) 

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

### To Do lit

#### Datasets 
DPO when Fine-Tuning

1. Dataset I'rab :

AR_Text | Irab | Bad_Irab (API)

2. Dataset Questions/Réponses

Question | Answer | Bad_Answer (API)

3. Dataset AR/EN

Arabic | English 

4. Dataset Poem

AR_Text | AR_Poem

#### Agents

Implement "Iteration of Tought" (IoT) every agent.
Do RAG on chapters.

1. Agent Teacher (+Examinator)

- Write : "Hello, I am your Teacher. What would you like to discuss today ?"
- List of : Topics non-finished --> Courses non-finished --> Chapters non-finished
- Prompt : "Based on {Text_of_chapter}. Elaborate : objectives, explanation ...."

2. Agent Discussion
3. Agent Revision

#### Features
- User can choose to only write in Arabic OR in Arabic and English.
- User can choose the Agent Mode in a list (Teacher, Discussion, Revision)
- Implement "Box of Leitner" : (3,7,14,30 days)
  
