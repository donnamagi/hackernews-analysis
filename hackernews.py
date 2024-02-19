import requests
from bs4 import BeautifulSoup
import re
import json

def clean_text(text):
  """Remove extra spaces, newlines, and any script/style elements."""
  text = re.sub('\s+', ' ', text)
  text = re.sub('\n', ' ', text)
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

# Hacker News API 
  
def get_top_stories():
  url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'

  response = requests.get(url)
  if response.status_code == 200:
    return response.json()
  else:
    print(f"Error fetching data: {response.status_code}")

def get_story_details(story_id):
  url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty'

  response = requests.get(url)
  if response.status_code == 200:
    return response.json()
  else:
    print(f"Error fetching data: {response.status_code}")

def get_stories(limit=3):
  stories = dict()
  top_stories = get_top_stories()
  for story_id in top_stories[:limit]:
    stories[story_id] = get_story_details(story_id)
  return stories

def scrape_content(stories):
  articles = dict()
  for story in stories:
    url = stories[story]['url']
    content = requests.get(url)

    if content.status_code == 200:
      soup = BeautifulSoup(content.text, 'html.parser')
      title = soup.find('title').get_text() if soup.find('title') else ''

      description = set_description(soup)
      body = set_body(soup)

      summary = description + clean_text(body)

      articles[url] = {
        'title': title,
        'content': summary
      }
    else:
      print(f"Error fetching content: {content.status_code}")
  return articles
  
def get_full_dict(articles, stories):
  data = []
  for story in stories:

    hn_comment = ''
    if 'text' in stories[story]:
      llm = call_ollama(stories[story]['text'])
      hn_comment += clean_text(llm)

    content = ''
    if stories[story]['url'] in articles:
      scraped_content = articles[stories[story]['url']]['content']
      llm = call_ollama(scraped_content)
      content += clean_text(llm)

    data.append({
      'hn_id': story,
      'title': stories[story]['title'],
      'url': stories[story]['url'],
      'comment_count': stories[story]['descendants'] if 'descendants' in stories[story] else 0,
      'hn_comment': hn_comment,
      'content': content,
      'comment_ids': stories[story]['kids'] if 'kids' in stories[story] else []
    })
  return data

def main():
  stories = get_stories()
  articles = scrape_content(stories)
  data = get_full_dict(articles, stories)
  return data
