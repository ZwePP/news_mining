/*
Overview: Initializes the PostgreSQL database and medallion schemas (bronze, silver, gold).
Example Usage:
    psql -U <username> -f init_db.sql
*/
CREATE DATABASE news_mining;


CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;
