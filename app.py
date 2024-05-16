
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


# history graph
y0 = playerstats[['Tm','H','HR','R']]
y1 = load_data(selected_year - 1)[['Tm','H','HR','R']]
y2 = load_data(selected_year - 2)[['Tm','H','HR','R']]
y3 = load_data(selected_year - 3)[['Tm','H','HR','R']]

y0['Year'] = selected_year 
y1['Year'] = selected_year - 1
y2['Year'] = selected_year - 2
y3['Year'] = selected_year - 3


# Combine datasets
combined_data = [y0, y1, y2, y3]
years = [selected_year, selected_year - 1, selected_year - 2, selected_year - 3]

# Set colors for each year
colors = ['red', 'blue', 'green', 'orange']

# Create subplots for each statistic
fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

# Plot scatter plot for each statistic
for i, stat in enumerate(['H', 'HR', 'R']):
    for j, data in enumerate(combined_data):
        axs[i].scatter(data[stat], data['Tm'], label=str(years[j]), color=colors[j], alpha=0.7)
    axs[i].set_xlabel(stat)

# Set common y-axis label and title
fig.text(0.5, 0.04, 'Teams (Tm)', ha='center')
fig.suptitle('Scatter Plots of Hits (H), Home Runs (HR), and Runs (R)')

# Add legend to the last subplot
axs[-1].legend()

# Show plot
plt.tight_layout()
plt.show()


# # Display plot in Streamlit
st.pyplot(plt)
