import requests
import json

def get_keywords(summary):
  keywords = call_ollama(summary)
  keywords = clean_keywords(keywords)
  return keywords

def call_ollama(content):
  ollama_url = "http://localhost:11434/api/generate"
  data = {
    "model": "llama2",
    "prompt": f"""Generate 5 relevant keywords for an article. Answer only with the keywords!
    Do not make them too specific (e.g. 'Consumer protection' instead of 'Telephone Consumer Protection Act (TCPA)')
    This is the article's summary: {content}. 
    """,
    "stream": False
  }
  data_json = json.dumps(data)
  response = requests.post(ollama_url, data=data_json, headers={"Content-Type": "application/json"})

  if response.status_code == 200:
    data = response.json()
    return data['response']
  else:
    print(f"Request failed with status code: {response.status_code}")
    return None

def clean_keywords(input_string):
  lines = input_string.split('\n')

  # Remove empty lines and intro sentence
  cleaned_lines = [line.strip() for line in lines if line.strip() != '']
  cleaned_keywords = cleaned_lines[1:]

  # Remove the numbering
  cleaned_keywords = [line.split('. ')[1] for line in cleaned_keywords]

  return cleaned_keywords # [str, str, ...]
