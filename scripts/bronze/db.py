"""
===============================================================================
Database Connection Module: SQLAlchemy Engine
===============================================================================
Script Purpose:
This module initializes a SQLAlchemy database engine using credentials
loaded from environment variables (.env) to connect to PostgreSQL.

Usage:
    from db import db_engine
    engine = db_engine()
===============================================================================
"""

# =============================================================================
# Database Engine Initialization
# =============================================================================
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

pg_username=os.getenv('PG_USERNAME')
pg_password=os.getenv('PG_PASSWORD')
pg_host=os.getenv('PG_HOST')
pg_port=os.getenv('PG_PORT')
pg_database=os.getenv('PG_DATABASE')


def db_engine():
    engine = create_engine(
        f'postgresql://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_database}')
    return engine

if __name__ == "__main__":
    print(db_engine())
