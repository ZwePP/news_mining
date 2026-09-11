"""
Overview: Ingests raw fake news CSV data into the bronze layer table 'bronze.fake_news'.
Example Usage:
    python scripts/bronze/ingest_fake_news.py
"""
from pathlib import Path
import pandas as pd 
import db 

file_path = 'data/'
fake_news_df = pd.read_csv(f'{file_path}/fake.csv')

engine = db.db_engine()

fake_news_df.to_sql(
    name='fake_news', 
    schema='bronze',
    con=engine, 
    if_exists='replace',  # Options: 'fail', 'replace', 'append'
    index=False           # Do not write the DataFrame index as a column
)