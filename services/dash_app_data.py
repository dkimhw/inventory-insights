import query as q
# https://towardsdatascience.com/the-good-way-to-structure-a-python-project-d914f27dfcc9

def query_inventory_data():
  '''
    Returns:
      Average price of used cars of the current month
  '''
  sql_query = """
    SELECT
      *
    FROM inventory;
  """
  result = q.query(sql_query)
  return result

# print(query_inventory_data().head())


def avg_price_month(month_year):
  inv = query_inventory_data()
  print(inv['scraped_date'][0])


avg_price_month('2022-01-01')
