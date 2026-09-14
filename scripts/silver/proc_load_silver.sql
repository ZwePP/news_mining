/*
===============================================================================
Stored Procedure: Load Silver Layer
===============================================================================
Script Purpose:
This stored procedure cleans, standardizes, and loads data from the Bronze layer
into the Silver layer tables (silver.fake_news, silver.real_news).

Usage:
    CALL silver.load_silver();
===============================================================================
*/

-- =============================================================================
-- Stored Procedure: silver.load_silver()
-- =============================================================================

CREATE OR REPLACE PROCEDURE silver.load_silver()
LANGUAGE plpgsql 
AS $$
	BEGIN
		RAISE NOTICE '>>TRUNCATING silver.fake_news';
		TRUNCATE TABLE silver.fake_news;
		RAISE NOTICE '>>INSERTING silver.fake_news';
		INSERT INTO silver.fake_news(
			headline,
			description,
			authors,
			published_date,
			news_type
		)SELECT * FROM (
            SELECT
                TRIM(REGEXP_REPLACE(LOWER(title), '[^a-zA-Z\s]', '', 'g')) AS cleaned_title,
                TRIM(REGEXP_REPLACE(LOWER("text"), '[^a-zA-Z\s]', '', 'g')) AS cleaned_text,
                TRIM(REGEXP_REPLACE(LOWER(author), '[^a-zA-Z\s]', '', 'g')) AS cleaned_author,
                CAST(published AS DATE) AS published_date,
                TRIM(REGEXP_REPLACE(LOWER(type), '[^a-zA-Z\s]', '', 'g')) AS cleaned_type
            FROM bronze.fake_news
            WHERE "text" IS NOT NULL 
        ) AS cleaned_fake
        WHERE cleaned_text != '';
		RAISE NOTICE 'Insert silver.fake_news Complete';

		RAISE NOTICE '------------------------------------';
		RAISE NOTICE '------------------------------------';

					
		RAISE NOTICE '>>TRUNCATING silver.real_news';
		TRUNCATE TABLE silver.real_news;
		RAISE NOTICE '>>INSERTING silver.real_news';
		INSERT INTO silver.real_news(
			headline,
			description,
			authors,
			published_date)
		SELECT * FROM 
			(
				SELECT
					REGEXP_REPLACE(LOWER(TRIM(headline)), '[^a-zA-Z\\s]', '', 'g') AS cleaned_headline,
					REGEXP_REPLACE(LOWER(TRIM(short_description)), '[^a-zA-Z\\s]', '', 'g') AS cleaned_description,
					REGEXP_REPLACE(LOWER(TRIM(authors)), '[^a-zA-Z\\s]', '', 'g') AS cleaned_authors,
					CAST(date AS DATE) AS cleaned_date
				FROM bronze.real_news
				WHERE short_description IS NOT NULL
			 ) AS cleaned_data
		WHERE cleaned_description != ''
		AND cleaned_description IS NOT NULL;
		RAISE NOTICE 'Insert silver.real_news Complete';
		RAISE NOTICE '------------------------------------';

		EXCEPTION WHEN OTHERS THEN
			RAISE NOTICE 'Error Occured During Loading Silver Layer';
			RAISE NOTICE 'Error Message: %', SQLERRM;
	END;
$$