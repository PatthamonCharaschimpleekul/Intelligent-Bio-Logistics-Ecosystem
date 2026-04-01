import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os

class traffic_prediction:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        self.is_trained = False
    
    def train_from_csv(self, file_path):
        try:
            df = pd.read_csv(file_path)
            
            # 1. Convert 'Time' column to actual numbers (Hours)
            # This turns "08:30:00" into 8.0
            df['Hour'] = pd.to_datetime(df['Time']).dt.hour
            
            # 2. Convert 'Day of the week' to numbers (0-6)
            # Machine Learning models only understand numbers!
            df['Day_Index'] = pd.to_datetime(df['Date']).dt.dayofweek

            # 3. Standardize 'Traffic Situation' and Map to Target
            df['Traffic Situation'] = df['Traffic Situation'].str.strip().str.lower()
            mapping = {'low': 0, 'normal': 1, 'high': 2, 'heavy': 3}
            df['target'] = df['Traffic Situation'].map(mapping)

            # 4. Select Features and Target based on your CSV
            X = df[['Hour', 'Day_Index']]
            y = df['target']

            # 5. Drop any rows with missing data (safety check)
            X = X.dropna()
            y = y.loc[X.index]

            self.model.fit(X, y)
            self.is_trained = True
            print("✅ AI Model Trained Successfully!")

        except Exception as e:
            print(f"❌ Error training model: {e}")
    
    def predict_density(self, hour, day_index):
        if not self.is_trained:
            return 0.4
        
        # Predict class and map back to density (0.0 - 1.0)
        prediction_class = self.model.predict([[hour, day_index]])[0]
        density_map = {0: 0.2, 1: 0.4, 2: 0.7, 3: 1.0}
        return density_map.get(prediction_class, 0.4)

if __name__ == "__main__":
    ai = traffic_prediction()
    
    # Use your absolute path here
    path = 'data\Traffic.csv'
    
    ai.train_from_csv(path)

    if ai.is_trained:
        # Test: 8 AM on a Monday (Day_Index 0)
        res = ai.predict_density(8, 0)
        print(f"Predicted Density at 8 AM: {res} (From AI Model)")