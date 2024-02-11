import requests
from bs4 import BeautifulSoup
import re
import pprint

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
  if 'github.com' in stories[story]['url']:
    body_content = soup.find(['article'], class_='markdown-body')
  else:
    body_content = soup.find(['article', 'main'])
    if not body_content:
      body_content = soup.find('body')  

  body = body_content.get_text() if body_content else ''

  return body


url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'

response = requests.get(url)
if response.status_code == 200:
  top_stories = response.json()
else:
  print(f"Error fetching data: {response.status_code}")
  exit()

stories = dict()

for story_id in top_stories[:10]:
  story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty'
  story_response = requests.get(story_url)
  story_details = story_response.json()
  stories[story_id] = story_details

articles = dict()

for story in stories:
  print(f"{stories[story]['title']} - {stories[story]['url']}")
  content = requests.get(stories[story]['url'])

  if content.status_code == 200:
    soup = BeautifulSoup(content.text, 'html.parser')
    title = soup.find('title').get_text()

    description = set_description(soup)
    body = set_body(soup)

    summary = description + clean_text(body)
    short_summary = summarize_text(summary, 1000)

    articles[stories[story]['url']] = {
      'title': title,
      'content': summary
    }
  else:
    print(f"Error fetching content: {content.status_code}")
  
  final = []
  for story in stories:    
    final.append({
      'hn_id': stories[story]['id'],
      'title': stories[story]['title'],
      'url': stories[story]['url'],
      'comment_count': stories[story]['descendants'] if 'descendants' in stories[story] else 0,
      'content': articles[stories[story]['url']]['content'] if stories[story]['url'] in articles else '',
      'comment_ids': stories[story]['kids'] if 'kids' in stories[story] else []
    })

pprint.pprint(final)