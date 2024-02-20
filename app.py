from hackernews import main as get_hn_data
from scrape import main as scrape_content
import pprint

data = get_hn_data()
for story in data:
  summary = scrape_content(story['url'])
  story['content'] = summary


pprint.pprint(data)