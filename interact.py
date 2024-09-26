from ibm_wastonx_ai import *

def generate_llm(prompt):
    """
    Function to generate responses from the LLM
    """
    authenticator = IAMAuthenticator('GjztbmXZwtS4jEzjvrL8J9JuS8pPi-ulDQ2JhzPrtZst')
    token = authenticator.token_manager.get_token()
    body = {
        "input": f"""[INST] {prompt} [/INST]""",

        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 1536,
            "repetition_penalty": 1
        },
        "model_id": "sdaia/allam-1-13b-instruct",
        "project_id": "cb0d224c-3a53-4fec-ab52-a5f3dd088ba2"
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
