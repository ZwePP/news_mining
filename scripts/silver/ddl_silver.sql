-- DDL for Silver -- 
-- Removed unnecessary columns

DROP TABLE IF EXISTS silver.real_news;
CREATE TABLE silver.real_news(
	headline TEXT,
	description TEXT,
	authors TEXT,
	published_date	DATE,
	dwh_create_time TIMESTAMP DEFAULT clock_timestamp()
);

DROP TABLE IF EXISTS silver.fake_news;
CREATE TABLE silver.fake_news(
	headline TEXT,
	description TEXT,
	authors TEXT,
	published_date DATE,
	news_type TEXT,
	dwh_create_time TIMESTAMP DEFAULT clock_timestamp()
);

