import pickle
import pandas as pd
import numpy as np

class Recommender:
    def __init__(self, model_path, data_path):
        with open(model_path, 'rb') as model_file:
            self.model = pickle.load(model_file)
            self.data = np.load(data_path)

    def recommend(self, tour_id, original_data, num_recommendations=3):
        distances, indices = self.model.kneighbors(self.data[tour_id].reshape(1, -1), n_neighbors=20)
        neighbor_indices = indices[0][1:]
        neighbor_distances = distances[0][1:]
        return self._pick_top_neighbours(tour_id, neighbor_indices, num_recommendations, original_data)
    
    def _pick_top_neighbours(self, tour_id, neighbor_indices, num_recommendations, original_data ):
        tour = original_data.iloc[tour_id]
        nearest_rows = original_data.iloc[neighbor_indices].loc[original_data['tour_id'] != tour['tour_id']].drop_duplicates(subset='tour_id', keep='first')
        return pd.concat([tour.to_frame().T, nearest_rows]).head(num_recommendations + 1)
