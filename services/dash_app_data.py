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

  # It is possible to have multiple same vin in a month (e.g. we scraped it multiple times during the same month)
  # For this dashboard we want to make sure we are only counting one vehicle per month. The reason is imagine we had only 3 cars in the dataset. If two of those were the same vin for the same month - the average we take would be biased towards that particular vin.
  # Example vin: 19UDE2F70KA002008
  sql_query = """
    with inventory_data as (
    SELECT
      *
      , row_number() OVER (PARTITION BY vin, DATE(scraped_date, 'start of month')  ORDER BY scraped_date ASC) AS filter_row
    FROM inventory
    )
    select * from inventory_data where filter_row = 1;
  """
  result = query(sql_query)
  # 19UDE2F70KA002008
  result['scraped_date'] = pd.to_datetime(result['scraped_date'], format='%Y-%m-%d')

  # For vehicles that there was no VIN data use title + scraped_month (Y-m) format as the key for count distincts
  for i, row in result.iterrows():
      if (not row['vin']):
        scraped_month_year = row['scraped_date'].strftime('%Y-%m')
        unique_id = row['title'] + ' - ' + row['dealership_name'] + ' - ' + scraped_month_year
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

def avg_dealership_inventory_size_by_month(start_date, end_date):
  """
    Calculates the average inventory size by month

    start_date: specify the start time period for filtering out the inventory data for calculating the average inventory size by month
    end_date: specify the end time period for filtering out the inventory data for calculating the average inventory size by month
    returns:
      DataFrame with two columns - month & average inventory size
  """
  inv = query_inventory_data()
  inv['inventory_month'] = pd.to_datetime(inv['scraped_date'])
  for i, row in inv.iterrows():
      #new_datetime_obj = datetime.strptime(row['scraped_date'], '%Y-%m-%d')
      new_val = datetime.date(row['scraped_date'].year, row['scraped_date'].month, 1).strftime('%Y-%m-%d')
      inv.at[i,'inventory_month'] = new_val


  inv = inv.loc[ (inv['scraped_date'] >= start_date) & (inv['scraped_date'] <= end_date), :]

  avg_inv_size_by_month = inv.groupby(['inventory_month'], as_index = False).agg({
    'vin': pd.Series.nunique
    , 'dealership_name': pd.Series.nunique
  })

  avg_inv_size_by_month['inventory_size'] = round(avg_inv_size_by_month['vin'] / avg_inv_size_by_month['dealership_name'], 0)
  avg_inv_size_by_month.sort_values(by="inventory_month", ascending = False, inplace=True)
  return avg_inv_size_by_month.loc[:, ['inventory_month', 'inventory_size']]


def make_count_by_month(start_date, end_date):
  """
    Calculates the number of cars by manufacturer & scraped month

    start_date: specify the start time period for filtering out the inventory data for counting the num of cars by manufacturer
    end_date: specify the end time period for filtering out the inventory data for counting the num of cars by manufacturer

    returns:
      DataFrame with three columns - manufacturer & inventory month & count of cars

  """
  inv = query_inventory_data()
  inv['inventory_month'] = pd.to_datetime(inv['scraped_date'])
  for i, row in inv.iterrows():
      #new_datetime_obj = datetime.strptime(row['scraped_date'], '%Y-%m-%d')
      new_val = datetime.date(row['scraped_date'].year, row['scraped_date'].month, 1).strftime('%Y-%m-%d')
      inv.at[i,'inventory_month'] = new_val
  inv = inv.loc[ (inv['scraped_date'] >= start_date) & (inv['scraped_date'] <= end_date), :]

  make_count = inv.groupby(['make'], as_index = False).vin.nunique()
  make_count.sort_values(by="vin", ascending = False, inplace=True)
  top_makes = make_count.head(10)
  # df.country.isin(countries_to_keep)

  make_date_count = inv.groupby(['make', 'inventory_month'], as_index = False).vin.nunique()
  make_date_count = make_date_count.loc[make_date_count['make'].isin(top_makes['make']), :]
  make_date_count.sort_values(by="inventory_month", ascending = False, inplace=True)
  return make_date_count


def transmission_type_count(start_date, end_date):
  '''
    Calculates the number of cars by transmission type

    start_date: specify the start time period for filtering out the inventory data for counting the num of cars by manufacturer
    end_date: specify the end time period for filtering out the inventory data for counting the num of cars by manufacturer

    returns:
      DataFrame with two columns - transmission type & count of cars
  '''

  # It is possible to have multiple same vin in a month (e.g. we scraped it multiple times during the same month)
  # For this dashboard we want to make sure we are only counting one vehicle per month. The reason is imagine we had only 3 cars in the dataset. If two of those were the same vin for the same month - the average we take would be biased towards that particular vin.
  # Example vin: 19UDE2F70KA002008
  sql_query = f"""
    with inventory_data as (
      SELECT
        coalesce(vin, title + ' ' + dealership_name + ' - ' + DATE(scraped_date, 'start_month')) as vin
        , case
            when transmission LIKE '%Automatic%' then 'Automatic'
            when transmission LIKE '%Manual%' then 'Manual'
          end as transmission
        , row_number() OVER (PARTITION BY vin, DATE(scraped_date, 'start of month')  ORDER BY scraped_date ASC) AS filter_row
      FROM
        inventory
      WHERE
        scraped_date >= '{start_date}' and scraped_date <= '{end_date}'
    )
    select
      *
    from
      inventory_data
    where
      filter_row = 1;
  """
  result = query(sql_query)
  transmission_cnt = result.groupby(['transmission'], as_index = False).vin.nunique()
  return transmission_cnt
