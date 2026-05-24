import pandas as pd

df = pd.read_csv('../data/movies_dataset.csv')

# display first few rows
print("First 5 rows of the dataset:")
print(df.head())

# always check your actual column names first
print("Column names:")
print(df.columns.tolist())

# summary + stats
df.info()
print(df.describe(include='all'))

# missing values
print("Missing values per column:")
print(df.isna().sum())

# cleaning — correct column name is ReleaseDate
df['ReleaseDate'] = pd.to_datetime(df['ReleaseDate'], errors='coerce')
df['release_year'] = df['ReleaseDate'].dt.year   # fixed typo
df['release_month'] = df['ReleaseDate'].dt.month

# unique genres
print("Unique genres:", df['Genre'].unique())

# min, max, avg IMDb rating — cleaner as one line
print("IMDb Rating Stats:")
print(df['IMDbRating'].agg(['min', 'max', 'mean']))

# movies per decade — your logic was correct!
df['decade'] = (df['release_year'] // 10) * 10
movies_per_decade = df['decade'].value_counts().sort_index()
print("Movies per decade:")
print(movies_per_decade)