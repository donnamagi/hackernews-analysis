import requests
from bs4 import BeautifulSoup
import re
import json

def clean_text(text):
  """Remove extra spaces, newlines, and any script/style elements."""
  text = re.sub('\s+', ' ', text)
  text = re.sub('\n', ' ', text)
  return text.strip()

def set_description(soup : BeautifulSoup):
  description = ''
  meta_description = soup.find('meta', attrs={'name': 'description'})
  og_description = soup.find('meta', attrs={'property': 'og:description'})
  if meta_description:
    description = meta_description.get('content', '')
  elif og_description:
    description = og_description.get('content', '')
  
  return description

def set_body(soup : BeautifulSoup):
  paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
  paragraph_text = ' '.join(paragraphs)
  return paragraph_text[:2000]

def scrape_content(url):
  content = requests.get(url)
  if content.status_code == 200:
    soup = BeautifulSoup(content.text, 'html.parser')
    # title = soup.find('title').get_text() if soup.find('title') else ''

    description = set_description(soup)
    body = set_body(soup)
    summary = description + clean_text(body)

    return summary
  else:
    print(f"Error fetching content: {content.status_code}")

def call_ollama(content):
  ollama_url = "http://localhost:11434/api/generate"
  data = {
    "model": "llama2",
    "prompt": f"Summarize the text in 2-3 sentences. Be precise, no introduction needed: {content}",
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

def main(data):
  return scrape_content(data)
