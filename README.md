# Premium Travel Trends Analysis and Recommender System

## Project Overview: 
This project performs a multifaceted analysis and builds a recommendation system focusing on tours provided by the Luxury Escapes tour operator. Developed as part of the Ironhack Bootcamp final project, it blends advanced analytical and machine learning techniques to deliver insights and personalized tour suggestions.

## Project Structure

    ├── README.md  # Documentation about the project, how to set up and run, etc.
    ├── app.py  # Main application file, containing the entry point for the Streamlit application.
    ├── assets # Static assets like images.
    ├── config
    │   └── config.yaml  # Configuration file, storing settings, constants, etc.
    ├── data  # Processed and raw data.
    │   ├── processed  # Processed data, which is ready to be used by models or for analysis.
    │   └── raw  # Raw data acquired from the source.
    ├── database  # SQL scripts and database schema related files.
    ├── logs # Log file for the application, logging events, errors, etc.
    ├── models  # Folder to store model related files, like trained models.
    ├── notebooks  # Jupyter notebooks for EDA and modeling
    │   ├── data_acquisition.ipynb  # Notebook for acquiring data.
    │   ├── eda  # Exploratory Data Analysis notebooks and helper scripts.
    │   ├── preprocessing  # Notebooks for preprocessing of data.
    │   ├── recommendations  # Notebooks related to recommendation algorithms and models.
    │   └── text_vectorization  # Notebooks and files related to text embedding or vectorization.
    ├── plots  # Storing plot images.
    ├── requirements.txt  # List of required Python packages for the project.
    └── src  # Source code directory.
        ├── analysis  # Python files related to data analysis.
        ├── data_acquisition  # Python files for acquiring data.
        ├── data_processing  # Python files related to data processing.
        ├── database_handler.py  # Python file to handle database interactions.
        └── recommenders  # Python files related to recommendation algorithms and models.

## Features
- **Interactive Visualizations:** Offers insights through interactive maps, heat maps, and statistical visualizations, enabling users to explore various aspects of the tours.
- **Recommendation System:** Utilizes methodologies like BERT embeddings for text data and other machine learning models, offering tailored tour suggestions.

## Data Acquisition and Processing
Data, meticulously retrieved utilizing the backend API of the Luxury Escapes website, was consolidated into JSON files and structured in SQL after a rigorous review. Each file encapsulates more than 10,000 rows, forming the foundation for subsequent analysis and modeling.

## Usage
Users can interact with the application to explore tours using interactive visualizations and receive personalized tour recommendations by inputting specific tour IDs and selecting the preferred recommender model.
