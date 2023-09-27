import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class CosineSimilarityRecommender:
    def __init__(self, feature_matrix_path):
        self.feature_matrix = np.load(feature_matrix_path)  
        self.similarity_matrix = cosine_similarity(self.feature_matrix)
        
    def recommend(self, tour_id, original_data, num_recommendations=3) -> pd.DataFrame:
        # Get the top-k similar tours for a given tour
        top_k = 20 #num_recommendations + 1  # Including the tour itself
        similar_tours_indexes = self.similarity_matrix[tour_id].argsort()[::-1][:top_k][1:]  # Exclude the tour itself
        
        # Extract the target tour and recommendations from the original_data DataFrame
        target_tour = original_data.iloc[[tour_id]]
        recommendations = original_data.iloc[similar_tours_indexes]
        
        # Concatenate the recommendations with target_tour
        result = pd.concat([target_tour, recommendations])
        
        # Drop duplicate tour_id rows, keeping the first occurrence
        result_unique_tours = result.drop_duplicates(subset='tour_id', keep='first')
        
        return result_unique_tours.head(num_recommendations + 1)
