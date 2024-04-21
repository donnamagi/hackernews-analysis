import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from utils import get_articles_per_week


export = pd.read_csv(f'exports/export_{datetime.now().strftime("%Y-%m-%d")}.csv')
keywords = pd.read_csv(f'exports/keywords_{datetime.now().strftime("%Y-%m-%d")}.csv')


st.write("The data I am working with:")
st.write(export)

st.write("List of most frequently recurring keywords:")
st.write(keywords)

st.write("Articles added per week:")
st.line_chart(get_articles_per_week(), x='Date', y='Count')

