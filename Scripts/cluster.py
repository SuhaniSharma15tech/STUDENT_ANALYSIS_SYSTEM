
import pandas as pd
import random
import numpy as np
from math import sqrt 

centroiddict={}
clustered_data={}
difference={}
infinity=float('inf')

def calcdistance(x,y):
    return sqrt(np.sum((x - y) ** 2))

def findingrandomcentroids(no, datapoints):
    global centroiddict, clustered_data, difference
    datapoints = np.array(datapoints)
    
    # Initialize centroids using K-Means++ logic
    centroiddict['cluster1'] = datapoints[random.randint(0, len(datapoints)-1)]
    clustered_data['cluster1'] = []
    difference['cluster1'] = 0

    for i in range(2, no + 1):
        distances = np.array([min(np.sum((x - c)**2) for c in centroiddict.values()) for x in datapoints]) 
        prob = distances / (distances.sum() + 1e-10) # Added epsilon to avoid div by zero
        idx = np.random.choice(len(datapoints), p=prob)
        centroiddict[f'cluster{i}'] = datapoints[idx]
        clustered_data[f'cluster{i}'] = []
        difference[f'cluster{i}'] = 0

def clustering(precision, data_points_set):
    tocontinue = True
    while tocontinue:
        for cluster in clustered_data:
            clustered_data[cluster] = []
            
        for datapoint in data_points_set:
            best = None
            mindistance = infinity
            for cluster in centroiddict:
                distance = calcdistance(datapoint, centroiddict[cluster])
                if distance < mindistance:
                    mindistance = distance
                    best = cluster
            clustered_data[best].append(datapoint)

        for cluster in centroiddict:
            arr = np.array(clustered_data[cluster])
            if len(arr) == 0:
                continue
            newcentroid = np.mean(arr, axis=0)
            difference[cluster] = calcdistance(newcentroid, centroiddict[cluster])
            centroiddict[cluster] = newcentroid
            
        if max(difference.values()) < precision:
            tocontinue = False

# --- KEY CHANGES START HERE ---

# 1. Load the data
# Use the file that contains both scaled columns
df = pd.read_csv("data/scaleddata.csv") 

# 2. Select ONLY the 2 score parameters
# We filter for these two specific columns
data_to_cluster = df[['Exam_Score', 'Previous_Scores']].to_numpy()

# 3. Run training (clustering into, say, 3 performance tiers: High, Mid, Low)
findingrandomcentroids(3, data_to_cluster) 
clustering(10**-10, data_to_cluster)

# 4. Output results
print("Final Centroids (Exam Score vs Previous Score):")
columns = ['Exam_Score', 'Previous_Scores']
centroid_df = pd.DataFrame(centroiddict).T
centroid_df.columns = columns

print(centroid_df)

# Save results specifically for the scores
with open(r"resultsNew.txt","w") as file:
    file.write('\n')
    file.write('--------------academic_performance-------------\n')
    file.write(str(centroiddict))
