import pandas as pd
import numpy as np

class KMeansRecommender:

    def __init__(self, clusters_csv_path):
        self.clusters_data = pd.read_csv(clusters_csv_path)

    def recommend(self, tour_id, original_data, num_recommendations=3):
        # Identify the cluster of the input tour
        cluster_label = self.clusters_data.loc[tour_id, 'cluster']
        
        # Get the indices of tours in the same cluster
        similar_tours_indices = self.clusters_data[self.clusters_data['cluster'] == cluster_label].index.tolist()
        
        # Filter out the input tour
        recommended_indices = [idx for idx in similar_tours_indices if idx != tour_id]
        
        # Get unique tour_ids within the same cluster, keeping the first occurrence
        recommended_unique_indices = original_data.loc[recommended_indices].drop_duplicates(subset='tour_id', keep='first').index.tolist()
        
        # If there are fewer unique recommendations available than requested, then adjust the number of recommendations to return
        num_recommendations = min(num_recommendations, len(recommended_unique_indices))
        
        # Sample the required number of unique recommendations
        sampled_recommendations = np.random.choice(recommended_unique_indices, num_recommendations, replace=False)
        
        # Concatenate with the target tour and return the details of the recommended tours
        final_recommendations = [tour_id] + sampled_recommendations.tolist()
        return original_data.loc[final_recommendations]
