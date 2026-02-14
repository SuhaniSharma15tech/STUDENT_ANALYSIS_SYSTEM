from math import sqrt

def predict_pc(data5, centroid5):
    # 1. Initialize output dictionary
    # Example: {"cluster1": [indices], "cluster2": [indices]...}
    persona_map = {cluster: [] for cluster in centroid5.keys()}

    def calcdistance(x, y):
        return sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))

    # 2. Iterate through the 8feature dataframe
    for index, row in data5.iterrows():
        
    
        # Theme order must match be same as our centroid training order
        point = [
            row['Hours_Studied'], 
            row['Attendance'],
            row['Previous_Scores'],
            row['Motivation_Level'],
            row['Resource_Access'], 
            row['Family_Capital'], 
            row['Personal_Wellbeing'], 
            row['Environmental_Stability']
        ]
        best_cluster = None
        mindistance = float('inf')
        
        # 3. Find the closest Persona centroid
        for cluster_name, centroid_coords in centroid5.items():
            dist = calcdistance(point, centroid_coords)
            if dist < mindistance:
                mindistance = dist
                best_cluster = cluster_name
        
        # 4. Store the original index
        persona_map[best_cluster].append(index)
        
    return persona_map
    # this is a dictionary 

def predict_ac(data3, centroid3):
    # 1. Initialize output dictionary
    prediction_map = {cluster: [] for cluster in centroid3.keys()}
    
    def calcdistance(x, y):
        # Euclidean distance formula
        return sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))

    # 2. Iterate through the dataframe by index
    for index, row in data3.iterrows():
        point = [row['Exam_Score'], row['Previous_Scores']]
        
        best_cluster = None
        min_dist = float('inf')
        
        # 3. Find the closest centroid
        for cluster_name, centroid_coords in centroid3.items():
            dist = calcdistance(point, centroid_coords)
            if dist < min_dist:
                min_dist = dist
                best_cluster = cluster_name
        
        # 4. Store the index (e.g., if it's record 13, index is 12)
        prediction_map[best_cluster].append(index)
        
    return prediction_map
    # returns a dictionary