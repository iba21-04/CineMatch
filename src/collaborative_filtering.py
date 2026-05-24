import pandas as pd
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv('../data/movies_dataset.csv').sample(n=10000, random_state=42).reset_index(drop=True)

# rows = Directors, columns = Movies, values = IMDbRating
user_item_matrix = df.pivot_table(
    index='Director',
    columns='Title',
    values='IMDbRating',
    fill_value=0
)
model = NearestNeighbors(n_neighbors=6, metric='cosine')
model.fit(user_item_matrix)

def recommend(director_name, n=5):
    try:
        idx = user_item_matrix.index.get_loc(director_name)
    except KeyError:
        print("Director not found.")
        return []

    distances, indices = model.kneighbors(
        [user_item_matrix.iloc[idx]], n_neighbors=n+1
    )

    # movies this director already made
    already_made = set(df[df['Director'] == director_name]['Title'])

    # similar directors
    similar_directors = user_item_matrix.index[indices[0][1:]]

    # movies from similar directors, excluding already_made
    similar_movies = df[
        df['Director'].isin(similar_directors) &
        ~df['Title'].isin(already_made)
    ]

    # sort by IMDbRating and return top n
    similar_movies = similar_movies.sort_values(by='IMDbRating', ascending=False)
    return similar_movies[['Title', 'IMDbRating']].head(n).to_dict(orient='records')

if __name__ == '__main__':
    sample_director = df['Director'].iloc[0]
    print(recommend(sample_director))
     


