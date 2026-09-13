/*
===============================================================================
DDL Script: Create Gold Views
===============================================================================
Script Purpose:
This script creates views for the Gold layer in the data warehouse.
It combines and standardizes cleaned data from the Silver layer
to produce an integrated dataset ready for machine learning and reporting.

Usage:
    psql -U <username> -d news_mining -f scripts/gold/ddl_gold.sql
    SELECT * FROM gold.total_news LIMIT 10;
===============================================================================
*/

-- =============================================================================
-- Create View: gold.total_news
-- =============================================================================
CREATE OR REPLACE VIEW gold.total_news AS

-- 1. Select and standardize REAL news
SELECT 
    headline AS title,
    description AS article_text,
    authors AS author,
    published_date AS published_date,
    'real_news' AS source_type,
    0 AS is_fake  -- Target variable for ML (0 = Real)
FROM silver.real_news

UNION ALL

-- 2. Select and standardize FAKE news
SELECT 
    headline AS title,
    description AS article_text,
    authors AS author,
    published_date AS published_date,
    news_type AS source_type,
    1 AS is_fake  -- Target variable for ML (1 = Fake)
FROM silver.fake_news;