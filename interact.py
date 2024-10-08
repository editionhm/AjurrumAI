import requests
import streamlit as st
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

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
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("Chapter"):
                chapters.append(line.strip())  # Add the chapter line to the list
    return chapters
