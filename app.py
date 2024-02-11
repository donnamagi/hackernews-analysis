import requests
from bs4 import BeautifulSoup
import re

def clean_text(text):
    """Remove extra spaces, newlines, and any script/style elements."""
    text = re.sub('\s+', ' ', text)
    return text.strip()

def summarize_text(text, max_chars=2000):
    """Summarize the text to the first N characters."""
    return text[:max_chars]

url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'

response = requests.get(url)
if response.status_code == 200:
  top_stories = response.json()
else:
  print(f"Error fetching data: {response.status_code}")
  exit()

stories = dict()

for story_id in top_stories[:5]:
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
    description = soup.find('meta', attrs={'name': 'description'}).get('content', '')

    body_content = soup.find(['article', 'main'])
    if not body_content:
      body_content = soup.find('body')  

    body_text = clean_text(body_content.get_text())
    summarized_text = summarize_text(body_text, 2000)

    articles[stories[story]['url']] = {
        'title': title,
        'description': description,
        'content': summarized_text
    }

  else:
    print(f"Error fetching content: {content.status_code}")

for article in articles:
  print('''\n\n
        Title: {title}
        Description: {description}
        Content: {content}
        '''.format(**articles[article])
        )