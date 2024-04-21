import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import altair as alt
from utils import get_articles_per_week, get_mentions_per_day


export = pd.read_csv(f'exports/export_{datetime.now().strftime("%Y-%m-%d")}.csv')
keywords = pd.read_csv(f'exports/keywords_{datetime.now().strftime("%Y-%m-%d")}.csv')


st.write("## The data I am working with")
st.write(export)

st.write("## List of most frequently recurring keywords")
st.write(keywords)

st.write("## Articles added per week")
st.line_chart(get_articles_per_week(), x='Date', y='Count')

st.write("## Mentions of keywords per day")

options = ['AI', 'Apple', 'GitHub', 'Security', 'Performance', 'Google', 'API', 'Development', 'Technology', 'Language models', 'Privacy', 'Open-source', 'EU', 'Open source', 'Linux', 'Automation', 'the European Union']
options = st.multiselect(
    'Choose keywords to plot',
    options,
    ['AI', 'Apple'])

st.scatter_chart(get_mentions_per_day(options), x='Date')



events = [
  {
    'title': 'XZ Backdoor attack discovered',
    'annotations': [('Mar 29, 2024', 'XZ Backdoor attack discovered')],
    'keywords': ['Security', 'Backdoor', 'Open source', 'XZ']
  },
  {
    'title': 'Apple EU lawsuit',
    'annotations': [('Mar 29, 2024', 'XZ Backdoor attack discovered')],
    'keywords': ['Apple', 'EU', 'the European Union', 'Development']
  },
  {
    'title': 'The AI Act',
    'annotations': [('Mar 29, 2024', 'XZ Backdoor attack discovered')],
    'keywords': ['EU', 'the European Union', 'Artificial intelligence', 'AI', 'Privacy']
  }
]

for event in events:
  mentions_df = get_mentions_per_day(event['keywords'])
  mentions_df['Total mentions'] = mentions_df[event['keywords']].sum(axis=1)

  event['df'] = mentions_df

st.write("## Events")

titles = [event['title'] for event in events]
tab1, tab2, tab3 = st.tabs(titles)

with tab1:
  st.write('A security backdoor was found in a widely used open source piece of software - XZ. The attack raised concerns about the security of open source software, and the execution sparked widespread discussion.')
  xz_chart = alt.Chart(events[0]['df']).mark_circle().encode(
    x='Date', y='Total mentions', color='Total mentions', tooltip=['Date'] + events[0]['keywords']
  ).interactive()
  st.altair_chart(xz_chart, use_container_width=True)


with tab2:
  apple_chart = alt.Chart(events[1]['df']).mark_circle().encode(
    x='Date', y='Total mentions', color='Total mentions', tooltip=['Date'] + events[1]['keywords']
  ).interactive()
  st.altair_chart(apple_chart, use_container_width=True)


with tab3:
  eu_chart = alt.Chart(events[2]['df']).mark_circle().encode(
    x='Date', y='Total mentions', color='Total mentions', tooltip=['Date'] + events[2]['keywords']
  ).interactive()
  st.altair_chart(eu_chart, use_container_width=True)
