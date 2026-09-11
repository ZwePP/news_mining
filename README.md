# News Classification Data Pipeline

A data pipeline implementing a Medallion Architecture (Bronze, Silver, Gold) on PostgreSQL to ingest, clean, and prepare real and fake news datasets for classification.

## Architecture

- **Bronze (Raw)**: Ingests raw news datasets as-is into PostgreSQL tables.
- **Silver (Cleaned)**: Cleans text fields, standardizes dates, and filters missing values.
- **Gold (Aggregated/Features)**: Planned layer for feature extraction and classification modeling.

## Project Structure

```
├── data/                    # Raw datasets (fake.csv, News_Category_Dataset_v3.json)
├── scripts/
│   ├── bronze/              # Database connection and bronze ingestion scripts
│   ├── silver/              # Silver DDL and stored procedure for data cleaning
│   └── gold/                # Gold layer scripts (future)
├── init_db.sql              # Database and schema initialization script
├── requirements.txt         # Python package dependencies
├── .envexample              # Environment variable template
└── README.md                # Project documentation
```

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   Create a `.env` file based on `.envexample`:
   ```env
   PG_USERNAME=postgres
   PG_PASSWORD=your_password
   PG_HOST=localhost
   PG_PORT=5432
   PG_DATABASE=news_mining
   ```

3. **Initialize Database and Schemas**:
   ```bash
   psql -U postgres -f init_db.sql
   ```

## Pipeline Execution

1. **Bronze Ingestion (Python)**:
   ```bash
   python scripts/bronze/ingest_fake_news.py
   python scripts/bronze/ingest_real_news.py
   ```

2. **Silver Transformation (PostgreSQL)**:
   Create silver tables and stored procedure:
   ```bash
   psql -U postgres -d news_mining -f scripts/silver/ddl_silver.sql
   psql -U postgres -d news_mining -f scripts/silver/proc_load_silver.sql
   ```
   Execute the procedure to clean and load data:
   ```sql
   CALL silver.load_silver();
   ```

## Datasets

- `fake.csv`: Fake news dataset containing text and metadata tagged as questionable/misleading.
- `News_Category_Dataset_v3.json`: Real news category dataset from HuffPost (2012-2022).

## AI Acknowledgment

This documentation and code overview comments were generated with the assistance of AI (Google Antigravity) to document the repository structure, workflow, and code usage.
