import spacy
import requests
import json

# Load the English model for named entity recognition
nlp = spacy.load("en_core_web_sm")

def get_keywords(summary):
  keywords = call_ollama(summary)
  keywords = clean_keywords(keywords)
  return keywords

def get_orgs(content):
  orgs = set()
  doc = nlp(content)
  named_entities = [(entity.text, entity.label_) for entity in doc.ents]
  for entity, label in named_entities:
    if label == 'ORG':
      orgs.add(entity)

  return list(orgs) if len(orgs) > 1 else None

def call_ollama(content):
  ollama_url = "http://localhost:11434/api/generate"
  data = {
    "model": "llama2",
    "prompt": 
      f""" 
      Generate 3-5 relevant keywords for an article's topic. Answer ONLY with a list of keywords. Example: [str, str, ...]
      Make them general. For example:
      Bad response: ["HTML microframework", "modular web user interfaces", "vanilla HTML code", "page fragments", "content replacement"]
      Good response: ["code minimalism", "microframeworks", "vanilla HTML", "modular interfaces"]
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
  if input_string.startswith('['):
    return json.loads(input_string)
  
  lines = input_string.split('\n')

  # Remove empty lines and intro sentence
  cleaned_lines = [line.strip() for line in lines if line.strip() != '']
  cleaned_keywords = cleaned_lines[1:]

  # Remove the numbering
  cleaned_keywords = [line.split('. ')[1] for line in cleaned_keywords]

  return cleaned_keywords # [str, str, ...]
