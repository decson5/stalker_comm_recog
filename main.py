# Import required libraries for data processing and modeling
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

# Load data from the CSV file with S.T.A.L.K.E.R. 2 reviews
df = pd.read_csv("stalker_reviews.csv")
X = df["Text"]  # Column with review texts
y = df["Label"]  # Column with labels (positive/negative)

# Convert text data into numerical features using Tfidf
vectorizer = TfidfVectorizer()
X_vector = vectorizer.fit_transform(X)

# Initialize the logistic regression model
model = LogisticRegression()

# Evaluate model performance using 5-fold cross-validation
scores = cross_val_score(model, X_vector, y, cv=5)
print(f"Average accuracy: {scores.mean():.2f} (+/- {scores.std() * 2:.2f})")

# Train the model on the entire dataset
model.fit(X_vector, y)

# Test the model with a new review
new_text = "This game is so cool!"
text_vector = vectorizer.transform([new_text])
prediction = model.predict(text_vector)
print(f"Prediction for '{new_text}': {prediction[0]}")