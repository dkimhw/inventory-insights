import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from config import settings
import datetime

engine = create_engine(f'postgresql://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}')

def query(sql_query):
  result = pd.read_sql_query(sqlalchemy.text(sql_query), engine)
  return result

def avg_inventory_price(start_date, end_date):
  """
    Calculates the average inventory price

    :param start_date: start time value for filtering out the inventory data
    :type start_date: str
    :param end_date: end time value for filtering out the inventory data
    :type end_date: str

    :returns: avg inventory price based on input start date and end date
    :rtype: float
  """
  sql_query = f"""
    select
      avg(price::numeric) as price
    from
      scraped_inventory_data.inventories as i
    where
      scraped_date >= '{start_date}'
      and scraped_date <= '{end_date}'
  """
  result = query(sql_query)
  return result['price'].values[0]

def avg_vehicle_year(start_date, end_date):
  """
    Calculates the average vehicle year

    start_date: start time value for filtering out the inventory data
    end_date: end time value for filtering out the inventory data

    Returns:
      Avg vehicle year based on input start date and end date
  """
  sql_query = f"""
    select
      avg(year::numeric) as year
    from
      scraped_inventory_data.inventories as i
    where
      scraped_date >= '{start_date}'
      and scraped_date <= '{end_date}'
  """
  result = query(sql_query)
  return result['year'].values[0]

def avg_vehicle_mileage(start_date, end_date):
  """
    Calculates the average vehicle mileage

    start_date: start time value for filtering out the inventory data
    end_date: end time value for filtering out the inventory data

    Returns:
      Avg vehicle mileage based on input start date and end date
  """
  sql_query = f"""
    select
      avg(mileage::numeric) as mileage
    from
      scraped_inventory_data.inventories as i
    where
      scraped_date >= '{start_date}'
      and scraped_date <= '{end_date}'
  """
  result = query(sql_query)
  return result['mileage'].values[0]

def make_count(start_date, end_date):
  """
    Calculates the number of cars by manufacturer

    start_date: specify the start time period for filtering out the inventory data for counting the num of cars by manufacturer
    end_date: specify the end time period for filtering out the inventory data for counting the num of cars by manufacturer

    returns:
      DataFrame with two columns - manufacturer & count of cars

  """
  sql_query = f"""
    select
      make
      , count(distinct vin) as vin
    from
      scraped_inventory_data.inventories as i
    where
      scraped_date >= '{start_date}'
      and scraped_date <= '{end_date}'
    group by
      1
    order by
      1 desc;
  """
  result = query(sql_query)
  return result

def avg_price_by_month(start_date, end_date):
  """
    Calculates the average price by month

    start_date: specify the start time period for filtering out the inventory data for calculating the average price by month
    end_date: specify the end time period for filtering out the inventory data for calculating the average price by month
    returns:
      DataFrame with two columns - month & average price
  """
  sql_query = f"""
    select
      DATE_TRUNC('month', scraped_date)  as inventory_month
      , avg(price::numeric) as price
    from
      scraped_inventory_data.inventories as i
    where
      scraped_date >= '{start_date}'
      and scraped_date <= '{end_date}'
    group by
      1
    order by
      1 desc;
  """
  result = query(sql_query)
  return result

def avg_dealership_inventory_size_by_month(start_date, end_date):
  """
    Calculates the average inventory size by month

    :param start_date: specify the start time period for filtering out the inventory data for calculating the average inventory size by month
    :type start_date: str
    :param end_date: specify the end time period for filtering out the inventory data for calculating the average inventory size by month
    :type end_date: str

    :returns: DataFrame with two columns - month & average inventory size
    :rtype: DataFrame
  """
  sql_query = f"""
    select
      DATE_TRUNC('month', scraped_date) as inventory_month
      , avg(mileage::numeric) as inventory_size
    from
      scraped_inventory_data.inventories as i
    where
      scraped_date >= '{start_date}'
      and scraped_date <= '{end_date}'
    group by
      1
    order by
      1 desc;
  """
  result = query(sql_query)
  return result

