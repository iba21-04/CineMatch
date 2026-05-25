from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)
CORS(app)

# ── Load data and train model ONCE at startup ──────────────────────────────
# (you don't want to reload data on every request — that would be very slow)

df = pd.read_csv('data/movies_dataset.csv').sample(n=10000, random_state=42).reset_index(drop=True)

genre_dummies = pd.get_dummies(df['Genre'], prefix='Genre')
numeric = df[['IMDbRating', 'RottenTomatoesScore', 'ReleaseYear']]
features = pd.concat([genre_dummies, numeric], axis=1)

scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)

model = NearestNeighbors(n_neighbors=6, metric='cosine')
model.fit(features_scaled)

# ── Routes ─────────────────────────────────────────────────────────────────

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title', '')

    if not title:
        return jsonify({'error': 'No title provided'}), 400

    # check if movie exists BEFORE trying to index
    matches = df[df['Title'] == title]
    if matches.empty:
        return jsonify({'error': f'Movie not found: {title}'}), 404

    movie_idx = matches.index[0]
    distances, indices = model.kneighbors([features_scaled[movie_idx]])

    results = []
    for i in range(1, len(indices[0])):
        idx = indices[0][i]
        movie = df.iloc[idx]
        results.append({
            'title': str(movie['Title']),
            'imdb_rating': float(movie['IMDbRating']),
            'rotten_tomatoes_score': int(movie['RottenTomatoesScore'])
        })

    return jsonify(results)
@app.route('/titles', methods=['GET'])
def titles():
    sample = df['Title'].head(50).tolist()
    return jsonify(sample)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'movies_loaded': len(df)})

if __name__ == '__main__':
    app.run(debug=True)