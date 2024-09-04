import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2025))))  # Extended year range to include recent years

# Web scraping of NBA player stats
@st.cache_data  # Updated caching method to avoid deprecation warnings
def load_data(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)  # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats

# Load data based on selected year
playerstats = load_data(selected_year)

# Ensure 'Team' column values are strings
if 'Team' in playerstats.columns:  # Check if 'Team' column exists
    playerstats['Team'] = playerstats['Team'].astype(str)  # Convert to string to avoid sorting issues
    sorted_unique_team = sorted(playerstats['Team'].unique())
    selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)
else:
    st.warning("The 'Team' column is not found. Skipping team selection.")
    selected_team = []

# Sidebar - Position selection
unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats['Team'].isin(selected_team)) & (playerstats['Pos'].isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write(f'Data Dimension: {df_selected_team.shape[0]} rows and {df_selected_team.shape[1]} columns.')
st.dataframe(df_selected_team)

# Download NBA player stats data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    
    # Filter the DataFrame to include only numeric columns
    numeric_df = df_selected_team.select_dtypes(include=[np.number])
    
    if numeric_df.empty:
        st.error("No numeric data available for correlation matrix.")
    else:
        corr = numeric_df.corr()  # Calculate the correlation matrix
        mask = np.triu(np.ones_like(corr, dtype=bool))  # Mask for upper triangle
        plt.figure(figsize=(14, 14))
        sns.heatmap(corr, mask=mask, vmax=1, square=True, annot=True, fmt='.2f', cmap='coolwarm')
        st.pyplot(plt)  # Display the heatmap
