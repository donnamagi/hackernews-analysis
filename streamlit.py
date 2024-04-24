import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import altair as alt
from utils import get_articles_per_week, get_mentions_per_day, get_week_start_end_dates
from trying import get_all_companies_per_week, get_companies_per_week
from events import get_events


export = pd.read_csv(f'exports/export_2024-04-21.csv')
keywords = pd.read_csv(f'exports/keywords_2024-04-21.csv')

st.write("""
        # Hi!
         
        This is an exposé of my work from the last semester. I set out to create my own dataset of stories and articles 
        from Hacker News, and trying to find connections and extract insights from the data I was processing.
        
         """)

st.write(" ## What is Hacker News?")
col1, col2 = st.columns(2)
col1.write(keywords)
col2.write("""
            
          Hacker News, as defined by their Wikipedia, is a social news website focusing on computer science and 
          entrepreneurship. 
           
          In general, content that can be submitted is defined as **"anything that gratifies one's intellectual curiosity"**.
           
          As you can see from the keywords on the left though, there is a definite bias to technical topics in the community.
        
          """)

st.bar_chart(keywords, y="frequency", x="keyword")

st.write("""
         ## Introduction to the dataset
        
         Although there are datasets available on the content of this website, none of them were recent. Hacker News does 
         however have an open API that allowed me to access their articles and statistics in real time. This provoked me 
         to create my own dataset.

        #### My data aggregation process
         
         - Each day, get the top 50 trending articles from Hacker News 
         - Store the metrics, comments, etc data from Hacker News 
         - Get the content of the article (often on third party websites)
         - Synthesize and process the content using Llama 2 (a locally running LLM)
         - Extract mentions of organisations and topics (referenced as "keywords" in the dataset)
         - Create embeddings from the processed content

         #### First 100 lines of the dataset

         """)

# get down to 50 or 100 or so
st.write(export)

st.write("""

         However, I learned that the frontline trending articles tend to, on average, stay there for 1-3 days. That meant unique
         content added per day was more around 10-15 articles.

         The dependency on me to trigger the data aggregation script daily is a definite cause of some inconsistency in the dataset. 
         The week of March 25th introduced a dip in articles processed - this is not related to anomalies on Hacker News, but me 
         missing three days of content.

         """)

st.write("#### Articles added per week")
# fix dates with range names
# and pull more articles
st.line_chart(get_articles_per_week(), x='date', y='Count', width="container")

st.write(""" 
         ## Knowledge body

         I wished to visualize the articles on Hacker News through their semantic meaning. For this, comparing the article embedding's 
         cosine similarity helped me create graph visualisations of the data. 
         
         Starting out with a cosine similarity treshold > 0.7 produced a dense graph with very few outliers or distinguishable patterns.
         From this, I would infer to say that in general, the trending content on Hacker News is a rather coherent subset of similar 
         articles - at least in their choices of topic.  

         #### Graph of the complete dataset
         As of April 7th, with a cosine similarity treshold of 0.7

         """)

### ADD IMAGES OF GRAPHS
# or somehow the graph itself?

st.write(""" 
         By increasing the cosine similarity treshold and enhancing the edge weights, I was able to produce more coherent and 
         telling graphs.
         """)


# TOPIC CLUSTERS? That you could select? would be cool

# st.write("## Mentions of keywords per day")

# options = ['AI', 'Apple', 'GitHub', 'Security', 'Performance', 'Google', 'API', 
#            'Development', 'Technology', 'Language models', 'Privacy', 'Open-source', 
#            'EU', 'Open source', 'Linux', 'Automation', 'the European Union']
# options = st.multiselect(
#     'Choose keywords to plot',
#     options,
#     options)

# st.scatter_chart(get_mentions_per_day(options), x='date', size= options[0])

st.write("# Companies in the spotlight")
st.write("""
         Many companies were mentioned in the dataset on an occasional basis. Because of the limited size of the dataset,
         I believed it would be more meaningful to draw conclusions when working with aggregated data on a weekly basis. 
         
         For this, I filtered out the mentions of companies and other organizations, and compared how popular they were in 
         comparison with other topics that week. Any company not included in the top 15 most common keywords for that week 
         was excluded from this subset.
         """)

st.write("#### Companies mentioned per week")
df, long_df = get_all_companies_per_week()
st.scatter_chart(long_df, x='Company', y='Week', size='Mentions', color='Company', height=400)

st.write("""
         There is a clear technical bias to the companies and organisations in focus, with no obvious pattern to the amount 
         of front-page attention companies receive. 

         #### Finding reasons

         Why was Google mentioned so frequently in the week of February 11th, 2024? Filtering the articles of that week
         for the keyword 'Google' gives us this:
         """)

weekly_df = pd.read_csv('exports/weekly/weekly_2024-02-19.csv')
weekly_df = weekly_df[weekly_df['keywords'].str.contains('Google', case=False, na=False)]
weekly_df = weekly_df[['title', 'keywords', 'content_summary', 'Date', 'Processing Date']]
st.write(weekly_df)

st.write("""
         Based on the titles of the articles, this seems to be the week when Google released two new AI models. Google was
         a recurring conversation topic in the technical community due to its groundbreaking, but controversial launches.

         #### Conclusion

         The rise in weekly mentions of companies are in alignment with real-world events.
         
         GitHub is an outlier - many mentions of Github were due to the articles promoting their work in GitHub repositories, 
         not news related to the company itself
         """)

## build something like – select company and get the articles for it?
## probably not relevant. but maybe?

# companies = ['Boeing', 'Google', 'Intel', 'Apple', 'GitHub', 'Android', 'the European Union', 'ChatGPT', 'YouTube']
# defaults = ['Boeing']
# company_options = st.multiselect(
#       'Click to select different companies to plot on the line chart below',
#       companies, defaults)

# new_df = get_companies_per_week(company_options, df)
# st.line_chart(new_df, x='Week', height=300)

st.write("## Significant events")

st.write("""         
         The discourse around certain key events influenced the community's attention. There is not only an uptick
         in the mentions of companies or technologies involved, but often the underlying issues as well. 
          """)

events = get_events()
titles = [event['title'] for event in events]
tab1, tab2, tab3, tab4 = st.tabs(titles)

with tab1:
  st.write("""A security backdoor was found in a widely used open source piece of software - XZ. 
           The attack raised concerns about the security of open source software, and the execution 
           sparked widespread discussion.""")
  
  st.write(f"Counting mentions for the following keywords: {events[0]['keywords']}")
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
  st.write(f"Counting mentions for the following keywords: {events[1]['keywords']}")
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
  st.write(f"Counting mentions for the following keywords: {events[2]['keywords']}")
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
  st.write(f"Counting mentions for the following keywords: {events[3]['keywords']}")
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


