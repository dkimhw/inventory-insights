

import sqlite3
import pandas as pd

TABLE_NAME = 'inventory'
DB_NAME = '../data/cars.db'

def productionize():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  check_tbl_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TABLE_NAME}';"
  tbl_info = pd.read_sql_query(check_tbl_query, conn)

  if (tbl_info.empty):
    print("No such table exists.");

    # Create replica table from inventory_staging
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} AS SELECT * FROM inventory_staging LIMIT 1;")
    print(f"{TABLE_NAME} was created.")
    conn.commit()

    # Truncate all rows
    cursor.execute(f"DELETE FROM {TABLE_NAME};")
    conn.commit()

  # Insert everything from inventory_staging
  cursor.execute(f"INSERT INTO {TABLE_NAME} SELECT * FROM inventory_staging;")
  conn.commit()

  # Truncate inventory_staging
  cursor.execute(f"DELETE FROM inventory_staging;")
  conn.commit()

  #Closing the connection
  conn.close()
