import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
# included for linear regression
import os
import joblib

def mapped_scaled(df):
    #numerical encoding
    df_mapped = df.copy()

    # Fill missing values with the most common value for each column before mapping
    for col in ['Teacher_Quality', 'Parental_Education_Level', 'Distance_from_Home']:
        if col in df_mapped.columns:
            df_mapped[col] = df_mapped[col].fillna(df_mapped[col].mode()[0])
    
    # 1. CATEGORICAL MAPPING
    # We map these so that higher numbers generally represent 'more' of a trait
    mapping_dict = {
        'Parental_Involvement': {'Low': 0, 'Medium': 1, 'High': 2},
        'Access_to_Resources': {'Low': 0, 'Medium': 1, 'High': 2},
        'Motivation_Level': {'Low': 0, 'Medium': 1, 'High': 2},
        'Family_Income': {'Low': 0, 'Medium': 1, 'High': 2},
        'Teacher_Quality': {'Low': 0, 'Medium': 1, 'High': 2},
        'Extracurricular_Activities': {'No': 0, 'Yes': 1},
        'Internet_Access': {'No': 0, 'Yes': 1},
        'Learning_Disabilities': {'No': 1, 'Yes': 0}, #no is better so 1 
        'School_Type': {'Public': 0, 'Private': 1}, #these are categories
        'Peer_Influence': {'Negative': 0, 'Neutral': 1, 'Positive': 2},
        'Gender': {'Male': 0, 'Female': 1}, #these are categories
        'Distance_from_Home': {'Near': 2, 'Moderate': 1, 'Far': 0}, # Inverted so that Near is better
        'Parental_Education_Level': {'Basic': 0, 'High School': 1, 'College': 2, 'Postgraduate': 3}
    }

    for col, val_map in mapping_dict.items():
        if col in df_mapped.columns:
            df_mapped[col] = df_mapped[col].map(val_map)

    return df_mapped


def persona_reduction(df_mapped):
    """
    Step 2: 8-Column Feature Reduction (Thematic)
    Combines 20 columns into 8 core dimensions for clustering.
    """
    reduced_df = pd.DataFrame(index=df_mapped.index)

    # Individual Direct Metrics
    reduced_df['Hours_Studied'] = df_mapped['Hours_Studied']
    reduced_df['Attendance'] = df_mapped['Attendance']
    reduced_df['Previous_Scores'] = df_mapped['Previous_Scores']
    reduced_df['Motivation_Level'] = df_mapped['Motivation_Level']

    # Theme 1: Resource Access (Socio-economic & School Tools)
    # Mean of: Access to Resources, Internet, Tutoring, Income, Teacher Quality
    res_cols = ['Access_to_Resources', 'Internet_Access', 'Tutoring_Sessions', 
                'Family_Income', 'Teacher_Quality']
    reduced_df['Resource_Access'] = df_mapped[res_cols].mean(axis=1)

    # Theme 2: Family Capital (Home Support)
    fam_cols = ['Parental_Involvement', 'Parental_Education_Level']
    reduced_df['Family_Capital'] = df_mapped[fam_cols].mean(axis=1)

    # Theme 3: Personal Wellbeing (Lifestyle)
    well_cols = ['Sleep_Hours', 'Physical_Activity', 'Extracurricular_Activities']
    reduced_df['Personal_Wellbeing'] = df_mapped[well_cols].mean(axis=1)

    # Theme 4: Environmental Stability (External Factors)
    env_cols = ['Peer_Influence', 'Distance_from_Home', 'Learning_Disabilities']
    reduced_df['Environmental_Stability'] = df_mapped[env_cols].mean(axis=1)
    

    
    
    # 2. GLOBAL MIN-MAX SCALING
    # This squashes everything into a 0.0 to 1.0 range
    scaler = StandardScaler()
    reduced_df[reduced_df.columns] = scaler.fit_transform(reduced_df)

    return reduced_df

def academic_reduction(df_mapped):
    """
    Step 2b: 2-Column Feature Reduction
    Focuses strictly on academic performance metrics.
    """
    
    # predict scores for beginning of sem analysis (when 19 col are given) and use Exam_Score column if it's already given
    was_predicted=False
    if 'Exam_Score' not in df_mapped.columns or df_mapped['Exam_Score'].isnull().all():
        # FIND THE MODEL:
        # __file__ is 'utilities/preprocessing.py'
        # base_dir will be the 'utilities' folder
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, 'regression_model.pkl')
        
        was_predicted = True

        if os.path.exists(model_path):
            model = joblib.load(model_path)

            # The model was trained without 'Gender' and 'School_Type'
            # We must drop them to match the feature input shape (17 columns)
            cols_to_drop = ['Gender', 'School_Type']
            X_input = df_mapped.drop(columns=[c for c in cols_to_drop if c in df_mapped.columns])
            
            # Ensure no other extra columns (like Target if it was all NaNs) are present
            if 'Exam_Score' in X_input.columns:
                X_input = X_input.drop(columns=['Exam_Score'])
                
            df_mapped['Exam_Score'] = model.predict(X_input)
        else:
            raise FileNotFoundError(f"Model file '{model_path}' not found. Cannot predict missing Exam_Score.")
    
    # Extract the two core academic columns
    academic_df = df_mapped[['Previous_Scores', 'Exam_Score']].copy()
    
    # Apply Standard Scaling
    scaler = StandardScaler()
    academic_df[['Previous_Scores', 'Exam_Score']] = scaler.fit_transform(academic_df[['Previous_Scores', 'Exam_Score']])

    return academic_df,was_predicted
