from hackernews import main as get_hn_data
from scrape import main as scrape_content
from embeddings import get_content_embeddings
import pprint

data = get_hn_data()
for story in data:
  summary = scrape_content(story['url'])
  if summary:
    story['content'] = summary
    story['vector'] = get_content_embeddings([summary])

pprint.pprint(data)
