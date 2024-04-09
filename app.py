import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to parse the date string to datetime
def parse_date(date):
    return pd.to_datetime(date)

# Function to plot the cumulative sum of Mass
def plot_cumulative_mass(df):
    df['Date'] = df['Date / YYYY-MM-DD'].apply(parse_date)
    df['Total Mass'] = df['Mass / kg'].cumsum()
    # Create figure
    fig = go.Figure()
    
    # Add line trace
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Total Mass'], mode='lines', name='Total Mass'))
    
    # Add filled area trace
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Total Mass'], fill='tozeroy', mode='none', fillcolor='rgba(0,100,80,0.2)', name=""))
    
    # Update layout
    fig.update_layout(title='Total Mass of Picked Litter', xaxis_title='Date', yaxis_title='Total Mass  /  kg')
    
    st.plotly_chart(fig)

# Streamlit app
def main():
    st.title('Trondheim Trash Data Hub')
    
    # Read data from CSV file
    url = 'https://raw.githubusercontent.com/jsimonclark/TrondheimTrash/main/data/MassData.csv'
    df = pd.read_csv(url) 
    
    # Plot cumulative sum of Mass
    #st.subheader('Cumulative Sum of Mass')
    plot_cumulative_mass(df)

if __name__ == "__main__":
    main()
