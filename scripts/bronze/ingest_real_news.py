"""
Overview: Ingests raw real news JSON data into the bronze layer table 'bronze.real_news'.
Example Usage:
    python scripts/bronze/ingest_real_news.py
"""
from pathlib import Path
import pandas as pd 
import db 


file_path = 'data/'
engine = db.db_engine()



real_news_df = pd.read_json(lines=True, path_or_buf= f'{file_path}/News_Category_Dataset_v3.json')

real_news_df.to_sql(
    name='real_news', 
    schema='bronze',
    con=engine, 
    if_exists='replace',  # Options: 'fail', 'replace', 'append'
    index=False           # Do not write the DataFrame index as a column
)
