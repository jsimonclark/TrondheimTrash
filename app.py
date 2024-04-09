import streamlit as st
import pandas as pd
import plotly.express as px

# Function to parse the date string to datetime
def parse_date(date):
    return pd.to_datetime(date)

# Function to plot the cumulative sum of Mass
def plot_cumulative_mass(df):
    df['Date'] = df['Date / YYYY-MM-DD'].apply(parse_date)
    df['Cumulative Mass'] = df['Mass / kg'].cumsum()
    fig = px.line(df, x='Date', y='Cumulative Mass', title='Cumulative Sum of Mass Over Time')
    st.plotly_chart(fig)

# Streamlit app
def main():
    st.title('Cumulative Sum of Mass')
    
    # Read data from CSV file
    url = 'https://raw.githubusercontent.com/jsimonclark/TrondheimTrash/main/data/MassData.tsv'
    df = pd.read_csv(url, sep='\s{3,}', engine='python') 
    
    # Display raw data
    st.subheader('Raw Data')
    st.write(df)
    
    # Plot cumulative sum of Mass
    st.subheader('Cumulative Sum of Mass')
    plot_cumulative_mass(df)

if __name__ == "__main__":
    main()
