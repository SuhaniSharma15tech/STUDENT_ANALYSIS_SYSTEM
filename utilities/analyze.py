# we are not clustering everytime, we are just predicting
import pandas as pd
import preprocessing
import predict
import numpy as np

# each centoid is Exam_Score, Previous_Scores
CENTROID3 = {
    'cluster1': np.array([0.83384127, 0.28523119]), 
    'cluster2': np.array([0.16748274, 0.24843434]), 
    'cluster3': np.array([0.4980978 , 0.26407826])
}

# each centroid is in this order :
# Hours_Studied, Attendance, Previous_Scores, Motivation_Level, Resource_Access, Family_Capital, Personal_Wellbeing, Environmental_Stability
CENTROID5 = {
    'cluster1': np.array([0.44068296, 0.76803797, 0.4636509 , 0.50033311, 0.48963191, 0.44770153, 0.51776593, 0.75194315]), 
    'cluster2': np.array([0.44565181, 0.28637191, 0.77933042, 0.36026201, 0.49517831, 0.43104076, 0.54144428, 0.74417758]), 
    'cluster3': np.array([0.44155739, 0.69383145, 0.49362294, 0.        , 0.4909137 , 0.45417029, 0.52813978, 0.74326672]), 
    'cluster4': np.array([0.43556128, 0.49245068, 0.51207891, 1.        , 0.49268146, 0.43664643, 0.53637666, 0.74140111]), 
    'cluster5': np.array([0.44298367, 0.24214173, 0.23990499, 0.34085511, 0.49068026, 0.46060966, 0.53668514, 0.75072579])
}

def get_complete_analysis(input_csv):
    # 1. Read raw data
    df_raw = pd.read_csv(input_csv)
    
    # 2. Universal Preprocessing (Mapped and Scaled)
    mapped_scaled_df = preprocessing.mapped_scaled(df_raw)

    # -------------- Persona Wise Predictions (K=5) ------------------------
    reduced_persona_df = preprocessing.persona_reduction(mapped_scaled_df)
    persona_clusters = predict.predict_pc(reduced_persona_df, CENTROID5)
    
    # ------------------Academic Wise Predictions (K=3) ------------------------
    reduced_academic_df = preprocessing.academic_reduction(mapped_scaled_df)
    academic_clusters = predict.predict_ac(reduced_academic_df, CENTROID3)

    # ----------------- Demographic Analysis Logic ----------------------------
    analysis_results = {
        "persona_segmentation": {},
        "academic_segmentation": {}
    }

    # Analyze Gender and School Type for Persona Clusters
    for cluster_name, indices in persona_clusters.items():
        if not indices:
            continue
            
        # Extract subset from original raw dataframe using the indices
        cluster_data = df_raw.iloc[indices]
        total_in_cluster = len(cluster_data)

        # Gender counts
        gender_counts = cluster_data['Gender'].value_counts(normalize=True).to_dict()
        
        # School Type counts
        school_counts = cluster_data['School_Type'].value_counts(normalize=True).to_dict()

        analysis_results["persona_segmentation"][cluster_name] = {
            "total_students": total_in_cluster,
            "gender_distribution": {k: round(v * 100, 2) for k, v in gender_counts.items()},
            "school_distribution": {k: round(v * 100, 2) for k, v in school_counts.items()}
        }

    # Do the same for Academic Clusters 
    for cluster_name, indices in academic_clusters.items():
        if not indices: 
            continue
                # Extract subset from original raw dataframe using the indices
        cluster_data = df_raw.iloc[indices]
        total_in_cluster = len(cluster_data)

        # Gender counts
        gender_counts = cluster_data['Gender'].value_counts(normalize=True).to_dict()
        
        # School Type counts
        school_counts = cluster_data['School_Type'].value_counts(normalize=True).to_dict()

        analysis_results["academic_segmentation"][cluster_name] = {
            "total_students": total_in_cluster,
            "gender_distribution": {k: round(v * 100, 2) for k, v in gender_counts.items()},
            "school_distribution": {k: round(v * 100, 2) for k, v in school_counts.items()}
        }

    return analysis_results

# print(get_complete_analysis("rawdata.csv"))

# result will look something like this
# {'persona_segmentation': {'cluster1': {'total_students': 1501, 'gender_distribution': {'Male': 57.43, 'Female': 42.57}, 'school_distribution': {'Public': 68.69, 'Private': 31.31}}, 'cluster2': {'total_students': 1373, 'gender_distribution': {'Male': 56.66, 'Female': 43.34}, 'school_distribution': {'Public': 69.56, 'Private': 30.44}}, 'cluster3': {'total_students': 1151, 'gender_distribution': {'Male': 56.99, 'Female': 43.01}, 'school_distribution': {'Public': 68.64, 'Private': 31.36}}, 'cluster4': {'total_students': 1318, 'gender_distribution': {'Male': 58.5, 'Female': 41.5}, 'school_distribution': {'Public': 70.71, 'Private': 29.29}}, 'cluster5': {'total_students': 1264, 'gender_distribution': {'Male': 59.1, 'Female': 40.9}, 'school_distribution': {'Public': 70.41, 'Private': 29.59}}}, 
# 'academic_segmentation': {'cluster1': {'total_students': 32, 'gender_distribution': {'Female': 53.12, 'Male': 46.88}, 'school_distribution': {'Public': 68.75, 'Private': 31.25}}, 'cluster2': {'total_students': 5038, 'gender_distribution': {'Male': 57.48, 'Female': 42.52}, 'school_distribution': {'Public': 69.71, 'Private': 30.29}}, 'cluster3': {'total_students': 1537, 'gender_distribution': {'Male': 58.75, 'Female': 41.25}, 'school_distribution': {'Public': 69.23, 'Private': 30.77}}}}