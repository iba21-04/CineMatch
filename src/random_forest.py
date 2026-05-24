import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

df = pd.read_csv('../data/movies_dataset.csv').sample(n=10000, random_state=42).reset_index(drop=True)

# Create RatingTier from IMDbRating
def label_tier(rating):
    if rating < 5:
        return 'Low'
    elif rating <= 7.5:
        return 'Mid'
    else:
        return 'High'

df['RatingTier'] = df['IMDbRating'].apply(label_tier)

genre_dummies = pd.get_dummies(df['Genre'], prefix='Genre')

numeric_features = df[['RottenTomatoesScore', 'ReleaseYear']]  # add more if available

X = pd.concat([genre_dummies, numeric_features], axis=1)
y = df['RatingTier']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Evaluation
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2f}")

print("\nClassification Report:")
print(classification_report(y_test, model.predict(X_test)))

# Feature importance
importances = model.feature_importances_
feature_importance = sorted(
    zip(X.columns, importances),
    key=lambda x: x[1],
    reverse=True
)

print("\nTop 10 Feature Importances:")
for feat, score in feature_importance[:10]:
    print(f"{feat}: {score:.4f}")

