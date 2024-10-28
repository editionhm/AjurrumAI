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
            "max_new_tokens": 1536,
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
            if chapter:  # Ensure there's a value in the "Chapter" column
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

