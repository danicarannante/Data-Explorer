import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import requests

st.set_page_config(
    page_title="MLB Data Explorer"
)

st.title('Major League Baseball Stat Explorer')
st.write('To view a stat across all teams use the side bar menu to select a year and stat')
# st.markdown("""
# This app performs simple webscraping of NBA player stats data!
# * **Python libraries:** base64, pandas, streamlit
# * **Data source:** [Baseball-reference.com](https://www.baseball-reference.com/).
# """)

selected_year = st.sidebar.selectbox('Year', list(reversed(range(1980,2024))))

# Web scraping of NBA player stats
@st.cache_data
def load_data(year):
    url = "https://www.baseball-reference.com/leagues/majors/" + str(year) + ".shtml"
    response = requests.get(url)
    html = pd.read_html(response.content)
    df = html[0]
    filtered = df.drop(df[df.Tm == 'Tm'].index).drop(df[df.Tm == 'League Average'].index).dropna() # Deletes repeating headers in content
    return filtered

df = load_data(selected_year) # raw input 

# Convert non-numeric columns to numeric 
numeric_cols = df.columns[1:]  #  first column is 'Team'
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# # Display DataFrame
# st.write(df)

# Create a bar graph
selected_stat = st.sidebar.selectbox('Statistic:', numeric_cols)
plt.figure(figsize=(10, 6))
plt.bar(df['Tm'], df[selected_stat])
plt.xlabel('Team')
plt.ylabel(selected_stat)
plt.title(f'{selected_stat} by Team')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
st.pyplot(plt)