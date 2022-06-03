
import sqlite3
import pandas as pd

connection = sqlite3.connect('cars.db')
avg_inv_price_current_month_query = """
SELECT
  AVG(price) as avg_price
FROM inventory
WHERE date(scraped_date, 'start of month') = '2022-05-01';
"""

# WHERE
# date(scraped_date, 'start of month') = date('now', 'start of month')

def avg_price_current_month():
  result = pd.read_sql_query(avg_inv_price_current_month_query, connection)
  return result['avg_price'].loc[0];

print(avg_price_current_month())
