import streamlit as st
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt  
import plotly.express as px
import calendar

class StatisticalAnalysis:
    def __init__(self):
        self.data = pd.read_csv('data/processed/analysis.csv').dropna()
        self.locations_visited = pd.read_csv('data/processed/locations_visited.csv').dropna()
        self.departures = pd.read_csv('data/processed/departures.csv').dropna()

    def show(self):
        st.title("Statistical Analysis")

        # Display Descriptive Statistics
        st.subheader('Descriptive Statistics')
        st.table(self.data[[
            'number_of_tourOptions',
            'number_of_unique_countries',
            'number_of_locations_visited',
            'full_price_min',
            'full_price_max',
            'number_of_days'
            ]]
            .describe().T)

        st.subheader('Frequency of Countries Visited')
        country_freq = self.locations_visited['countryCode'].value_counts().reset_index()
        country_freq.columns = ['Country Code', 'Frequency']
        country_freq = country_freq.sort_values(by='Frequency', ascending=False)

        fig = px.bar(country_freq, x='Country Code', y='Frequency', text='Frequency')
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        st.plotly_chart(fig)

        # Calculate and Display Correlations
        st.subheader('Correlation Analysis')
        correlation_matrix = self.data[['full_price_min', 'number_of_days', 'number_of_locations_visited']].corr()
        st.table(correlation_matrix)

        # Display Heatmap of Correlations
        fig, ax = plt.subplots(figsize=(6,4))  # Set the figure size while creating the subplot
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)  # You can use ax parameter to draw on the correct axes.
        st.pyplot(fig)

        
        fig, ax = plt.subplots(figsize=(10,6))

        # Plotting the scatter plot along with a regression line
        sns.regplot(x='full_price_min', y='number_of_days', data=self.data, scatter_kws={'s':10}, line_kws={'color': 'red'}, ax=ax)

        ax.set_title('Relationship between Price and Number of Days')
        ax.set_xlabel('Minimum Full Price')
        ax.set_ylabel('Number of Days')

        st.pyplot(fig)


        fig, ax = plt.subplots(figsize=(10,6))

        # Plotting the scatter plot along with a regression line
        sns.regplot(x='full_price_min', y='number_of_locations_visited', data=self.data, scatter_kws={'s':10}, line_kws={'color': 'red'}, ax=ax)

        ax.set_title('Relationship between Price and Number of Locations Visited')
        ax.set_xlabel('Minimum Full Price')
        ax.set_ylabel('Number of Locations Visited')

        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(10,6))
        self.departures['start_month'] = pd.to_datetime(self.departures['startDate']).dt.month_name()
        tours_per_month = self.departures['start_month'].value_counts().sort_index()
        tours_per_month = tours_per_month.reindex(calendar.month_name[1:])
        tours_per_month.plot(kind='bar', ax=ax)

        ax.set_title('Number of Tours per Month')
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Tours')

        st.pyplot(fig)
