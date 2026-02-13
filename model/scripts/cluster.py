import pandas as pd
import random
import numpy as np
from math import sqrt 

centroiddict={}
clustered_data={}
difference={}
infinity=float('inf')

# 1. The algo
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
        prob = distances / distances.sum()
        idx = np.random.choice(len(datapoints), p=prob)
        centroiddict[f'cluster{i}'] = datapoints[idx]
        clustered_data[f'cluster{i}'] = []
        difference[f'cluster{i}'] = 0

def clustering(precision, data_points_set):
    tocontinue = True
    while tocontinue:
        # Reset clusters
        for cluster in clustered_data:
            clustered_data[cluster] = []
            
        # Assignment step
        for datapoint in data_points_set:
            best = None
            mindistance = infinity
            for cluster in centroiddict:
                distance = calcdistance(datapoint, centroiddict[cluster])
                if distance < mindistance:
                    mindistance = distance
                    best = cluster
            clustered_data[best].append(datapoint)

        # Update step
        for cluster in centroiddict:
            arr = np.array(clustered_data[cluster])
            if len(arr) == 0:
                continue
            newcentroid = np.mean(arr, axis=0)
            difference[cluster] = calcdistance(newcentroid, centroiddict[cluster])
            centroiddict[cluster] = newcentroid
            
        if max(difference.values()) < precision:
            tocontinue = False

df = pd.read_csv("data/processed_students.csv")
data_to_cluster = df.to_numpy()

# 2. Run training
findingrandomcentroids(5, data_to_cluster)
clustering(10**-10, data_to_cluster)

# 3. Output results
print("Final Centroids (5 Themes):")
columns = df.columns
centroid_df = pd.DataFrame(centroiddict).T
centroid_df.columns = columns
with open("results.txt","w") as file:
    file.write(str(centroiddict))

print(centroid_df)
