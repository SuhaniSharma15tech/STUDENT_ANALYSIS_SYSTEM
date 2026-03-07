
# we are not clustering everytime, we are just predicting
import pandas as pd
import numpy as np
try:
    # running from outside the package
    from . import preprocessing
    from . import predict
except:
    # running inside the package
    import preprocessing
    import predict

# each centroid is Previous_Scores, Exam_Score
CENTROID3 = {
    'Accelerating High-Achievers': np.array([0.48762996, 1.17656746]), #PEAKING
    'Consistent Strugglers': np.array([-0.94062206, -0.37412239]), #IMPROVING BUT STILL BEHIND
    'High Potential Slumpers': np.array([ 0.85216601, -0.37199457]) #DECLINING
}

# each centroid features: 
# Hours_Studied, Attendance, Previous_Scores, Motivation_Level, Resource_Access, Family_Capital, Personal_Wellbeing, Environmental_Stability
CENTROID5 = {
    'High-Drive Enthusiasts': np.array([
        -0.09666085, -0.04637682,  0.03029957,  1.57174936, 
         0.00726967, -0.02022114,  0.00958447, -0.01226610
    ]), 
    'Gifted Coasters': np.array([
        -0.82684984,  0.38527450,  0.85332617, -0.37338406, 
        -0.01328584,  0.03321634,  0.00400691, -0.03490454
    ]), 
    'Disengaged & At-Risk': np.array([
        -0.25221583, -0.92226203, -0.75712059, -0.43228023, 
         0.00270391,  0.02553331,  0.02765259,  0.00747651
    ]), 
    'Diligent but Struggling': np.array([
         0.15599181,  0.94444012, -0.81348218, -0.33608097, 
         0.01442486, -0.00076511, -0.03161793,  0.03316296
    ]),
    'Independent Grinders': np.array([
         0.95396803, -0.35845237,  0.79259655, -0.32434181,
        -0.01201209, -0.03932263, -0.00792122,  0.00033935
    ])
}

def get_complete_analysis(input_csv):
    """Generates segmentation data and cross-references trajectory with personas."""
    # 1. Read raw data
    df_raw = pd.read_csv(input_csv)
    
    # 2. Universal Preprocessing (Mapped and Scaled)
    mapped_scaled_df = preprocessing.mapped_scaled(df_raw)

    # -------------- Persona Wise Predictions (K=5) ------------------------
    reduced_persona_df = preprocessing.persona_reduction(mapped_scaled_df)
    persona_clusters = predict.predict_pc(reduced_persona_df, CENTROID5)
    
    # ------------------ Academic Wise Predictions (K=3) ------------------------
    reduced_academic_df = preprocessing.academic_reduction(mapped_scaled_df)
    academic_clusters = predict.predict_ac(reduced_academic_df, CENTROID3)

    # Create an index-to-persona map for trajectory cross-referencing
    idx_to_persona = {}
    for p_name, indices in persona_clusters.items():
        for idx in indices:
            idx_to_persona[idx] = p_name

    analysis_results = {
        "persona_segmentation": {},
        "academic_segmentation": {},
        "trajectory_persona_mapping": {}
    }

    # Analyze Demographic distribution for Personas
    for cluster_name, indices in persona_clusters.items():
        if not indices: continue
        cluster_data = df_raw.iloc[indices]
        
        analysis_results["persona_segmentation"][cluster_name] = {
            "total_students": len(cluster_data),
            "gender_distribution": {k: round(v * 100, 2) for k, v in cluster_data['Gender'].value_counts(normalize=True).to_dict().items()},
            "school_distribution": {k: round(v * 100, 2) for k, v in cluster_data['School_Type'].value_counts(normalize=True).to_dict().items()}
        }

    # Analyze demographics and Trajectory-Persona breakdown
    for cluster_name, indices in academic_clusters.items():
        if not indices: continue
        cluster_data = df_raw.iloc[indices]
        
        analysis_results["academic_segmentation"][cluster_name] = {
            "total_students": len(cluster_data),
            "gender_distribution": {k: round(v * 100, 2) for k, v in cluster_data['Gender'].value_counts(normalize=True).to_dict().items()},
            "school_distribution": {k: round(v * 100, 2) for k, v in cluster_data['School_Type'].value_counts(normalize=True).to_dict().items()}
        }

        # NEW: Trajectory-wise Persona Breakdown (for the requested pie charts)
        p_counts = {}
        for idx in indices:
            p_label = idx_to_persona.get(idx, "Unknown")
            p_counts[p_label] = p_counts.get(p_label, 0) + 1
        
        analysis_results["trajectory_persona_mapping"][cluster_name] = {
            p: round((count / len(indices)) * 100, 2) for p, count in p_counts.items()
        }


        # total students
        analysis_results["Total_Students_in_dataset"]=len(df_raw)


    return analysis_results

def chart_ready(input_csv):
    """Formats raw analysis results into JSON-ready structure for charts.html."""
    # do the analysis first
    result=get_complete_analysis(input_csv)
    total_records=result["Total_Students_in_dataset"]
    
    # 1. Overall Pie Chart Compositions
    mega_pie = {
        "persona": {name: round((d['total_students'] / total_records) * 100, 2) for name, d in result["persona_segmentation"].items()},
        "academic": {name: round((d['total_students'] / total_records) * 100, 2) for name, d in result["academic_segmentation"].items()}
    }

    # 2. Spider Chart Data (Centroids)
    features = ['Hours_Studied', 'Attendance', 'Previous_Scores', 'Motivation_Level', 
                'Resource_Access', 'Family_Capital', 'Personal_Wellbeing', 'Environmental_Stability']
    spider = {name: {features[i]: round(float(centroid[i]), 3) for i in range(len(features))} for name, centroid in CENTROID5.items()}

    # 3. Demographic Summaries
    gender_summary = {
        "persona": {name: d['gender_distribution'] for name, d in result["persona_segmentation"].items()},
        "academic": {name: d['gender_distribution'] for name, d in result["academic_segmentation"].items()}
    }
    school_summary = {
        "persona": {name: d['school_distribution'] for name, d in result["persona_segmentation"].items()},
        "academic": {name: d['school_distribution'] for name, d in result["academic_segmentation"].items()}
    }

    return {
        "mega_pie": mega_pie,
        "spider": spider,
        "gender_summary": gender_summary,
        "school_summary": school_summary,
        "trajectory_mapping": result["trajectory_persona_mapping"]
    }

# print(chart_ready("rawdata.csv"))
