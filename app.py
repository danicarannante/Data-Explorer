
import streamlit as st
import pandas as pd
import base64
#import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
import requests


# st.title('MLB Player Stats Explorer')

# st.markdown("""
# This app performs simple webscraping of NBA player stats data!
# * **Python libraries:** base64, pandas, streamlit
# * **Data source:** [Baseball-reference.com](https://www.baseball-reference.com/).
# """)

# st.sidebar.header('User Input Features')
# selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))

# Web scraping of NBA player stats
@st.cache_data
def load_data(year):
    #url = "https://www.baseball-reference.com/leagues/majors/" + str(year) + ".shtml"
    url = "https://www.mlb.com/stats/"
    response = requests.get(url)
    html = pd.read_html(response.content)
    df = html[0]
    raw = df.drop(df[df.PLAYERPLAYER == 'PLAYERPLAYER'].index) # Deletes repeating headers in content
    print(raw)
    return df
playerstats = load_data(2023)

# Sidebar - Team selection
unique_team = playerstats.TEAMTEAM.unique()
print(unique_team)

selected_team = st.sidebar.multiselect('Team', unique_team, unique_team)


# # Sidebar - Position selection
# unique_pos = ['C','PF','SF','PG','SG']
# selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# # Filtering data
# df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

# st.header('Display Player Stats of Selected Team(s)')
# st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
# st.dataframe(df_selected_team)
