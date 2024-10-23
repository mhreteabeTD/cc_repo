import numpy as np
from sklearn import datasets
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score

# Load a larger dataset
covtype = datasets.fetch_covtype()
X = covtype.data
y = covtype.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

# Create AdaBoost model with a grid search over several hyperparameters
param_grid = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 1]
}
model = GridSearchCV(AdaBoostClassifier(), param_grid, cv=3)

# Fit model on training data
model.fit(X_train, y_train)

# Predict and evaluate
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")
print(f"Best Parameters: {model.best_params_}")
