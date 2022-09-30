from re import S
from services.query_util import query

def get_vehicle_makes():
  '''
  Returns a dataframe that contains a list of unique vehicle makes

  :returns: DataFrame with one column - vehicle make
  :rtype: DataFrame
  '''
  sql_query = f"""
    select
      distinct INITCAP(make) as make
    from
      scraped_inventory_data.inventories
    where make is not null
    order by
      make;
  """
  result = query(sql_query)
  result = result['make'].tolist()
  return result

def get_avg_price_by_month_and_make(start_date, end_date, makes):
  '''
  Returns a dataframe with average inventory price by year & make

  :params start_date: specify the start time period for filtering out the inventory data for calculating the avg inventory price
  :type start_date: str
  :params end_date: specify the end time period for filtering out the inventory data for calculating the avg inventory price
  :type end_date: str
  :params make: list of vehicle makes to filter out the inventory data for calculating the avg inventory price
  :type make: list

  :returns: DataFrame with three columns - year, make, and avg inventory price
  :rtype: DataFrame
  '''
  makes_str = "','".join(makes) if makes else ''
  makes_str = f"and make in ('{makes_str}')" if makes_str != '' else ''

  sql_query = f"""
    select
      scraped_month as inventory_month,
      INITCAP(make) as make,
      avg(price::numeric) as price
    FROM
      scraped_inventory_data.inventories
    WHERE
      scraped_date >= '{start_date}'
      and scraped_date <= '{end_date}'
      {makes_str}
    group by
      1, 2
    order by
      1 DESC, 2 ASC;
  """
  result = query(sql_query)
  return result

def get_avg_mileage_by_month_and_make(start_date, end_date, makes):
  '''
  Returns a dataframe containing the average inventory mileage by year & make

  :params start_date: specify the start time period for filtering out the inventory data for calculating the avg inventory mileage
  :type start_date: str
  :params end_date: specify the end time period for filtering out the inventory data for calculating the avg inventory mileage
  :type end_date: str
  :params make: list of vehicle makes to filter out the inventory data for calculating the avg inventory mileage
  :type make: list

    returns:
      DataFrame with three columns - year, make, and avg inventory mileage
  '''
  makes_str = "','".join(makes) if makes else ''
  makes_str = f"and make in ('{makes_str}')" if makes_str != '' else ''

  sql_query = f"""
    select
      scraped_month as inventory_month,
      INITCAP(make) as make,
      avg(mileage) as mileage
    from
      scraped_inventory_data.inventories
    where
      scraped_date >= '{start_date}'
      and scraped_date <= '{end_date}'
      {makes_str}
    group by
      1, 2
    order by
      1 DESC, 2 ASC;
  """
  result = query(sql_query)
  return result

def get_avg_vehicle_year_by_month_and_make(start_date, end_date, makes):
  '''
  Returns a dataframe containing  the average inventory year by year & make

  :params start_date: specify the start time period for filtering out the inventory data for calculating the avg inventory year
  :type start_date: str
  :params end_date: specify the end time period for filtering out the inventory data for calculating the avg inventory year
  :type end_date: str
  :params make: list of vehicle makes to filter out the inventory data for calculating the avg inventory year
  :type make: list

  :returns: DataFrame with three columns - year, make, and avg inventory year
  :rtype: DataFrame
  '''
  makes_str = "','".join(makes) if makes else ''
  makes_str = f"and make in ('{makes_str}')" if makes_str != '' else ''

  sql_query = f"""
    select
      scraped_month as inventory_month,
      INITCAP(make) as make,
      round(avg(year), 0) as vehicle_year
    from
      scraped_inventory_data.inventories
    where
      scraped_date >= '{start_date}'
      and scraped_date <= '{end_date}'
      {makes_str}
    group by
      1, 2
    order by
      1 DESC, 2 ASC;
  """
  result = query(sql_query)
  return result

def get_make_model_trim_data(start_date, end_date, makes):
  '''
  Returns a dataframe containing aggregated metrics for each vehicle make model trim

  :params start_date: specify the start time period for filtering out the inventory data for calculating the avg inventory year
  :type start_date: str
  :params end_date: specify the end time period for filtering out the inventory data for calculating the avg inventory year
  :type end_date: str
  :params make: list of vehicle makes to filter out the inventory data for calculating the avg inventory year
  :type make: list

  :returns: a dataframe containing aggregated metrics for each vehicle make model trim
  :rtype: DataFrame
  '''
  makes_str = "','".join(makes) if makes else ''
  makes_str = f"and make in ('{makes_str}')" if makes_str != '' else ''

  sql_query = f"""
    select
      INITCAP(make) || ' ' || model_trim as vehicle_model_title,
      count(distinct vin) as total_inventory,
      round(avg(year), 0) as avg_vehicle_year,
      round(avg(price::numeric), 0) as avg_price,
      round(avg(mileage), 0) as avg_mileage
    from
      scraped_inventory_data.inventories
    where
      scraped_date >= '{start_date}'
      and scraped_date <= '{end_date}'
      {makes_str}
    group by
      1
    order by
      2 DESC;
  """
  result = query(sql_query)
  return result
