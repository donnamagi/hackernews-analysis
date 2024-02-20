import requests
import datetime

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

def get_full_dict(stories):
  data = []
  for story in stories:

    hn_comment = ''
    if 'text' in stories[story]:
      hn_comment += stories[story]['text']

    data.append({
      'hn_id': story,
      'title': stories[story]['title'],
      'url': stories[story]['url'],
      'comment_count': stories[story]['descendants'] if 'descendants' in stories[story] else 0,
      'hn_comment': hn_comment,
      'comment_ids': stories[story]['kids'] if 'kids' in stories[story] else [],
      'date': datetime.datetime.now().isoformat()
    })
  return data

def main():
  stories = get_stories()
  data = get_full_dict(stories)
  return data

main()
