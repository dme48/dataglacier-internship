# Importing the libraries
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

MODEL_PATH = "model.pkl"

df = pd.read_csv('crab_age.csv').dropna()

# Process csv
fields = ["Length", "Diameter", "Height", "Weight"]
X = pd.get_dummies(data=df[fields])
y = df["Age"]

# Build model, fit model
model = LinearRegression()
model.fit(X, y)


# Pickle the object
with open(MODEL_PATH,'wb') as savefile:
    pickle.dump(model, savefile)


# Optional: test loading and use of model
example = [[1.0, 0.9, 0.3, 10]]
with open(MODEL_PATH, 'rb') as savefile:
    model = pickle.load(savefile)

prediction = model.predict(example)
print(prediction)