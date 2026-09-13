"""
===============================================================================
Data Ingestion: Bronze Real News
===============================================================================
Script Purpose:
This script loads raw real news records from data/News_Category_Dataset_v3.json
into the PostgreSQL Bronze table 'bronze.real_news'.

Usage:
    python scripts/bronze/ingest_real_news.py
===============================================================================
"""

# =============================================================================
# Ingest News_Category_Dataset_v3.json into bronze.real_news
# =============================================================================
from pathlib import Path
import pandas as pd 
import scripts.db as db 


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
