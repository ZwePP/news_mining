/*
===============================================================================
DDL Script: Initialize Database and Schemas
===============================================================================
Script Purpose:
This script initializes the PostgreSQL database and creates medallion schemas
(bronze, silver, gold) for the data warehouse.

Usage:
    psql -U <username> -f init_db.sql
===============================================================================
*/

-- =============================================================================
-- Create Database
-- =============================================================================
CREATE DATABASE news_mining;


-- =============================================================================
-- Create Schemas: bronze, silver, gold
-- =============================================================================
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;
