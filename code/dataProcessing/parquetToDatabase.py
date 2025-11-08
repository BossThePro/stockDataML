# This file will aim to move the parquet file into a duckdb database for quicker and better access
import duckdb
db = duckdb.connect("stockData.db")
db.execute("CREATE TABLE stockTable AS SELECT * FROM parquet_scan('../../data/stockPullClean.parquet')")
results = db.execute("SELECT * FROM stockTable").df()
print(results)
