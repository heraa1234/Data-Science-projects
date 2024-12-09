# -*- coding: utf-8 -*-
"""ETL Pipeline for Movie Data Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jJcnK2RhpFRR6B7XkkQsCLuUOBl6mcOO
"""

pip install pandas sqlalchemy

import pandas as pd
from sqlalchemy import create_engine

# Step 1: Extract Data

# Load datasets
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
tags = pd.read_csv("tags.csv")

# Display the first few rows of each dataset
print("Movies Data:")
print(movies.head())
print("\nRatings Data:")
print(ratings.head())
print("\nTags Data:")
print(tags.head())

# Step 2: Transform Data

# Clean the movies data: Remove any duplicates
movies.drop_duplicates(inplace=True)

# Merge the ratings with movies to get a combined dataset for analysis
movie_ratings = pd.merge(ratings, movies, on='movieId', how='inner')

# Parse genres into a list format for easier analysis
movie_ratings['genres'] = movie_ratings['genres'].apply(lambda x: ', '.join(x))

# Convert timestamp column to a datetime format for better readability
movie_ratings['timestamp'] = pd.to_datetime(movie_ratings['timestamp'], unit='s')

print("\nTransformed Movie Ratings Data:")
print(movie_ratings.head())

# Step 3: Load Data

# Set up a SQLite database connection
engine = create_engine('sqlite:///movielens.db', echo=True)

# Load each dataframe into the database
movies.to_sql('movies', con=engine, if_exists='replace', index=False)
ratings.to_sql('ratings', con=engine, if_exists='replace', index=False)
tags.to_sql('tags', con=engine, if_exists='replace', index=False)
movie_ratings.to_sql('movie_ratings', con=engine, if_exists='replace', index=False)

print("\nData loaded successfully into SQLite database.")

# Step 4: Analysis (Example Queries)

# Query top-rated movies
with engine.connect() as conn:
    query = """
    SELECT title, AVG(rating) as average_rating
    FROM movie_ratings
    GROUP BY title
    HAVING COUNT(rating) > 10
    ORDER BY average_rating DESC
    LIMIT 10;
    """
    top_movies = pd.read_sql(query, conn)
    print("\nTop 10 Highest Rated Movies (with more than 10 ratings):")
    print(top_movies)

