
import pandas as pd
import joblib # Added for saving the model
from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MinMaxScaler # no longer needed
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error
from utilities import preprocessing

# 1. Load data and do encoding
DF = pd.read_csv("data/rawdata.csv")
df=preprocessing.mapped_scaled(DF)

# 2. Split features and target
TARGET_COL = "Exam_Score"
X = df.drop([TARGET_COL, "Gender", "School_Type"], axis=1)
y = df[TARGET_COL]

# 3. Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# # 4. Apply Min-Max Scaling
# scaler = MinMaxScaler() 
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)
# not scaling since previous score would be calculated in the academic_reduction() of preprocessing which takes data after numerical encoding not after scaling 

# 5. Train the Regression Model
# model = LinearRegression()
# model.fit(X_train_scaled, y_train)
#changes from  this to this:
model = LinearRegression()
model.fit(X_train, y_train)


# 6. Evaluate
y_pred = model.predict(X_test)
print(f"R2 Score: {r2_score(y_test, y_pred)}")
print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred)}")
print("Root Mean Squared Error      :", root_mean_squared_error(y_test, y_pred))
# 7. SAVE FOR DASHBOARD (Important!)
# Create a 'models' folder in your directory first
joblib.dump(model, 'models/regression_model.pkl')
# joblib.dump(scaler, 'models/regression_scaler.pkl')

print("Success: Model  saved to /models folder.")
