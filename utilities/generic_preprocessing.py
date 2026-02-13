import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess(input_csv_path):
    """
    Processes a 20-column student dataset:
    1. Maps descriptive categorical values to numeric.
    2. Inverts "Negative" features (Distance, Disabilities) so 1.0 = Better.
    3. Scales all numeric columns to 0-1 range based on the file's distribution.
    4. Reduces dimensions to the requested 8-column thematic dataframe.
    """
    
    # Load the dataframe
    df = pd.read_csv(input_csv_path)

    # 1. CATEGORICAL MAPPING
    mapping_dict = {
        'Parental_Involvement': {'Low': 0, 'Medium': 1, 'High': 2},
        'Access_to_Resources': {'Low': 0, 'Medium': 1, 'High': 2},
        'Motivation_Level': {'Low': 0, 'Medium': 1, 'High': 2},
        'Family_Income': {'Low': 0, 'Medium': 1, 'High': 2},
        'Teacher_Quality': {'Low': 0, 'Medium': 1, 'High': 2},
        'Extracurricular_Activities': {'No': 0, 'Yes': 1},
        'Internet_Access': {'No': 0, 'Yes': 1},
        'Learning_Disabilities': {'No': 0, 'Yes': 1},
        'School_Type': {'Public': 0, 'Private': 1},
        'Peer_Influence': {'Negative': 0, 'Neutral': 1, 'Positive': 2},
        'Parental_Education_Level': {'High School': 0, 'College': 1, 'Postgraduate': 2},
        'Distance_from_Home': {'Near': 0, 'Moderate': 1, 'Far': 2},
        'Gender': {'Female': 0, 'Male': 1}
    }

    # Apply mapping to categorical columns present in df
    for col, m in mapping_dict.items():
        if col in df.columns:
            df[col] = df[col].map(m).fillna(0)

    # 2. INVERSION OF NEGATIVE FEATURES (from scale.py logic)
    # Ensure 1.0 always means "Better for Success"
    if 'Distance_from_Home' in df.columns:
        df['Distance_from_Home'] = df['Distance_from_Home'].max() - df['Distance_from_Home']
    
    if 'Learning_Disabilities' in df.columns:
        df['Learning_Disabilities'] = df['Learning_Disabilities'].max() - df['Learning_Disabilities']

    # 3. DYNAMIC MIN-MAX SCALING
    # Scale all columns except IDs or non-numeric metadata if any
    scaler = MinMaxScaler()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # 4. DIMENSIONALITY REDUCTION (Target: 8 Columns)
    reduced_df = pd.DataFrame()
    
    # Direct mappings (The 4 core academic features)
    reduced_df['Hours_Studied'] = df['Hours_Studied']
    reduced_df['Attendance'] = df['Attendance']
    reduced_df['Previous_Scores'] = df['Previous_Scores']
    reduced_df['Motivation_Level'] = df['Motivation_Level']


    # Theme 1: Resource Access (Socio-economic & School Tools)
    reduced_df['Resource_Access'] = df[['Access_to_Resources', 'Internet_Access', 'Tutoring_Sessions', 'Family_Income', 
    'Teacher_Quality', 'School_Type']].mean(axis=1)

    # Theme 2: Family Capital (Home Support)
    reduced_df['Family_Capital'] = df[['Parental_Involvement', 
    'Parental_Education_Level']].mean(axis=1)

    # Theme 3: Personal Wellbeing (Lifestyle)
    reduced_df['Personal_Wellbeing'] = df[['Sleep_Hours', 'Physical_Activity', 
   'Extracurricular_Activities']].mean(axis=1)

    # Theme 4: Environmental Stability (External Factors)
    reduced_df['Environmental_Stability'] = df[['Peer_Influence', 'Distance_from_Home', 'Learning_Disabilities']].mean(axis=1)


    return reduced_df

