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
            
            # 1. Feature Engineering: Convert 'Time' and 'Date'
            # We remove the specific format to allow flexible parsing (e.g., 9:00:00 vs 09:00:00)
            df['Hour'] = pd.to_datetime(df['Time'], format='mixed', errors='coerce').dt.hour
            df['Day_Index'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce').dt.dayofweek

            # 2. Map Categorical Target to Numeric Values
            df['Traffic Situation'] = df['Traffic Situation'].str.strip().str.lower()
            mapping = {'low': 0, 'normal': 1, 'high': 2, 'heavy': 3}
            df['target'] = df['Traffic Situation'].map(mapping)

            # 3. Data Cleaning
            X = df[['Hour', 'Day_Index']]
            y = df['target']
            
            # Safety Check: Drop rows where time parsing failed
            X = X.dropna()
            y = y.loc[X.index]

            if len(X) == 0:
                print("❌ Training Error: No valid data found after parsing.")
                return

            # 4. Model Fitting
            self.model.fit(X, y)
            self.is_trained = True
            print(f"✅ AI Model Trained Successfully! ({len(X)} rows processed)")

        except Exception as e:
            print(f"❌ Error training model: {e}")
    
    def predict_density(self, hour, day_index):
        if not self.is_trained:
            return 0.4
        
        # Create DataFrame with matching feature names to avoid UserWarnings
        input_data = pd.DataFrame([[hour, day_index]], columns=['Hour', 'Day_Index'])
        
        # Predict traffic class
        prediction_class = self.model.predict(input_data)[0]
        
        # Map class back to density factor (0.0 to 1.0)
        density_map = {0: 0.2, 1: 0.4, 2: 0.7, 3: 1.0}
        return density_map.get(prediction_class, 0.4)

if __name__ == "__main__":
    ai = traffic_prediction()
    
    # Path to your dataset
    path = r'data\Traffic.csv'
    
    ai.train_from_csv(path)

    if ai.is_trained:
        # Test Case: 8 AM on a Monday (Day_Index 0)
        res = ai.predict_density(8, 0)
        print(f"Predicted Density at 8 AM: {res} (From AI Model)")