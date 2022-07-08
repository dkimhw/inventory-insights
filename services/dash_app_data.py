import query as q
import pandas as pd
# https://towardsdatascience.com/the-good-way-to-structure-a-python-project-d914f27dfcc9

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
  result = q.query(sql_query)
  return result

# print(query_inventory_data().head())

"""
  Returns:
    Avg price of the last scraped month
"""
def avg_price_last_scraped_month():
  inv = query_inventory_data()
  inv['scraped_date'] = pd.to_datetime(inv['scraped_date'])

  # Parse scraped date
  last_scraped_date = max(inv['scraped_date'])
  last_scraped_month = last_scraped_date.month
  last_scraped_year = last_scraped_date.year

  print(last_scraped_month)
  print(inv.loc[(inv['scraped_date'].dt.month == last_scraped_month), ['vin', 'dealership_name', 'price', 'scraped_date']])


avg_price_last_scraped_month()