def make_count_by_month(start_date, end_date):
  """
    Calculates the number of cars by manufacturer & scraped month

    start_date: specify the start time period for filtering out the inventory data for counting the num of cars by manufacturer
    end_date: specify the end time period for filtering out the inventory data for counting the num of cars by manufacturer

    returns:
      DataFrame with three columns - manufacturer & inventory month & count of cars

  """
  sql_query = f"""
    SELECT
      make
      , DATE_TRUNC('month', scraped_date) as inventory_month
      , COUNT(DISTINCT vin) as count_of_vehicles
    FROM
      scraped_inventory_data.inventories
    WHERE
      scraped_date >= '{start_date}' and scraped_date <= '{end_date}'
      AND make IN (
        select
          distinct make
        from
          (select make, count(distinct vin) as cnt_vehicles from scraped_inventory_data.inventories group by 1 order by 2 desc limit 10) as a
      )
    GROUP BY
      1, 2
  """
  result = query(sql_query)
  return result

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
    SELECT
      case
        when transmission LIKE '%Automatic%' or transmission LIKE '%Auto%' then 'Automatic'
        when transmission LIKE '%Manual%' then 'Manual'
        when transmission LIKE '%CVT%' then 'Automatic'
        when transmission LIKE '%Variable' then 'Automatic'
        when transmission LIKE '%A/T%' then 'Automatic'
        when transmission LIKE '%M/T%' then 'Manual'
        else 'Unknown'
      end as transmission
      , COUNT(DISTINCT vin) as count_of_vehicles
    FROM
      scraped_inventory_data.inventories
    WHERE
      scraped_date >= '{start_date}' and scraped_date <= '{end_date}'
    GROUP BY
      1
  """
  result = query(sql_query)
  return result

def vehicle_year_count(start_date, end_date):
  '''
    Calculates the number of cars by vehicle year

    start_date: specify the start time period for filtering out the inventory data for counting the num of cars by manufacturer
    end_date: specify the end time period for filtering out the inventory data for counting the num of cars by manufacturer

    returns:
      DataFrame with two columns - year & count of cars
  '''
  sql_query = f"""
    SELECT
      year
      , COUNT(DISTINCT vin) as count_of_vehicles
    FROM
      scraped_inventory_data.inventories
    WHERE
      scraped_date >= '{start_date}' and scraped_date <= '{end_date}'
      and year > 1990
    GROUP BY
      1
    ORDER BY
      1 ASC;
  """
  result = query(sql_query)
  return result

def get_vehicle_makes():
  '''
    Gets the unique vehicle makes in the entire database

    returns:
      DataFrame with one column: vehicle make
  '''
  sql_query = f"""
    select
      distinct make
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
    Calculates the average inventory price by year & make

    start_date: specify the start time period for filtering out the inventory data for calculating the avg inventory price
    end_date: specify the end time period for filtering out the inventory data for calculating the avg inventory price
    make: list of vehicle makes to filter out the inventory data for calculating the avg inventory price

    returns:
      DataFrame with three columns - year, make, and avg inventory price
  '''
  makes_str = "','".join(makes) if makes else ''
  makes_str = f"and make in ('{makes_str}')" if makes_str != '' else ''

  sql_query = f"""
    with inventory_data as (
      SELECT
        vin
        , make
        , DATE_TRUNC('month', scraped_date) as inventory_month
        , price
        , row_number() OVER (PARTITION BY vin, DATE_TRUNC('month', scraped_date)   ORDER BY scraped_date ASC) AS filter_row
      FROM
        scraped_inventory_data.inventories
      WHERE
        scraped_date >= '{start_date}'
        and scraped_date <= '{end_date}'
        {makes_str}
    )
    select
      inventory_month,
      make,
      avg(price::numeric) as price
    from
      inventory_data
    where
      filter_row = 1
    group by
      inventory_month
      , make
    order by
      inventory_month DESC, make ASC;
  """
  result = query(sql_query)
  return result

def get_avg_mileage_by_month_and_make(start_date, end_date, makes):
  '''
    Calculates the average inventory mileage by year & make

    start_date: specify the start time period for filtering out the inventory data for calculating the avg inventory mileage
    end_date: specify the end time period for filtering out the inventory data for calculating the avg inventory mileage
    make: list of vehicle makes to filter out the inventory data for calculating the avg inventory mileage

    returns:
      DataFrame with three columns - year, make, and avg inventory mileage
  '''
  makes_str = "','".join(makes) if makes else ''
  makes_str = f"and make in ('{makes_str}')" if makes_str != '' else ''

  sql_query = f"""
    with inventory_data as (
      SELECT
        vin
        , make
        , DATE_TRUNC('month', scraped_date)  as inventory_month
        , mileage
        , row_number() OVER (PARTITION BY vin, DATE_TRUNC('month', scraped_date)  ORDER BY scraped_date ASC) AS filter_row
      FROM
        scraped_inventory_data.inventories
      WHERE
        scraped_date >= '{start_date}'
        and scraped_date <= '{end_date}'
        {makes_str}
    )
    select
      inventory_month,
      make,
      avg(mileage) as mileage
    from
      inventory_data
    where
      filter_row = 1
    group by
      inventory_month
      , make
    order by
      inventory_month DESC, make ASC;
  """
  result = query(sql_query)
  return result

def get_avg_vehicle_year_by_month_and_make(start_date, end_date, makes):
  '''
    Calculates the average inventory year by year & make

    start_date: specify the start time period for filtering out the inventory data for calculating the avg inventory year
    end_date: specify the end time period for filtering out the inventory data for calculating the avg inventory year
    make: list of vehicle makes to filter out the inventory data for calculating the avg inventory year

    returns:
      DataFrame with three columns - year, make, and avg inventory year
  '''
  makes_str = "','".join(makes) if makes else ''
  makes_str = f"and make in ('{makes_str}')" if makes_str != '' else ''

  sql_query = f"""
    with inventory_data as (
      SELECT
        vin
        , make
        , DATE_TRUNC('month', scraped_date) as inventory_month
        , year
        , row_number() OVER (PARTITION BY vin, DATE_TRUNC('month', scraped_date) ORDER BY scraped_date ASC) AS filter_row
      FROM
        scraped_inventory_data.inventories
      WHERE
        scraped_date >= '{start_date}'
        and scraped_date <= '{end_date}'
        {makes_str}
    )
    select
      inventory_month,
      make,
      round(avg(year), 0) as vehicle_year
    from
      inventory_data
    where
      filter_row = 1
    group by
      inventory_month
      , make
    order by
      inventory_month DESC, make ASC;
  """
  result = query(sql_query)
  return result


def get_make_table_data(start_date, end_date):
  '''
    Aggregated metrics for each vehicle make

    :param start_date: specify the start time period for filtering out the inventory data for calculating the aggregated metrics
    :type start_date: str
    :param end_date: specify the end time period for filtering out the inventory data for calculating the aggregated metrics
    :type end_date: str

    :returns: DataFrame with aggregated metrics for each vehicle make
    :rtype: DataFrame
  '''
  sql_query = f"""
    select
      make,
      count(distinct vin) as total_inventory,
      round(avg(year), 0) as avg_vehicle_year,
      round(avg(price::numeric), 0) as avg_price,
      round(avg(mileage), 0) as avg_mileage,
      (select exterior_color from inventory as i2
        where i2.make = i.make and exterior_color is not null order by scraped_date desc limit 1) as most_popular_exterior_color
    from
      scraped_inventory_data.inventories as i
    where
      scraped_date >= '{start_date}'
      and scraped_date <= '{end_date}'
    group by
      make
    order by
      make asc;
  """
  result = query(sql_query)
  return result
