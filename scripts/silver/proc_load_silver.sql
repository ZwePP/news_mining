/*
Overview: Stored procedure silver.load_silver() to clean and transform data from bronze to silver layer.
Example Usage:
    CALL silver.load_silver();
*/

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
		)(
		SELECT
		    REGEXP_REPLACE(LOWER(TRIM(title)), '[^a-zA-Z\\s]', '', 'g') AS cleaned_title,
		    REGEXP_REPLACE(LOWER(TRIM(text)), '[^a-zA-Z\\s]', '', 'g') AS cleaned_text,
			REGEXP_REPLACE(LOWER(TRIM(author)), '[^a-zA-Z\\s]', '', 'g') AS cleaned_author,
		    CAST(published AS DATE) AS published_date,
		    REGEXP_REPLACE(LOWER(TRIM(type)), '[^a-zA-Z\\s]', '', 'g') AS cleaned_type
		FROM bronze.fake_news
		WHERE title IS NOT NULL
		OR text IS NOT NULL);
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
		(
		SELECT
			REGEXP_REPLACE(LOWER(TRIM(headline)), '[^a-zA-Z\\s]', '', 'g') AS cleaned_headline,
			REGEXP_REPLACE(LOWER(TRIM(short_description)), '[^a-zA-Z\\s]', '', 'g') AS cleaned_description,
			REGEXP_REPLACE(LOWER(TRIM(authors)), '[^a-zA-Z\\s]', '', 'g') AS cleaned_authors,
			CAST(date AS DATE) AS cleaned_date
		 FROM bronze.real_news
		 WHERE 
		 	headline != ''
		 OR 
		 	short_description != ''
		);
		RAISE NOTICE 'Insert silver.real_news Complete';
		RAISE NOTICE '------------------------------------';

		EXCEPTION WHEN OTHERS THEN
			RAISE NOTICE 'Error Occured During Loading Silver Layer';
			RAISE NOTICE 'Error Message: %', SQLERRM;
	END;
$$