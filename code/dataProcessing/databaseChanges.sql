-- This aims to note down all noteworthy SQL commands for my project.

-- Creating a temp table for testing out the adding of different measures
CREATE TABLE stockTest AS SELECT * FROM stockTable WHERE(Ticker='AAPL');

-- Adding percentage column to the test table
ALTER TABLE stockTest ADD COLUMN Percentage DOUBLE;

-- Adding values to the percentage column to the test table 

-- 100 * (CLOSE/OPEN) - 100
UPDATE stockTest SET Percentage = 100 * (Close/Open) - 100; 

-- Adding high/low percentage column to test table:
ALTER TABLE stockTest ADD COLUMN LowHighPercentage DOUBLE;

-- Adding values to the low/high percentage column to the test table: 
UPDATE stockTest SET LowHighPercentage = 100 * (High/Low) - 100; 

-- Adding three day moving average

ALTER TABLE stockTest ADD COLUMN ThreeDaySimpleAverage DOUBLE;

WITH Averages AS ( SELECT Date, Ticker, ROW_NUMBER() OVER ( 
			PARTITION BY Ticker 
			ORDER BY Date) 
		AS rn, 
        Avg(Close) OVER ( 
			PARTITION BY Ticker 
			ORDER BY Date 
			ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) 
		AS CalculatedAvg
FROM stockTest
)

UPDATE stockTest
SET ThreeDaySimpleAverage = 
	-- We have to set the row number to null when theres less than three days in the moving average due to there not being three days of data available
    CASE 
        WHEN Averages.rn < 3 THEN NULL 
        ELSE Averages.CalculatedAvg   
    END
FROM Averages
WHERE 
    stockTest.Date = Averages.Date
    AND stockTest.Ticker = Averages.Ticker;

-- Adding 50-day moving average 


ALTER TABLE stockTest ADD COLUMN FiftyDaySimpleAverage DOUBLE;

WITH Averages AS ( SELECT Date, Ticker, ROW_NUMBER() OVER ( 
			PARTITION BY Ticker 
			ORDER BY Date) 
		AS rn, 
        Avg(Close) OVER ( 
			PARTITION BY Ticker 
			ORDER BY Date 
			ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) 
		AS CalculatedAvg
FROM stockTest
)

UPDATE stockTest
SET FiftyDaySimpleAverage = 
	-- We have to set the row number to null when theres less than fifty days in the moving average due to there not being fifty days of data available
    CASE 
        WHEN Averages.rn < 50 THEN NULL 
        ELSE Averages.CalculatedAvg   
    END
FROM Averages
WHERE 
    stockTest.Date = Averages.Date
    AND stockTest.Ticker = Averages.Ticker;

-- Adding 200-day moving average

ALTER TABLE stockTest ADD COLUMN TwoHundredDaySimpleAverage DOUBLE;

WITH Averages AS ( SELECT Date, Ticker, ROW_NUMBER() OVER ( 
			PARTITION BY Ticker 
			ORDER BY Date) 
		AS rn, 
        Avg(Close) OVER ( 
			PARTITION BY Ticker 
			ORDER BY Date 
			ROWS BETWEEN 199 PRECEDING AND CURRENT ROW) 
		AS CalculatedAvg
FROM stockTest
)

UPDATE stockTest
SET TwoHundredDaySimpleAverage = 
	-- We have to set the row number to null when theres less than fifty days in the moving average due to there not being fifty days of data available
    CASE 
        WHEN Averages.rn < 200 THEN NULL 
        ELSE Averages.CalculatedAvg   
    END
FROM Averages
WHERE 
    stockTest.Date = Averages.Date
    AND stockTest.Ticker = Averages.Ticker;
