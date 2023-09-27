import pandas as pd
from geopy.distance import geodesic

class ProximityRecommender:

    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
    
    def recommend(self, tour_id, original_data, num_recommendations = 3) -> pd.DataFrame:
        target_tour = self.data.loc[tour_id]
        target_coords = (target_tour['latitude_mean'], target_tour['longitude_mean'])
        
        # Calculate distances
        self.data['distance'] = self.data.apply(
            lambda row: geodesic(target_coords, (row['latitude_mean'], row['longitude_mean'])).km, axis=1
        )
        
        target_tour_original = original_data.iloc[[tour_id]]  
        
        # Sort by distance and get top recommendations, excluding the input tour_id
        recommendation_indexes = self.data[self.data.index != tour_id].sort_values(by='distance').index.tolist()

        # Extract the target tour and recommendations from the original_data DataFrame
        
        recommendations_original = original_data.iloc[recommendation_indexes]
        
        # Concatenate the recommendations with target_tour
        result = pd.concat([target_tour_original, recommendations_original])
        
        # Drop duplicate tour_id rows, keeping the first occurrence
        result_unique_tours = result.drop_duplicates(subset='tour_id', keep='first')
        
        # Ensure the target tour is included in the result
        if tour_id not in result_unique_tours.index:
            result_unique_tours = pd.concat([target_tour_original, result_unique_tours])
        
        return result_unique_tours.head(num_recommendations + 1)

