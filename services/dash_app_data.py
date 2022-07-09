import pandas as pd
# https://towardsdatascience.com/the-good-way-to-structure-a-python-project-d914f27dfcc9
import sqlite3

CONN = sqlite3.connect('./data/cars.db')

def query(sql_query):
  result = pd.read_sql_query(sql_query, CONN)
  return result

def query_inventory_data():
  '''
    Returns:
      The full scarped used car inventory dataframe
  '''
  sql_query = """
    SELECT
      *
    FROM inventory;
  """
  result = query(sql_query)
  return result

def avg_price_last_scraped_month():
  """
    Returns:
      Avg price of the last scraped month
  """
  inv = query_inventory_data()
  inv['scraped_date'] = pd.to_datetime(inv['scraped_date'])

  # Parse scraped date
  last_scraped_date = max(inv['scraped_date'])
  last_scraped_month = last_scraped_date.month
  last_scraped_year = last_scraped_date.year

  return inv.loc[ (inv['scraped_date'].dt.month == last_scraped_month) & (inv['scraped_date'].dt.year == last_scraped_year)
  , ['price']].mean()[0]

def manufacturer_bar_char_count():
  inv = query_inventory_data()
  return inv
