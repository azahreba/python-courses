import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from sklearn.metrics import mean_absolute_error
from sklearn.externals import joblib

# Load the data set
df = pd.read_csv("ml_house_data_set.csv")

# Remove the fields from the data set that we don't want to include in our model
del df['house_number']
del df['unit_number']
del df['street_name']
del df['zip_code']

# Replace categorical data with one-hot encoded data
features_df = pd.get_dummies(df, columns=['garage_type', 'city'])

# Remove the sale price from the feature data
del features_df['sale_price']

# Create the X and y arrays
X = features_df.as_matrix()
y = df['sale_price'].as_matrix()

# Split the data set in a training set (70%) and a test set (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Fit regression (value prediction) model
model = ensemble.GradientBoostingRegressor(
    n_estimators=1000, # tells the model how many decision trees to build. Higher numbers usually allow the model to be more accurate but it increases the amount of time required to run the model
    learning_rate=0.1, # controls how much each additional decision tree influences the overall prediction. Lower rates usually lead to higher accuracy but only works if we have n_estimators set to a high value
    max_depth=6, # controls how many layers deep each individual decision tree can be. We'll start with 6 which means that each decision tree in the model can be up to 6 layers deep
    min_samples_leaf=9, # controls how many times a value must appear in our training set for a decision tree to make a decision based on it. Let's set it to 9. We are saying that at least 9 houses must exhibit the same characteristic before we consider it meaningful enough to build a decision tree around it. This helps prevent single outliers from influencing the model too much
    max_features=0.1, # percentage of features in our model that we randomly choose to consider each time we create a branch in our decision tree
    loss='huber', # controls how scikit-learn calculates the model's error rate or cost as it learns. The huber function does a good job while not being too influenced by outliers in the data set
    random_state=0
)
model.fit(X_train, y_train)

# Save the trained model to a file so we can use it in other programs
joblib.dump(model, 'trained_house_classifier_model.pkl')

# Find the error rate on the training set
mse = mean_absolute_error(y_train, model.predict(X_train))
print("Training Set Mean Absolute Error: %.4f" % mse)

# Find the error rate on the test set
mse = mean_absolute_error(y_test, model.predict(X_test))
print("Test Set Mean Absolute Error: %.4f" % mse)

