import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import RDFS

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

# Function to parse JSON-LD data into a graph
def parse_jsonld(jsonld_data):
    graph = Graph()
    graph.parse(data=jsonld_data, format='json-ld')
    return graph

# Function to display location coordinates on a map
def display_map(graph):
    # Define the SPARQL query to retrieve latitude and longitude
    query = """
    PREFIX schema: <http://schema.org/>
    SELECT ?latitude ?longitude
    WHERE {
        ?place a schema:Place .
        ?place schema:latitude ?latitude .
        ?place schema:longitude ?longitude .
    }
    """

    # Execute the query
    results = graph.query(query)

    # Process the results into a DataFrame
    locations = []
    for row in results:
        latitude = float(row['latitude'])
        longitude = float(row['longitude'])
        locations.append({'latitude': latitude, 'longitude': longitude})
    
    if locations:
        df = pd.DataFrame(locations)
        st.map(df)
    else:
        st.write("No locations found.")

def add_multiselect_options(graph):
    # Define the SPARQL query to retrieve photograph labels
    query = """
    PREFIX schema: <http://schema.org/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE {
        ?photo a schema:Photograph .
        ?photo schema:about ?subject .
        ?subject rdfs:label ?label .
    }
    """

    # Execute the query
    results = graph.query(query)

    # Extract the labels from the query results and remove duplicates
    options = list(set(str(row['label']) for row in results))

    # Use Streamlit multiselect to select photographs
    selected_options = st.multiselect("Select Photographs", options)
    return selected_options

# Function to retrieve and display selected images
def display_selected_images(graph, selected_options):
    # Define the SPARQL query to retrieve photograph URLs based on selected options
    query = """
    PREFIX schema: <http://schema.org/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?photo ?url
    WHERE {
        ?photo a schema:Photograph .
        ?photo schema:about ?subject .
        ?subject rdfs:label ?label .
        ?photo schema:url ?url .
        FILTER(?label IN (%s))
    }
    """ % ', '.join(['"' + option + '"' for option in selected_options])

    # Execute the query
    results = graph.query(query)

    # Display images for each selected photograph URL
    for row in results:
        st.image(str(row['url']))

# Streamlit app
def main():
    st.title('Trondheim Trash Data Hub')
    
    # Read data from CSV file
    csv_url = 'https://raw.githubusercontent.com/jsimonclark/TrondheimTrash/main/data/MassData.csv'
    df = pd.read_csv(csv_url) 

    # Read data from json-ld file
    jsonld_url = 'https://raw.githubusercontent.com/jsimonclark/TrondheimTrash/main/data/TrondheimTrash.json'
    
    # Plot cumulative sum of Mass
    #st.subheader('Cumulative Sum of Mass')
    plot_cumulative_mass(df)

    # Retrieve JSON-LD data from the URL
    response = requests.get(jsonld_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON-LD data into an RDF graph
        graph = parse_jsonld(response.text)
        print("Data retrieved successfully and parsed into an RDF graph.")
    else:
        print("Failed to retrieve JSON-LD data. Status code:", response.status_code)
    
    # Add multi-select options for photographs
    selected_options = add_multiselect_options(graph)

    # Display location coordinates on a map
    st.subheader('Location Map')
    display_map(graph)

    display_selected_images(graph, selected_options)

if __name__ == "__main__":
    main()
