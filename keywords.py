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

  return list(orgs)

def call_ollama(content):
  ollama_url = "http://localhost:11434/api/generate"
  data = {
    "model": "llama2",
    "prompt": 
      f""" 
      Generate 3-5 relevant keywords for an article's general topic. What areas of interest does the article cover?
      Avoid repetition, and keep the keywords general. Use plural case if necessary.
      This is the article's summary: {content}.
      Answer ONLY with the keywords. Every keyword should be 1-2 words only.
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
    list = json.loads(input_string)
    return set(list) 
  
  lines = input_string.split('\n')

  # Remove empty lines and intro sentence
  cleaned_lines = [line.strip() for line in lines if line.strip() != '']
  cleaned_keywords = cleaned_lines[1:]

  # remove the numbering, in case it's there
  try: 
    cleaned_keywords = set(line.split('. ')[1] for line in cleaned_keywords)
  except:
    cleaned_keywords = set(cleaned_keywords)

  return cleaned_keywords # {str, str, ...}
