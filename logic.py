
import pandas as pd

class StrabismusSurgeryRecommender:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

    def recommend(self, strabismus_type, deviation, approach):
        # Filter dataframe for matching criteria
        df_filtered = self.df[
            (self.df['Strabismus_Type'] == strabismus_type) &
            (self.df['Approach'] == approach)
        ]
        # Find closest deviation (nearest prism diopters)
        closest_dev = df_filtered['Deviation_PD'].sub(deviation).abs().idxmin()
        row = df_filtered.loc[closest_dev]

        # Collect all rows with this deviation (because multiple muscles)
        matched_rows = df_filtered[df_filtered['Deviation_PD'] == row['Deviation_PD']]

        # Build recommendation dictionary
        recommendation = []
        for _, r in matched_rows.iterrows():
            recommendation.append({
                'Muscle': r['Muscle'],
                'Surgery_Type': r['Surgery_Type'],
                'Recession_mm': r['Recession_mm'],
                'Resection_mm': r['Resection_mm']
            })

        return recommendation
