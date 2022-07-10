import pandas as pd
# https://towardsdatascience.com/the-good-way-to-structure-a-python-project-d914f27dfcc9
import sqlite3

CONN = sqlite3.connect('./data/cars.db')

def query(sql_query):
  result = pd.read_sql_query(sql_query, CONN)
  return result

def query_inventory_data():
  '''
    Returns the inventory table from cars.db

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
    Calculates the average price based on last scraped month

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


def make_bar_char_count(start_date, end_date):
  """
    Calculates the number of cars by manufacturer

    start_date: specify the start time period for filtering out the inventory data for counting the num of cars by manufacturer
    end_date: specify the end time period for filtering out the inventory data for counting the num of cars by manufacturer

    returns:
      DataFrame with two columns - manufacturer & count of cars

  """
  inv = query_inventory_data()
  print(inv.shape)
  print(inv.vin.isnull().sum())
  inv['scraped_date'] = pd.to_datetime(inv['scraped_date'])
  for i, row in inv.iterrows():
      new_val = row['scraped_date'].strftime('%Y-%m-%d')
      inv.at[i,'scraped_date'] = new_val

  inv = inv.loc[ (inv['scraped_date'] >= start_date) & (inv['scraped_date'] <= end_date), :]

  make_count = inv.groupby(['make'], as_index = False).vin.nunique()
  print(make_count)
  return inv
