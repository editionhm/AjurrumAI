import requests
import streamlit as st
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import csv


url = st.secrets["URL"] 
token_iam = st.secrets["TOKEN"]
project_id = st.secrets["PROJECT_ID"]

def generate_llm(prompt):
    """
    Function to generate responses from the LLM
    """
    authenticator = IAMAuthenticator(token_iam)
    token = authenticator.token_manager.get_token()
    body = {
        "input": f"""[INST] {prompt} [/INST]""",

        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 2048,
            "repetition_penalty": 1
        },
        "model_id": "sdaia/allam-1-13b-instruct",
        "project_id": project_id
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",   
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    resultat = data['results'][0]['generated_text']
    return resultat


#####

def extract_chapters(file_path):
    chapters = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            chapter = row.get("Chapter")
            if chapter and chapter != "Chapter":  # Ignore empty or header-like values
                chapters.append(chapter.strip())  # Add the chapter name to the list
    return chapters

def extract_passage(file_path, chapter_value):
    """
    Extrait le contenu de la colonne "Passage" pour la ligne où la colonne "Chapter" correspond à chapter_value.
    
    :param file_path: Chemin vers le fichier CSV
    :param chapter_value: Valeur de la colonne "Chapter" pour laquelle on souhaite récupérer le passage
    :return: Le contenu de la colonne "Passage" si trouvé, sinon None
    """
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row.get("Chapter") == chapter_value:
                return row.get("Passage")  # Récupère le contenu de la colonne "Passage"
    return None

import pandas as pd

def generate_questions(selected_chapter, file_path):
    """
    Génère une série de questions-réponses basées sur le contenu du chapitre sélectionné.
    
    Parameters:
    selected_chapter (str): Le titre du chapitre sélectionné.
    file_path (str): Le chemin vers le fichier CSV contenant les chapitres et leur contenu.
    
    Returns:
    list: Une liste de dictionnaires contenant des questions et leurs réponses.
    """
    # Charger le fichier CSV
    df = pd.read_csv(file_path)
    
    # Trouver le contenu du chapitre sélectionné
    chapter_content = df[df['Chapter'] == selected_chapter]['Content'].values
    if len(chapter_content) == 0:
        return []

    chapter_content = chapter_content[0]
    
    # Générer des questions simples en utilisant des techniques basiques de NLP
    # Ici, nous créons des questions du type "Compléter la phrase" et "Vrai ou faux"
    questions = []

    # Exemple de découpage simple du contenu en phrases
    sentences = chapter_content.split('.')
    
    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Question de type "Compléter la phrase"
        if len(sentence.split()) > 5:
            words = sentence.split()
            blank_index = len(words) // 2  # Prend un mot au milieu de la phrase
            answer = words[blank_index]
            words[blank_index] = '_____'
            question = ' '.join(words)
            questions.append({"question": f"Complétez la phrase: {question}", "answer": answer})
        
        # Question de type "Vrai ou faux"
        if i % 2 == 0 and len(sentence) > 10:
            questions.append({"question": f"Vrai ou Faux: {sentence} ?", "answer": "Vrai"})
    
    return questions


