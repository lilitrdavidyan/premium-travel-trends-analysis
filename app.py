import streamlit as st
from PIL import Image
from src.recommenders.recommender import Recommender
from src.recommenders.recommender_by_proximity import ProximityRecommender
from src.recommenders.recommender_by_cosine_similarity import CosineSimilarityRecommender
from src.recommenders.recommender_KMeans import KMeansRecommender
from src.analysis.geographical_segmentation import GeographicalSegmentation
from src.analysis.analysis_facade import AnalysisFacade

import pandas as pd


# Load the webp image
image_path = "assets/banner.webp"
webp_image = Image.open(image_path)

st.set_page_config(layout='wide')

analysis_facade = AnalysisFacade()

# Sidebar with radio buttons as menu items
option = st.sidebar.radio('Choose a section:', ('Recommenders', 'Interactive Map', 'Heat Map', 'Statistical Analysis'))

if option == 'Interactive Map':
    analysis_facade.show_geographical_segmentation()
elif option == 'Heat Map':
    analysis_facade.show_heat_map()
elif option == 'Statistical Analysis':
    analysis_facade.show_statistical_analysis()

elif option == 'Recommenders':
    st.image(webp_image, use_column_width=True)
    st.title('Similar Tour Recommender')

    file_path = 'data/processed/merged.csv'
    original_data = pd.read_csv(file_path)
    
    # List of Recommender Models
    recommenders = {
        'NearestNeighbours Text Only': Recommender('models/nearest_neighbors_text_only.pkl', 'notebooks/text_vectorization/embeddings/all_embeddings_merged.npy'),
        'NearestNeighbours All Data': Recommender('models/nearest_neighbors_all_features.pkl', 'data/processed/final_array.npy'),
        'Recommender by Proximity': ProximityRecommender('data/processed/mean_lat_long.csv'),
        'Cosine Similarity Recommender': CosineSimilarityRecommender('data/processed/final_array.npy'),
        'KMeans Recommender': KMeansRecommender('data/processed/clusters.csv')

    }
    
    # Dropdown for Recommender Selection
    selected_recommender = st.selectbox("Select a Recommender Model", recommenders.keys())
    
    # Model Description/Details
    if selected_recommender == 'NearestNeighbours Text Only':
        st.write('''This Nearest Neighbors model was trained exclusively on BERT-encoded text features.''')
    elif selected_recommender == "NearestNeighbours All Data":
        st.write('''This Nearest Neighbors model was trained on BERT-encoded text features as well as encoded and sclaed categorical and numerical features.''')
    elif selected_recommender == 'Recommender by Proximity':
        st.write("This model recommends tours based on geographical proximity.")
    elif selected_recommender == "Cosine Similarity Recommender":
        st.write("This recommender suggests tours that have high cosine similarity with the selected tour.")
    elif selected_recommender == "KMeans Recommender":
        st.write("This recommender suggests tours that are in the same cluster as the selected tour.")
    else:  
        st.write("Please select a recommender.")
    
    # Taking user input
    user_input = st.text_input("Enter tour id:")

    if user_input:  
        try:
            user_input = int(user_input)  
            if user_input < 0 or user_input > 772:  
                st.warning("Please enter a number between 0 and 772")
                user_input = None  # Reset user_input
        except ValueError:  # This will be executed if user_input cannot be converted to an integer
            st.warning("Please enter a valid number between 0 and 772")
            user_input = None  # Reset user_input

    # Button to Get Recommendations
    if st.button("Get Recommendations"):
        if user_input is not None:  # This will be True if user_input is a valid number between 1 and 773
            # Generate and Display Recommendations based on selected recommender
            st.write(f"Recommendations from '{selected_recommender}' for Tour: ", user_input)
            st.write(recommenders[selected_recommender].recommend(user_input, original_data).T)
        else:
            st.warning("Please enter a valid tour id before getting recommendations")
