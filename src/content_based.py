# Content-based filtering recommends movies similar to ones a user already likes, 
# based on the movie's own features — genre, rating, etc.
#  similarity close to 1 → they're similar.

import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('../data/movies_dataset.csv').sample(n=10000, random_state=42).reset_index(drop=True)

#Genre dummies
genre_dummies = pd.get_dummies(df['Genre'], prefix='Genre')

#Numeric features
numeric_features = df[['IMDbRating', 'RottenTomatoesScore', 'ReleaseYear']]

# Combine all features into one DataFrame
features = pd.concat([genre_dummies, numeric_features], axis=1)

# Normalize
scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)

#KNN MODEL
model = NearestNeighbors(n_neighbors=6, metric='cosine')
model.fit(features_scaled)


def recommend(title, n=5):
    try:
        idx = df[df['Title'] == title].index[0]
    except IndexError:
        print("Movie not found.")
        return []
    
    distances, indices = model.kneighbors([features_scaled[idx]], n_neighbors=n+1)

    results = []
    for i, dist in zip(indices[0][1:], distances[0][1:]):  # skip itself
        similarity = 1 - dist
        results.append({
            'title': df.loc[i, 'Title'],
            'similarity': round(similarity, 3)
        })

    return results

if __name__ == '__main__':
    sample_title = df['Title'].iloc[0]
    results = recommend(sample_title)
    print(results)






