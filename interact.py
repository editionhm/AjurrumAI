import requests
import streamlit as st
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import csv
import pandas as pd


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
def generate_questions(selected_chapter, file_path, level_mastery):
    """
    Génère une série de questions-réponses basées sur le contenu du chapitre sélectionné
    et le niveau de l'utilisateur en utilisant la fonction generate_llm.

    Parameters:
    selected_chapter (str): Le titre du chapitre sélectionné.
    file_path (str): Le chemin vers le fichier CSV contenant les chapitres et leur contenu.
    level_mastery (str): Le niveau de l'utilisateur (Beginner, Intermediate, Advanced, Expert).

    Returns:
    list: Une liste de dictionnaires contenant des questions et leurs réponses.
    """
    chapter_content = None
    
    # Lire le fichier CSV et trouver le contenu du chapitre sélectionné
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row.get("Chapter") == selected_chapter:
                chapter_content = row.get("Content")  # Récupère le contenu de la colonne "Content"
                break

    if not chapter_content:
        return []

    # Préparer le prompt pour la génération des questions en fonction du niveau de l'utilisateur
    prompt = f"""
    You are an expert Arabic Grammar teacher. Create a series of questions and answers based on the following chapter content:
    {chapter_content}
    The questions should match the user's level: {level_mastery}.
    Generate questions of various types (e.g., fill-in-the-blank, true/false, and open-ended) that assess understanding at this level.
    Provide answers for each question. Write in both english and arabic.
    """

    # Utiliser la fonction generate_llm pour générer les questions-réponses
    response = generate_llm(prompt)

    return response


def generate_pairs(num_pairs):
    pairs = {}
    prompt = f"Generate exaclty {num_pairs} pairs of common Arabic phrase and its English translation. Output should be ONLY: 1. Arabic phrase | English translation
    2. Arabic phrase | English translation
    3. Arabic phrase | English translation
    etc.."
    result = generate_llm(prompt)
    pairs[result] = result
        # Parse the response assuming it returns a pair like "مرحبا | Hello"
        """try:
            arabic, english = result.split(" | ")
            english, arabic = english.strip(), arabic.strip()
            if english and arabic and english not in pairs:
                pairs[english] = arabic
                print(f"Added pair: {english} - {arabic}")
         """
    return pairs
