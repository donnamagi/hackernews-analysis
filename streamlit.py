import pandas as pd
import streamlit as st
import altair as alt
from events import get_events


export = pd.read_csv(f'demo/export_2024-04-25.csv')
keywords = pd.read_csv(f'demo/keywords_2024-04-25.csv')

st.write("""
        # Analysis of trending content on the web platform Hacker News 
         
         The objective of this project was to create my own dataset of stories and articles from Hacker News, and to find insightful 
         correlations between the popular discourse in the tech community and real world events. 
         """)

st.write(" ## Introduction to Hacker News")
col1, col2 = st.columns(2)
col1.write(keywords)
col2.write("""
            
          [Hacker News](https://news.ycombinator.com), as defined by their Wikipedia, is a social news website focusing on 
          computer science and entrepreneurship. 
           
          In general, content that can be submitted is defined as **"anything that gratifies one's intellectual curiosity"**.
          
          On the left is a list of the most prevalent topic mentions in the dataset.
          """)

st.write("""
         As this dataset has been created between February and April 2024 - a time of rapid growth in the field of 
         artificial intelligence - mentions of AI surpass all other topics.
         """)

st.bar_chart(keywords.head(10), y="frequency", x="keyword")

st.write("""
         ## Introduction to the dataset
        
         Existing datasets available for the content on Hacker News were outdated. This prompted me to create a new dataset
         which uses the website's open API to access articles and statistics in real time. 

         At the time of this report, the dataset comprises of over 700 processed articles from Hacker News.

        ### Data aggregation methodology
         
         A systematic process was employed to collect and process articles from Hacker News. The methodology involved:
         

          1. **Daily Article Retrieval**: The top 30 trending articles from Hacker News were retrieved on a daily basis.
          2. **Metadata Collection**: Associated metrics, comments, and other relevant data were extracted from Hacker News.
          3. **Content Acquisition**: The content of each article was retrieved from their respective source.
          4. **Content Processing**: The article content was cleaned and synthesized using Llama 2, a locally running Large Language Model (LLM).
          5. **Entity Extraction**: Mentions of organizations and topics (referred to as "keywords" in the dataset) were extracted from the processed content.
          6. **Embedding Generation**: Vector embeddings were created from the processed content, enabling further analysis and modeling.
          7. **Data Storage**: The processed data was stored in a vector database for further analysis and visualization.
         
         #### First 100 lines of the dataset

         """)

st.write(export.head(101))

st.write("""

         Although 30 articles were chosen for processing every day (equivalent to the front page of Hacker News), the frontline trending articles tended to, 
         on average, stay there for 1-3 days. That meant unique content added per day was more around 7-10 articles.

         """)

st.write("#### Articles added per week")

articles_df = pd.read_csv('demo/articles_per_week_2024-04-25.csv')
st.line_chart(articles_df, x='date', y='Count', width="container")

st.write(""" 
         
         The dependency on manually triggering the data aggregation script daily has introduced some inconsistency in the dataset. Specifically, the week of 
         March 25th introduced a notable gap in the amount of articles processed - this can be attributed to a 3-day lapse in executing the script, not 
         anomalies on Hacker News itself.

         ## Visualizing the dataset

         To visualize the articles on Hacker News through their semantic structure, I utilized cosine similarity analysis of article embeddings
         to create graph visualisations of the data. 

         I wished to determine whether the articles formed any noticeable clusters, and, if so, identify what topics were most prevalent in the dataset.
         
         #### Graph of the complete dataset
         Graphs below are based on the dataset as of April 7th, 2024.

         Applying a cosine similarity threshold > 0.7 produced a dense graph with very few outliers or distinguishable patterns.
         """)

