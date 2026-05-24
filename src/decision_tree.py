import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.tree import export_text

df = pd.read_csv('../data/movies_dataset.csv').sample(n=10000, random_state=42).reset_index(drop=True)

# create RatingTier column
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

# Decision tree with depth limit to avoid overfitting
model = DecisionTreeClassifier(max_depth=5, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Evaluation
importance = pd.Series(model.feature_importances_, index=X.columns)
importance = importance.sort_values(ascending=False)
print("\nTop features:")
print(importance.head(10))
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2f}")

print("Classification Report:")
print(classification_report(y_test, model.predict(X_test)))

print("Decision Tree Rules:")
tree_rules = export_text(model, feature_names=list(X.columns))
print(tree_rules)