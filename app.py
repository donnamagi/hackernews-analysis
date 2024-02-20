from hackernews import main as get_hn_data
from scrape import main as scrape_content
from embeddings import get_embedding
from milvus import batch_insert

data = get_hn_data()
for story in data:
  summary = scrape_content(story['url'])
  if summary:
    story['content'] = summary
    story['vector'] = get_embedding([summary])
  elif story['hn_comment']: 
    story['content'] = ''
    story['vector'] = get_embedding([story['hn_comment']])
  else:
    story['content'] = ''
    story['vector'] = get_embedding([story['title']])

batch_insert(data)
