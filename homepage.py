
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import requests

st.set_page_config(
    page_title="MLB Data Explorer"
)

st.title('Main Page Explorer')

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

df = load_data(selected_year) # raw input 
# Sidebar - Team selection
unique_team = df.Tm.unique()
selected_team = st.sidebar.selectbox('Team', unique_team)
# Filtering data
df_selected_team = df[(df.Tm == selected_team)]

# ------------------------------------------------------------------------------------------------
# Convert non-numeric columns to numeric 
numeric_cols = df.columns[1:]  #  first column is 'Team'
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Create the Streamlit app
st.title('Baseball Team Stats')

# Display DataFrame (optional)
st.write(df)

# Create a bar graph
selected_stat = st.sidebar.selectbox('Select a stat:', numeric_cols)
plt.figure(figsize=(10, 6))
plt.bar(df['Tm'], df[selected_stat])
plt.xlabel('Team')
plt.ylabel(selected_stat)
plt.title(f'{selected_stat} by Team')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
st.pyplot(plt)