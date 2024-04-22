import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import altair as alt
from utils import get_articles_per_week, get_mentions_per_day, get_week_start_end_dates
from trying import get_all_companies_per_week, get_companies_per_week


export = pd.read_csv(f'exports/export_2024-04-21.csv')
keywords = pd.read_csv(f'exports/keywords_2024-04-21.csv')


st.write("## The data I am working with")
st.write(export)

st.write("## List of most frequently recurring keywords")
st.write(keywords)

st.write("## Articles added per week")
st.line_chart(get_articles_per_week(), x='date', y='Count')

st.write("## Mentions of keywords per day")

options = ['AI', 'Apple', 'GitHub', 'Security', 'Performance', 'Google', 'API', 
           'Development', 'Technology', 'Language models', 'Privacy', 'Open-source', 
           'EU', 'Open source', 'Linux', 'Automation', 'the European Union']
options = st.multiselect(
    'Choose keywords to plot',
    options,
    options)

st.scatter_chart(get_mentions_per_day(options), x='date', size= options[0])

st.write("# Companies in the spotlight")
st.write("""
         To start from somewhere, I looked into the most popular keywords per week.
         From there, I filtered out the mentions of companies and other organizations.

         This is not every organization mentioned in the dataset, but rather companies that
         stood out in the top 15 conversational keywords every week.
         """)

st.write("### Companies mentioned per week")
df, long_df = get_all_companies_per_week()
st.scatter_chart(long_df, x='Company', y='Week', size='Mentions', color='Company', height=400)

st.write("""
         Besides the clear technical bias, there is no obvious pattern to the amount of front-page attention 
         companies receive. 
         
         I suspected a correlation with real-world events that trigger this spike in community attention. 

         ##### Let's take a closer look

         Why was Google mentioned so frequently in the week of February 11th, 2024? Filtering the articles of that week
         for the keyword 'Google' gives us this:
         """)

weekly_df = pd.read_csv('exports/weekly/weekly_2024-02-19.csv')
weekly_df = weekly_df[weekly_df['keywords'].str.contains('Google', case=False, na=False)]
weekly_df = weekly_df[['title', 'keywords', 'content_summary', 'Date', 'Processing Date']]
st.write(weekly_df)

st.write("Based on the titles of the articles, this seems to be the week when Google released two new AI models.")

## build something like – select company and get the articles for it?
companies = ['Boeing', 'Google', 'Intel', 'Apple', 'GitHub', 'Android', 'the European Union', 'ChatGPT', 'YouTube']
defaults = ['Boeing']
company_options = st.multiselect(
      'Click to select different companies to plot on the line chart below',
      companies, defaults)

new_df = get_companies_per_week(company_options, df)
st.line_chart(new_df, x='Week', height=300)

events = [
  {
    'title': 'XZ Backdoor attack discovered',
    'annotations': [('Mar 29, 2024', 'XZ Backdoor attack discovered on March 29th')],
    'keywords': ['Security', 'Backdoor', 'Open source', 'XZ', 'Xz']
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
    'annotations': [('Mar 12, 2024', 'The finalizing of the AI Act is announced on March 12th')],
    'keywords': ['EU', 'the European Union', 'Artificial intelligence', 'AI Act']
  },
  {
    'title': 'Glassdoor leak',
    'annotations': [('Mar 19, 2024', 'Glassdoor users discover their anonymous reviews are public on March 19th')],
    'keywords': ['Glassdoor', 'Privacy', 'User data', 'Leak', 'Data breach']
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

st.write("## Significant events")

titles = [event['title'] for event in events]
tab1, tab2, tab3, tab4 = st.tabs(titles)

with tab1:
  st.write("""A security backdoor was found in a widely used open source piece of software - XZ. 
           The attack raised concerns about the security of open source software, and the execution 
           sparked widespread discussion.""")
  chart = alt.Chart(events[0]['df']).mark_circle().encode(
    x='date', y='Total mentions', size='Total mentions', color='Total mentions', tooltip=['date'] + events[0]['keywords']
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
    x='date', y='Total mentions', size='Total mentions', color='Total mentions', tooltip=['date'] + events[1]['keywords']
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
  st.write("""
           The AI Act was passed by the European Union on March 13th, which set new regulations for AI systems.
           The act was met with mixed reactions, with some praising the EU for taking a step towards AI regulation,
           while others criticized the act for being too restrictive.""")
  chart = alt.Chart(events[2]['df']).mark_circle().encode(
    x='date', y='Total mentions', size='Total mentions', color='Total mentions', tooltip=['date'] + events[2]['keywords']
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

with tab4:
  st.write("""Around March 19th, the topic of Glassdoor's user privacy went viral after a technical glitch.
            With anonymous reviews of companies being publicised with names, the trustworthiness
            of Glassdoor was under heavy scrutiny.""")
  chart = alt.Chart(events[3]['df']).mark_circle().encode(
    x='date', y='Total mentions', size='Total mentions', color='Total mentions', tooltip=['date'] + events[3]['keywords']
  ).interactive()

  annotation_layer = (
    alt.Chart(events[3]['annotations'])
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


