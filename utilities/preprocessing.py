import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def mapped_scaled(df):
    """
    Step 1: Universal Preprocessing
    Numerically maps categorical strings and scales all 20 columns to a 0-1 range.
    """
    df_mapped = df.copy()
    
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

    # Extract the two core academic columns
    academic_df = df_mapped[['Previous_Scores', 'Exam_Score']].copy()
    
    # Apply Min-Max Scaling so both scores are between 0.0 and 1.0
    scaler = StandardScaler()
    academic_df[['Previous_Scores', 'Exam_Score']] = scaler.fit_transform(academic_df[['Previous_Scores', 'Exam_Score']])

    return academic_df
