import requests
import streamlit as st
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import csv
import pandas as pd
import os
from ibm_watson_machine_learning import APIClient
#base
url_base = st.secrets["URL_2"] 
project_id_base = st.secrets["PROJECT_ID"]
token_iam_base = st.secrets["TOKEN_2"]

#fine_tuned
access_token = st.secrets['TOKEN']
deploy_url = "https://ai.deem.sa/ml/v1/deployments/5041749e-8c92-46a7-b625-276ffb5c53f3/text/generation?version=2021-05-01"
deploy_id  = "5041749e-8c92-46a7-b625-276ffb5c53f3"
project_id = "74cc6740-c372-4851-ba31-db8af6f7bc0a"

wml_credentials = {
                   "url": "https://ai.deem.sa/",
                   "token": access_token,
                   "instance_id": "openshift",
                   "version": "5.0"
                  }
client = APIClient(wml_credentials)

def generate_word(prompt):
    full_input = f"{prompt}"
    scoring_payload = {
        "input": full_input,
        "parameters": {
            "decoding_method" : "sample",
            "max_new_tokens": 30,
            "temperature": 0.8,
            "top_k": 30,
            "top_p": 0.8,
            "repetition_penalty": 1
        }
    }


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(deploy_url, headers=headers, json=scoring_payload)
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    resultat = data['results'][0]['generated_text']
    return resultat
  
def generate_llm_fine_tune(prompt):
    full_input = f"{prompt}" #f"[INST] {prompt} [/INST]"
    scoring_payload = {
        "input": full_input,
        "parameters": {
            "decoding_method" : "greedy",
            "max_new_tokens": 2047,
            "min_new_tokens" : 0,
            "repetition_penalty": 1
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(deploy_url, headers=headers, json=scoring_payload)
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    resultat = data['results'][0]['generated_text']
    return resultat


def generate_llm(prompt):
    """
    Function to generate responses from the LLM
    """

    authenticator = IAMAuthenticator(token_iam_base)
    token = authenticator.token_manager.get_token()
    body = {
        "input": f"""[INST] {prompt} [/INST]""",

        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 2048,
            "repetition_penalty": 1
        },
        "model_id": "sdaia/allam-1-13b-instruct",
        "project_id": project_id_base
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",   
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url_base, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()
    resultat = data['results'][0]['generated_text']
    return resultat

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


def generate_pairs(num_pairs=10):
    """
    Generate English-Arabic word/phrase pairs using the LLM.

    Parameters:
        num_pairs (int): Number of pairs to generate. Default is 10.

    Returns:
        Dict[str, str]: A dictionary where each key is an English phrase and each value is its Arabic translation.
    """
    pairs = {}
    
    # Prompt the LLM to return multiple pairs at once in the expected format
    prompt = f"""Generate exaclty {num_pairs} pairs of common Arabic phrase and its English translation. Output should be ONLY: 1. Arabic phrase | English translation
    2. Arabic phrase | English translation
    3. Arabic phrase | English translation
    etc.."""
    result = generate_llm(prompt)
    
    # Split the response into lines and process each line
    for line in result.splitlines():
        line = line.strip()  # Remove any leading/trailing whitespace
        if not line:
            continue  # Skip empty lines

        # Parse each line to extract the Arabic and English phrases
        try:
            # Remove the numbering if present, e.g., "1. "
            if '. ' in line:
                _, line = line.split('. ', 1)
            
            # Split the line by the "|" character to separate Arabic and English
            arabic, english = line.split(" | ")
            english, arabic = english.strip(), arabic.strip()  # Remove any extra spaces

            # Add the pair to the dictionary if it's unique
            if english and arabic and english not in pairs:
                pairs[english] = arabic
        except ValueError:
            print(f"Unexpected format in line: {line}")

    return pairs
