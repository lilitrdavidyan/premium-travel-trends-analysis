# geographical_segmentation.py
import streamlit as st
import pandas as pd  
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import plotly.express as px
from folium.plugins import MarkerCluster
import re
from branca.element import IFrame
import math


class PriceHeatMap:
    def __init__(self):
        self.data = pd.read_csv('data/processed/analysis.csv').dropna()
        # Rename the "Decc" column to "Dec"
        self.data.rename(columns={'Decc': 'Dec'}, inplace=True)

        # perform any other initialization steps
        pass

    def show(self):
        st.write("Interactive Map")
        
        list_of_countries= ['AL', 'AM', 'AR', 'AT', 'AU', 'BA', 'BE', 'BG', 'BR', 'BW', 'CA', 'CH', 'CL', 'CN', 'CR', 'CZ', 'DE', 'DK', 'EC', 'EG', 'EE', 'ES', 'FI', 'FR', 'GB', 'GE', 'GI', 'GR', 'HR', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KE', 'KH', 'KR', 'LA', 'LI', 'LK', 'LS', 'LT', 'LU', 'LV', 'MA', 'MC', 'MG', 'MK', 'MT', 'MV', 'MY', 'NE', 'NL', 'NO', 'NP', 'NZ', 'PE', 'PL', 'PT', 'RO', 'RS', 'RW', 'SE', 'SG', 'SI', 'SK', 'TH', 'TR', 'TW', 'TZ', 'UG', 'US', 'UY', 'VA', 'VN', 'ZA', 'ZM', 'ZW']
        list_of_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


        # Create widgets for filtering
        selected_countries = st.multiselect('Select Countries', list_of_countries)
        selected_months = st.multiselect('Select Months', list_of_months)
    
        # Get the minimum and maximum price from the data
        min_price = self.data['full_price_min'].min()
        max_price = self.data['full_price_max'].max()
        min_price_rounded_down = (min_price // 100) * 100
        max_price_rounded_up = math.ceil(max_price / 100) * 100

        # Create a price range slider
        price_range = st.slider('Select Price Range', min_value=int(min_price_rounded_down), max_value=int(max_price_rounded_up), value=(int(min_price_rounded_down), int(max_price_rounded_up)), step=100)

        # Adding Duration Range Slider
        min_duration = self.data['number_of_days'].min()
        max_duration = self.data['number_of_days'].max()
        duration_range = st.slider('Select Duration Range', min_value=int(min_duration), max_value=int(max_duration), value=(int(min_duration), int(max_duration)), step=1)


        # Filter data based on user input
        filtered_data = self.data

        # st.dataframe(filtered_data)

        if selected_countries:
            # Create a pattern to match any of the selected_countries
            pattern = '|'.join(re.escape(country) for country in selected_countries)
            
            # Filter the DataFrame to include rows where 'country_codes' column contains any of the selected_countries
            filtered_data = filtered_data[filtered_data['country_codes'].str.contains(pattern, na=False, regex=True)]
        
        # Filtering by selected months
        if selected_months:
            # Convert selected complete month names to their short form for filtering
            month_abbreviations = [month[:3] for month in selected_months]
            # Filtering the DataFrame to include rows where any of the selected_months is 1
            filtered_data = filtered_data[filtered_data[month_abbreviations].eq(1).any(axis=1)]
        
        # Filter data based on the selected price range
        filtered_data = filtered_data[
            filtered_data['full_price_min'].between(price_range[0], price_range[1]) | 
            filtered_data['full_price_max'].between(price_range[0], price_range[1]) |
            ((filtered_data['full_price_min'] < price_range[0]) & (filtered_data['full_price_max'] > price_range[1]))
        ]

        filtered_data = filtered_data[(filtered_data['number_of_days'] >= duration_range[0]) & (filtered_data['number_of_days'] <= duration_range[1])]
        
        # Display heat map with the filtered data
        self.display_heat_map(filtered_data)
        self.display_table(filtered_data)

    def price_to_color(self, price_min):
        if price_min <= 2000:
            return 'green'
        elif price_min <= 5000:
            return 'blue'
        elif price_min <= 10000:
            return 'yellow'
        elif price_min <= 15000:
            return 'orange'
        else:
            return 'red'

    def display_heat_map(self, filtered_data):
        # Initialize the map
        m = folium.Map(location=[20, 0], zoom_start=2)

        # Prepare data for the heat map
        heat_data = [[row['mean_lat'], row['mean_long'], row['full_price_min']] for index, row in filtered_data.iterrows()]

        # Add heat map layer to the map
        HeatMap(heat_data).add_to(m)
        
        # Display the map in Streamlit
        folium_static(m)


    def display_table(self, filtered_data):
        st.write(filtered_data)
