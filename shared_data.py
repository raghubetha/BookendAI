import pandas as pd

#Load the dataframes here
#This file is created to load the data once and share with other .py scripts using the import statement

df_books = pd.read_parquet('https://storage.googleapis.com/goodread_data/books.parquet')
df_selected_reviews = pd.read_parquet('https://storage.googleapis.com/goodread_data/selected_reviews.parquet')
df_users = pd.read_parquet('https://storage.googleapis.com/goodread_data/users.parquet')
df_sunburst = pd.read_parquet('https://storage.googleapis.com/goodread_data/sunburst.parquet')
