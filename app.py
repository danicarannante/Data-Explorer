
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
import requests


# st.title('MLB Player Stats Explorer')

# st.markdown("""
# This app performs simple webscraping of NBA player stats data!
# * **Python libraries:** base64, pandas, streamlit
# * **Data source:** [Baseball-reference.com](https://www.baseball-reference.com/).
# """)

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1980,2023))))

# Web scraping of NBA player stats
@st.cache_data
def load_data(year):
    url = "https://www.baseball-reference.com/leagues/majors/" + str(year) + ".shtml"
    #url = "https://www.mlb.com/stats/"
    response = requests.get(url)
    html = pd.read_html(response.content)
    df = html[0]

    filtered = df.drop(df[df.Tm == 'Tm'].index).drop(df[df.Tm == 'League Average'].index).dropna() # Deletes repeating headers in content
    return filtered

playerstats = load_data(selected_year)

# Sidebar - Team selection
unique_team = playerstats.Tm.unique()
selected_team = st.sidebar.selectbox('Team', unique_team)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm == selected_team)]

st.header(f'Display Team Stats of {selected_team}')
st.dataframe(df_selected_team)

