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
st.line_chart(get_articles_per_week(), x='date', y='Count')

st.write("## Mentions of keywords per day")

options = ['AI', 'Apple', 'GitHub', 'Security', 'Performance', 'Google', 'API', 'Development', 'Technology', 'Language models', 'Privacy', 'Open-source', 'EU', 'Open source', 'Linux', 'Automation', 'the European Union']
options = st.multiselect(
    'Choose keywords to plot',
    options,
    ['AI', 'Apple'])

st.scatter_chart(get_mentions_per_day(options), x='date')



events = [
  {
    'title': 'XZ Backdoor attack discovered',
    'annotations': [('Mar 29, 2024', 'XZ Backdoor attack discovered on March 29th')],
    'keywords': ['Security', 'Backdoor', 'Open source', 'XZ']
  },
  {
    'title': "Apple's conflict with Spotify and Epic Games",
    'annotations': [
      ('Mar 04, 2024', 'EU announces 1.8 billion fine for Apple on March 4th'),
      ('Mar 06, 2024', 'Apple terminates developer account of Epic Games on March 6th'),
      ],
    'keywords': ['Apple', 'Epic Games', 'Fortnite', 'The Digital Markets Act', 'App Store', 'Spotify', 'Lawsuit']
  },
  {
    'title': 'The AI Act',
    'annotations': [('Mar 13, 2024', 'The AI Act is passed on March 13th')],
    'keywords': ['EU', 'the European Union', 'Artificial intelligence', 'AI Act']
  }
]

for event in events:
  # total sum of keyword mentions
  mentions_df = get_mentions_per_day(event['keywords'])
  mentions_df['Total mentions'] = mentions_df[event['keywords']].sum(axis=1)
  event['df'] = mentions_df

  # annotations to df
  annotations_df = pd.DataFrame(event['annotations'], columns=["date", "event"])
  annotations_df.date = pd.to_datetime(annotations_df.date)
  annotations_df["Total mentions"] = mentions_df['Total mentions'].max()
  event['annotations'] = annotations_df

st.write("## Events")

titles = [event['title'] for event in events]
tab1, tab2, tab3 = st.tabs(titles)

with tab1:
  st.write("""A security backdoor was found in a widely used open source piece of software - XZ. 
           The attack raised concerns about the security of open source software, and the execution 
           sparked widespread discussion.""")
  chart = alt.Chart(events[0]['df']).mark_circle().encode(
    x='date', y='Total mentions', color='Total mentions', tooltip=['date'] + events[0]['keywords']
  ).interactive()

  annotation_layer = (
    alt.Chart(events[0]['annotations'])
    .mark_text(size=20, text="⬇", dx=-5, dy=-10, align="center", baseline="middle", color="white")
    .encode(
        x="date:T",
        y=alt.Y("Total mentions:Q"),
        tooltip=["event"],
    )
    .interactive()
  )
  st.altair_chart(
    (chart + annotation_layer).interactive(),
    use_container_width=True
)


with tab2:
  st.write("""In the span of a couple of days, Apple was the center of attention in the tech world.
           Spotify raised concerns over Apple's App Store policies, which resulted in a 1.8b fine from the EU.
           Straight after, Apple's termination of Epic Games' developer account (Fortnite) sparked a lawsuit.""")
  chart = alt.Chart(events[1]['df']).mark_circle().encode(
    x='date', y='Total mentions', color='Total mentions', tooltip=['date'] + events[1]['keywords']
  ).interactive()

  annotation_layer = (
    alt.Chart(events[1]['annotations'])
    .mark_text(size=20, text="⬇", dx=-5, dy=-10, align="center", baseline="middle", color="white")
    .encode(
        x="date:T",
        y=alt.Y("Total mentions:Q"),
        tooltip=["event"],
    )
    .interactive()
  )
  st.altair_chart(
    (chart + annotation_layer).interactive(),
    use_container_width=True
)


with tab3:
  chart = alt.Chart(events[2]['df']).mark_circle().encode(
    x='date', y='Total mentions', color='Total mentions', tooltip=['date'] + events[2]['keywords']
  ).interactive()

  annotation_layer = (
    alt.Chart(events[2]['annotations'])
    .mark_text(size=20, text="⬇", dx=0, dy=-10, align="center", baseline="middle", color="white")
    .encode(
        x="date:T",
        y=alt.Y("Total mentions:Q"),
        tooltip=["event"],
    )
    .interactive()
  )
  st.altair_chart(
    (chart + annotation_layer).interactive(),
    use_container_width=True
)
