
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
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1980,2025))))

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


# # history graph
# y0 = playerstats[['Tm','H','HR','R']]
# y1 = load_data(selected_year - 1)[['Tm','H','HR','R']]
# y2 = load_data(selected_year - 2)[['Tm','H','HR','R']]
# y3 = load_data(selected_year - 3)[['Tm','H','HR','R']]

# y0['Year'] = selected_year 
# y1['Year'] = selected_year - 1
# y2['Year'] = selected_year - 2
# y3['Year'] = selected_year - 3

# # Combine all years into one DataFrame
# combined_df = pd.concat([y0, y1, y2, y3])


# # Melt the DataFrame to have 'Year' as id variable
# melted_df = pd.melt(combined_df, id_vars=['Year', 'Tm'], var_name='Stat', value_name='Value')
# print(melted_df.to_numeric(s, errors='ignore'))
# print(melted_df.dtypes)

# # Filter DataFrame for the selected team
# selected_team_df = melted_df[melted_df['Tm'] == selected_team]

# # Plotting using Matplotlib scatter plot
# plt.figure(figsize=(10, 6))

# for year in selected_team_df['Year'].unique():
#     year_data = selected_team_df[selected_team_df['Year'] == year]
#     plt.scatter(year_data['Stat'], year_data['Value'], label=str(year))
#     plt.plot(year_data['Stat'], year_data['Value'], marker='o', linestyle='-')

# plt.title('Team A Stats Over the Years')
# plt.xlabel('Stat')
# plt.ylabel('Value')
# plt.legend()

# # Display plot in Streamlit
# st.pyplot(plt)
