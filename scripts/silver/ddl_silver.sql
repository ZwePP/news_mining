/*
===============================================================================
DDL Script: Create Silver Tables
===============================================================================
Script Purpose:
This script creates tables for the cleaned Silver layer in the data warehouse.
The Silver layer stores standardized, filtered, and typed news records.

Usage:
    psql -U <username> -d news_mining -f scripts/silver/ddl_silver.sql
===============================================================================
*/

-- =============================================================================
-- Create Table: silver.real_news
-- =============================================================================
DROP TABLE IF EXISTS silver.real_news;
CREATE TABLE silver.real_news(
	headline TEXT,
	description TEXT,
	authors TEXT,
	published_date	DATE,
	dwh_create_time TIMESTAMP DEFAULT clock_timestamp()
);

-- =============================================================================
-- Create Table: silver.fake_news
-- =============================================================================
DROP TABLE IF EXISTS silver.fake_news;
CREATE TABLE silver.fake_news(
	headline TEXT,
	description TEXT,
	authors TEXT,
	published_date DATE,
	news_type TEXT,
	dwh_create_time TIMESTAMP DEFAULT clock_timestamp()
);

