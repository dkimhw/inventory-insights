import pandas as pd
# https://towardsdatascience.com/the-good-way-to-structure-a-python-project-d914f27dfcc9
import sqlite3
import datetime

CONN = sqlite3.connect('./data/cars.db', check_same_thread=False)

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
  result['scraped_date'] = pd.to_datetime(result['scraped_date'], format='%Y-%m-%d')

  # For vehicles that there was no VIN data use title + scraped_month (Y-m) format as the key for count distincts
  for i, row in result.iterrows():
      if (not row['vin']):
        scraped_month_year = row['scraped_date'].strftime('%Y-%m')
        unique_id = row['title'] + ': ' + scraped_month_year
        result.at[i, 'vin'] = unique_id

  return result


def avg_inventory_price(start_date, end_date):
  """
    Calculates the average inventory price

    start_date: start time value for filtering out the inventory data
    end_date: end time value for filtering out the inventory data

    Returns:
      Avg inventory price based on input start date and end date
  """
  inv = query_inventory_data()
  inv = inv.loc[ (inv['scraped_date'] >= start_date) & (inv['scraped_date'] <= end_date), :]
  inv['price'] = inv['price'].astype(str).astype(float)
  return inv['price'].mean()



def avg_vehicle_year(start_date, end_date):
  """
    Calculates the average vehicle year

    start_date: start time value for filtering out the inventory data
    end_date: end time value for filtering out the inventory data

    Returns:
      Avg vehicle year based on input start date and end date
  """
  inv = query_inventory_data()
  inv = inv.loc[ (inv['scraped_date'] >= start_date) & (inv['scraped_date'] <= end_date), :]
  inv['year'] = inv['year'].astype(str).astype(int)

  return inv['year'].mean()

def avg_vehicle_mileage(start_date, end_date):
  """
    Calculates the average vehicle mileage

    start_date: start time value for filtering out the inventory data
    end_date: end time value for filtering out the inventory data

    Returns:
      Avg vehicle mileage based on input start date and end date
  """
  inv = query_inventory_data()
  inv = inv.loc[ (inv['scraped_date'] >= start_date) & (inv['scraped_date'] <= end_date), :]
  inv['vehicle_mileage'] = inv['vehicle_mileage'].astype(str).astype(float)

  return inv['vehicle_mileage'].mean()

def make_count(start_date, end_date):
  """
    Calculates the number of cars by manufacturer

    start_date: specify the start time period for filtering out the inventory data for counting the num of cars by manufacturer
    end_date: specify the end time period for filtering out the inventory data for counting the num of cars by manufacturer

    returns:
      DataFrame with two columns - manufacturer & count of cars

  """
  inv = query_inventory_data()
  for i, row in inv.iterrows():
      new_val = row['scraped_date'].strftime('%Y-%m-%d')
      inv.at[i,'scraped_date'] = new_val

  inv = inv.loc[ (inv['scraped_date'] >= start_date) & (inv['scraped_date'] <= end_date), :]

  make_count = inv.groupby(['make'], as_index = False).vin.nunique()
  return make_count

def avg_price_by_month(start_date, end_date):
  """
    Calculates the average price by month

    start_date: specify the start time period for filtering out the inventory data for calculating the average price by month
    end_date: specify the end time period for filtering out the inventory data for calculating the average price by month
    returns:
      DataFrame with two columns - month & average price
  """
  inv = query_inventory_data()
  inv['inventory_month'] = pd.to_datetime(inv['scraped_date'])
  for i, row in inv.iterrows():
      #new_datetime_obj = datetime.strptime(row['scraped_date'], '%Y-%m-%d')
      new_val = datetime.date(row['scraped_date'].year, row['scraped_date'].month, 1).strftime('%Y-%m-%d')
      inv.at[i,'inventory_month'] = new_val


  inv = inv.loc[ (inv['scraped_date'] >= start_date) & (inv['scraped_date'] <= end_date), :]
  avg_price_by_month = inv.groupby(['inventory_month'], as_index = False).price.mean()
  avg_price_by_month.sort_values(by="inventory_month", ascending = False, inplace=True)
  return avg_price_by_month
