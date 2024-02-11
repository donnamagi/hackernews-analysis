import requests
from bs4 import BeautifulSoup
import re
import pprint
import json

def clean_text(text):
  """Remove extra spaces, newlines, and any script/style elements."""
  text = re.sub('\s+', ' ', text)
  return text.strip()

def summarize_text(text, max_chars=2000):
  """Summarize the text to the first N characters."""
  return text[:max_chars]

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

def call_ollama(content):
  ollama_url = "http://localhost:11434/api/generate"
  data = {
    "model": "llama2",
    "prompt": f"Summarize this text. Stay precise, remove all noise: {content}",
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

url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'

response = requests.get(url)
if response.status_code == 200:
  top_stories = response.json()
else:
  print(f"Error fetching data: {response.status_code}")
  exit()

stories = dict()

for story_id in top_stories[:3]:
  story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty'
  story_response = requests.get(story_url)
  story_details = story_response.json()
  stories[story_id] = story_details

articles = dict()

for story in stories:
  url = stories[story]['url']
  print(f"{stories[story]['title']} - {url}")
  content = requests.get(url)

  if content.status_code == 200:
    soup = BeautifulSoup(content.text, 'html.parser')
    title = soup.find('title').get_text() if soup.find('title') else ''

    description = set_description(soup)
    body = set_body(soup)

    summary = description + clean_text(body)
    short_summary = summarize_text(summary, 1000)

    articles[url] = {
      'title': title,
      'content': summary
    }
  else:
    print(f"Error fetching content: {content.status_code}")
  
  final = []
  for story in stories:
    print(f"Story: {stories[story]}")
    if 'text' in stories[story]:
      hn_comment = call_ollama(stories[story]['text'])

    if stories[story]['url'] in articles:
      scraped_content = articles[stories[story]['url']]['content']
      content = call_ollama(scraped_content)

    final.append({
      'hn_id': story,
      'title': stories[story]['title'],
      'url': stories[story]['url'],
      'comment_count': stories[story]['descendants'] if 'descendants' in stories[story] else 0,
      'hn_comment': hn_comment if hn_comment else '',
      'content': content if content else '',
      'comment_ids': stories[story]['kids'] if 'kids' in stories[story] else []
    })

pprint.pprint(final)