caption = "Graph of the complete dataset with a cosine similarity threshold of 0.7"
st.image(image="./demo/og_graph.png", caption=caption, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.write(""" 
         To enhanche the clarity and coherence of the graphs, I iteratively adjusted the cosine similarity threshold and edge weights.

         I hypothesized that the nodes (articles) with the highest degree centrality would provide insights into the most popular
         topics on Hacker News.
        
         To identify these articles, I applied a degree threshold of 6, filterint out nodes with less connection to the general corpus 
         of articles. Sequentially, I labeled the highest-degree nodes by their corresponding keywords to provide some context.
         """)

caption = "Graph of nodes with degree > 6, with the highest-degree nodes labeled by their keywords."
st.image(image="./demo/keywords-graph.png", caption=caption, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.write("""
         
         This refined graph revealed the most central articles on Hacker News, providing insights to the clusters of popular topics. 
         The most recurring topics were related to Artificial Intelligence, open-source initiatives, and both hardware and software 
         development. Notably, discussions surrounding licensing and regulations also emerged as a significant theme.

         The outlier node on top of the graph represents and interesting subset of articles that can be categorized as personal projects.
         The central article in question was about a book generated from the author's personal messaging history, and related to 
         other articles featuring individuals showcasing their pet projects.

         #### Conclusion
         
         In general, the trending content on Hacker News is a rather coherent body of knowledge. 

         Graphs of the dataset were a viable way to gain insights into the main topic clusters discussed on the platform.
         
         Although Hacker News brands itself as a forum for "anything interesting", it is rare to have front-page articles on 
         topics unrelated to technology.
         """)

st.write("# Companies in the spotlight")
st.write("""
         Many companies were mentioned in the dataset on an occasional basis. Because of the limited size of the dataset,
         I believed it would be more insightful to draw conclusions when working with aggregated data on a weekly basis. 

         I examined whether certain companies were associated with the most popular topics of the week, and if there 
         were any noticeable correlations with real-world events.

         Popularity in this context is defined as the number of mentions in the dataset.

         """)

caption = "Most mentioned companies per week"
st.image(image="./demo/top-5.png", caption=caption, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.write("""
         The graph above, an early attempt on visualizing this data, seemed riddled with outliers, likely due to the small dataset. 
         I wished to track the mentions of the all-time most mentioned companies across the entire period, aiming to identify more general
         popularity trends.

         For this, I identified the 20 most popular companies overall, and use time series analysis to compare their weekly popularity in 
         comparison with other weekly trending topics. Any company not included in the top 15 most popular keywords for that week 
         was excluded from this subset.

         """)

st.write("#### Companies mentioned per week")


long_df = pd.read_csv('demo/weekly_companies_long_2024-04-25.csv')
st.scatter_chart(long_df, x='Company', y='Week', size='Mentions', color='Company', height=400)

st.write("""
         There is a clear technical bias to the companies and organisations in focus, with no obvious pattern or correlation with 
         company size to the amount of front-page attention different entities received. 

         Most likely, the patterns in the data are due to real-world events, such as product launches or controversial decisions.

         #### Deep dive into the data

         To prove this hypothesis, I decided to investigate the weekly mentions of Google in the dataset.

         Why was Google mentioned so frequently in the week of February 11th, 2024? Filtering the articles of February 11th, 2024
         for the keyword 'Google' revealed the following articles:
         """)

weekly_df = pd.read_csv('demo/weekly_2024-02-19.csv')
weekly_df = weekly_df[weekly_df['keywords'].str.contains('Google', case=False, na=False)]
weekly_df = weekly_df[['title', 'keywords', 'content_summary', 'Date', 'Processing Date']]
st.write(weekly_df)

st.write("""
         Based on the titles of the articles, this week can be correlated to when Google released two new AI models. Google was
         a recurring conversation topic in the technical community due to its groundbreaking, but controversial product reveals.
         """)

st.write("#### Significant events")

st.write("""         
         The discourse around certain key events influenced the community's attention. There is not only an uptick
         in the mentions of companies or technologies involved, but often the underlying issues as well. 
          """)

events = get_events()
titles = [event['title'] for event in events]
tab1, tab2, tab3 = st.tabs(titles)

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
           Google released a new groundbreaking LLM model called Gemini on February 15th. Early reviewers of the model noted 
           that the model was heavily biased towards certain racial groups, and that it emphasized representation
           over historical accuracy. The release sparked a discussion about the dangers of misinformation and the future of 
           AI's influence.
           """)
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
  
st.write("""
         #### Conclusion

         The rise in weekly mentions of companies are in alignment with real-world events.

         Outstanding events may have triggered shifts in discourse, producing spikes in keyword mentions also for the more
         general related topics. However, the amount of overall mentions are too low to draw any definitive conclusions of 
         this correlation.
         
         GitHub is an outlier - consistent mentions of Github were due to the articles promoting their work in GitHub repositories, 
         not news related to the company itself.

         ## Future work

         The dataset is still in its infancy, and there are many avenues for further analysis and improvement:
         
         #### Sentiment analysis 
         
         Sentiment analysis of the articles and their corresponding commentary by the community could provide insights into 
         the community's general mood and opinions on the topics discussed, as well as the companies and technologies involved. 

         This could be analysed in opposition with market data to see if there are any correlations between the community's 
         sentiment and the stock market.

          #### Data aggregation

         Entity recognition could be improved to better identify companies and organizations in the articles. For now, this
         process was manually aided by removing certain common abbreviations spaCy had wrongfully labeled as organisations.

         The process of data aggregation could be automated to ensure a more consistent dataset. Processing more articles per day
         could also benefit the dataset's size and quality of analysis. 


          #### Time series analysis
         
         As the dataset grows, time series analysis could provide insights into the evolvement of the community's interests, 
         as well as the tech scene.

         The current dataset could equally be compared to older datasets, if equally processed, to identify trends and shifts in
         the community's interests over time.
         """)
