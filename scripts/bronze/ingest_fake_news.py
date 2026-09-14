"""
===============================================================================
Data Ingestion: Bronze Fake News
===============================================================================
Script Purpose:
This script loads raw fake news records from data/fake.csv into the
PostgreSQL Bronze table 'bronze.fake_news'.

Usage:
    python scripts/bronze/ingest_fake_news.py
===============================================================================
"""

# =============================================================================
# Ingest fake.csv into bronze.fake_news
# =============================================================================
from pathlib import Path
import pandas as pd 
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
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