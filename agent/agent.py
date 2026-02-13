# take a csv
# analysis strategy :
# multiple APIs?

# --------------------------persona identification----------------------
# AI layer(call the API)
#identify the highest varaince 3-4 columns
#leave them as it is
#if there are columns that can lead to natural grouping of students like gender ,exclude it, keep it for post clustering analysis
# club remaining columns into meaningful features that............?
# return feature map ,excluded columns in the form of jsons

# we need a simple function here(native processing)
# write a script that uses feature map to reduce the df to those features(has gotta be generic)

# identify best value of K using Elbow method(call the API ,ask it to return a single integer)

# cluster using k-means (is already generic)
# obtain the centroids as result

# send the centroids along with feature map to AI(Call API again)
# ask it to return names and spider chart(json) for the centroid students, along with reason to name them the way it did, and insights on how the centroid student could be helped


