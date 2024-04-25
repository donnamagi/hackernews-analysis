import pandas as pd
import streamlit as st
import altair as alt
from utils import get_articles_per_week
from events import get_events


export = pd.read_csv(f'demo/export_2024-04-25.csv')
keywords = pd.read_csv(f'demo/keywords_2024-04-25.csv')

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

st.write("""
         And as this dataset has been created between February and April 2024 - a time of rapid growth in the field of 
         artificial intelligence - it is not surprising that mentions of AI surpass all other topics.
         """)
st.bar_chart(keywords.head(10), y="frequency", x="keyword")

st.write("""
         ## Introduction to the dataset
        
         Although there are datasets available on the content of this website, none of them were recent. Hacker News does 
         however have an open API that allowed me to access their articles and statistics in real time. This provoked me 
         to create my own dataset.

         By the time of this exposé, I have 700 processed articles from Hacker News.

        #### My data aggregation process
         
         - Each day, get the top 30 trending articles from Hacker News 
         - Store the metrics, comments, etc data from Hacker News 
         - Get the content of the article (often on third party websites)
         - Synthesize and process the content using Llama 2 (a locally running LLM)
         - Extract mentions of organisations and topics (referenced as "keywords" in the dataset)
         - Create embeddings from the processed content

         #### First 100 lines of the dataset

         """)

st.write(export.head(101))

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

         I wished to see if the articles formed any noticeable clusters, and if so, what topics were most prevalent in the dataset.
         
         #### Graph of the complete dataset
         Graphs below are generated from the dataset as of April 7th, 2024.

         A cosine similarity treshold > 0.7 produced a dense graph with very few outliers or distinguishable patterns.
         """)

caption = "Graph of the complete dataset with a cosine similarity treshold of 0.7"
st.image(image="./demo/og_graph.png", caption=caption, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.write(""" 
         By increasing the cosine similarity treshold and tinkering with the edge weights, I was able to produce more coherent and 
         readable graphs later on.

         For example, on the graph below, I hypothesized that the most high-degree articles would provide insights into the most popular
         topics on Hacker News.
        
         I filtered out the nodes with a degree of less than 6, and titled the most high-degree nodes by their keywords.
         """)

caption = "Graph of only nodes with degree > 6, with the most high-degree nodes titled by their keywords."
st.image(image="./demo/keywords-graph.png", caption=caption, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.write("""

         This was rather telling of the most popular topics on Hacker News. The most recurring topic clusters were related to AI, 
         open source work, both hardware and software development, and - quite surprisingly to me - discussions around licensing and 
         regulations.

         The outlier node on the top of the graph represents and interesting subsection of articles that I would title as personal projects.
         The article in question was about a book generated from the author's personal messaging history, and related to many other articles
         around people showcasing their pet projects.

         #### Conclusion
         
         In general, the trending content on Hacker News is a rather coherent body of knowledge. 

         Graphs of the dataset were a viable way to gain insights into the main topic clusters discussed on the platform.
         
         Although Hacker News brands itself as a forum for "anything interesting", it is rare to have front-page articles on 
         topics unrelated to technology.
         """)

st.write("# Companies in the spotlight")
st.write("""
         Many companies were mentioned in the dataset on an occasional basis. Because of the limited size of the dataset,
         I believed it would be more meaningful to draw conclusions when working with aggregated data on a weekly basis. 

         I wanted to see if the mentions of companies were in any way related to the most popular topics of the week, and if 
         there were any noticeable correlations of real world events.

         """)

caption = "Most mentioned companies per week"
st.image(image="./demo/top-5.png", caption=caption, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.write("""
         I wished to track the mentions of the most popular companies in the dataset over the total period to see more general
         popularity trends. The graph above, an early attempt on visualizing this data, seemed riddled with outliers.

         For this, I found the 20 most mentioned companies overall, and compared how popular they were on a weekly basis in 
         comparison with the other topics that week. Any company not included in the top 15 most common keywords for that week 
         was excluded from this subset.
         """)

st.write("#### Companies mentioned per week")


long_df = pd.read_csv('demo/weekly_companies_long_2024-04-25.csv')
st.scatter_chart(long_df, x='Company', y='Week', size='Mentions', color='Company', height=400)

st.write("""
         There is a clear technical bias to the companies and organisations in focus, with no obvious pattern to the amount 
         of front-page attention companies receive. 

         #### Finding reasons

         Why was Google mentioned so frequently in the week of February 11th, 2024? Filtering the articles of that week
         for the keyword 'Google' gives us this:
         """)

weekly_df = pd.read_csv('demo/weekly_2024-02-19.csv')
weekly_df = weekly_df[weekly_df['keywords'].str.contains('Google', case=False, na=False)]
weekly_df = weekly_df[['title', 'keywords', 'content_summary', 'Date', 'Processing Date']]
st.write(weekly_df)

st.write("""
         Based on the titles of the articles, this seems to be the week when Google released two new AI models. Google was
         a recurring conversation topic in the technical community due to its groundbreaking, but controversial launches.
         """)

st.write("#### Significant events")

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

## replace with google and gemini?
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
  
st.write("""
         #### Conclusion

         The rise in weekly mentions of companies are in alignment with real-world events.

         Outstanding events triggered shifts in discourse, producing noticeable spikes in keyword mentions also for the more
         general related topics. 
         
         GitHub is an outlier - many mentions of Github were due to the articles promoting their work in GitHub repositories, 
         not news related to the company itself.

         #### This has been my exposé. 
         
         ### Thank you for your attention!
         """)
