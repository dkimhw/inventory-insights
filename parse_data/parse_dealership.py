
import parse_inventory as pi
import pandas as pd
from datetime import datetime

# Functions to parse specific dealership web data
def get_direct_auto_inventory_data(soup, dealership_info, url):
    # Initialize empty data frame & dictionary
    cars = pd.DataFrame()
    cars_dict = {}

    # Parse title
    title = pi.parse_subsection(soup, 'div', 'h2', 'ml-0 ml-lg-5 pt-4 pb-2 border-bottom', 'ebiz-vdp-title color m-0')
    valid_len_data = len(title)

    # Parse year, make, model_trim, vehicle_type, model, trim
    years = pi.get_valid_year(title)
    makes, model_trim, vehicle_type = pi.get_car_make_model_type(title)

    # Model & Trim
    # Not easily prasable for this dealership - set to None
    models = [None] * valid_len_data
    trim = pi.parse_subsection(soup, 'div', 'h3', 'ml-0 ml-lg-5 pt-4 pb-2 border-bottom', 'ebiz-vdp-subtitle h4 body-font m-0')

    # ebiz-vdp-subtitle h4 body-font m-0
    # Add mileage col
    miles = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'li', 'ml-0 ml-lg-5 pt-4 pb-2 border-bottom', 'mileage-units', 'get_text'))

    # Add price
    car_prices = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'h4', 'ml-0 ml-lg-5 pt-4 pb-2 border-bottom', 'money-sign-disp body-font d-inline m-0', 'get_text'))

    # Misc car information
    exterior_color = pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'exterior')
    interior_color = pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'interior')
    transmission = pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'transmission')
    engine = pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'engine')
    drivetrain = [None] * valid_len_data
    vin = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'li', 'ml-0 ml-lg-5 pt-4 pb-2 border-bottom', 'vin', 'get_text'), 'VIN #')

    # Append all parsed data to cars_list
    cars_dict['title'] = title
    cars_dict['year'] = years
    cars_dict['make'] = makes
    cars_dict['model_trim'] = model_trim
    cars_dict['vehicle_type'] = vehicle_type
    cars_dict['model'] = models
    cars_dict['trim'] = trim
    cars_dict['vehicle_mileage'] = miles
    cars_dict['price'] = car_prices
    cars_dict['exterior_color'] = exterior_color
    cars_dict['interior_color'] = interior_color
    cars_dict['transmission'] = transmission
    cars_dict['engine'] = engine
    cars_dict['drivetrain'] = drivetrain
    cars_dict['vin'] = vin

    # Check if data is valid
    is_valid = pi.data_length_validation(cars_dict, valid_len_data)

    if (is_valid):
      # If valid create cars dataframe to return
      for key in cars_dict:
        pi.add_column_df(cars, cars_dict[key], key)

      # Add dealership info
      cars['dealership_name'] = dealership_info['dealership_name']
      cars['dealership_address'] = dealership_info['address']
      cars['dealership_zipcode'] = dealership_info['zipcode']
      cars['dealership_city'] = dealership_info['city']
      cars['dealership_state'] = dealership_info['state']
      cars['inventory_url'] = dealership_info['url']
      cars['scraped_date'] = datetime.now(tz = None)

      # Specific changes
      cars['model'] = cars['model_trim']
      cars['model_trim'] = cars['model_trim'] + ' ' + cars['trim']
      cars['title'] = cars['year'].apply(str) + ' ' + cars['make'] + ' ' + cars['model_trim']

      return cars
    else:
      error_df = pd.DataFrame()
      error_df.at[0, 'error'] = 'Data Validation'
      error_df.at[0, 'dealership'] = dealership_info['dealership_name']
      error_df.at[0, 'date'] = datetime.now(tz = None)
      error_df.at[0, 'url'] = url
      return error_df

def get_bostonyan_inventory_data(soup, dealership_info, url):
    # Initialize empty data frame & dictionary
    cars = pd.DataFrame()
    cars_dict = {}

    # Add vehicle title
    title = pi.parse_subsection(soup, 'div', 'a', 'col- dynamic-col', 'accent-color1')
    valid_len_data = len(title)

    # Parse year, make, model_trim, vehicle_type, model, trim
    years = pi.get_valid_year(title)
    makes, model_trim, vehicle_type = pi.get_car_make_model_type(title)
    # Not easily prasable for this dealership - set to None
    makes = pi.parse_subsection_attr(soup, 'data-displaymake', 'div', 'div', 'col- dynamic-col', 'clearfix inventory-panel palette-bg2 vehicle lot-00')
    models = pi.parse_subsection_attr(soup, 'data-displaymodel', 'div', 'div', 'col- dynamic-col', 'clearfix inventory-panel palette-bg2 vehicle lot-00')
    trim = pi.parse_subsection_attr(soup, 'data-displaytrim', 'div', 'div', 'col- dynamic-col', 'clearfix inventory-panel palette-bg2 vehicle lot-00')

    # Add mileage col
    miles = pi.convert_to_numeric_type(pi.parse_subsection_attr(soup, 'data-displaymileage', 'div', 'div', 'col- dynamic-col', 'clearfix inventory-panel palette-bg2 vehicle lot-00'))

    # Add price
    car_prices = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'div', 'col- dynamic-col', 'pricevalue1 accent-color1', 'get_text'))

    # Add Colors & transmission & other cols
    exterior_color = pi.parse_subsection(soup, 'div', 'span', 'col- dynamic-col', 'Extcolor', 'get_text')
    interior_color = pi.parse_subsection(soup, 'div', 'span', 'col- dynamic-col', 'Intcolor', 'get_text')
    transmission = pi.parse_subsection(soup, 'div', 'div', 'col- dynamic-col', 'transmission', 'get_text')
    engine = pi.parse_subsection_attr(soup, 'data-displayengine', 'div', 'div', 'col- dynamic-col', 'clearfix inventory-panel palette-bg2 vehicle lot-00')
    drivetrain = pi.parse_subsection_attr(soup, 'data-displaydrivetrain', 'div', 'div', 'col- dynamic-col', 'clearfix inventory-panel palette-bg2 vehicle lot-00')
    vin = pi.parse_subsection(soup, 'div', 'span', 'col- dynamic-col', 'vin', 'get_text')

    # Append all parsed data to cars_list
    cars_dict['title'] = title
    cars_dict['year'] = years
    cars_dict['make'] = makes
    cars_dict['model_trim'] = model_trim
    cars_dict['vehicle_type'] = vehicle_type
    cars_dict['model'] = models
    cars_dict['trim'] = trim
    cars_dict['vehicle_mileage'] = miles
    cars_dict['price'] = car_prices
    cars_dict['exterior_color'] = exterior_color
    cars_dict['interior_color'] = interior_color
    cars_dict['transmission'] = transmission
    cars_dict['engine'] = engine
    cars_dict['drivetrain'] = drivetrain
    cars_dict['vin'] = vin

    # Check if data is valid
    is_valid = pi.data_length_validation(cars_dict, valid_len_data)

    if (is_valid):
      # If valid create cars dataframe to return
      for key in cars_dict:
        pi.add_column_df(cars, cars_dict[key], key)

      # Add dealership info
      cars['dealership_name'] = dealership_info['dealership_name']
      cars['dealership_address'] = dealership_info['address']
      cars['dealership_zipcode'] = dealership_info['zipcode']
      cars['dealership_city'] = dealership_info['city']
      cars['dealership_state'] = dealership_info['state']
      cars['inventory_url'] = dealership_info['url']
      cars['scraped_date'] = datetime.now(tz = None)

      # Additional changes to data
      for idx, row in cars.iterrows():
        if row['model'] == 'Other':
          cars.at[idx, 'model'] = None
          cars.at[idx, 'model_trim'] = row['trim']
        else:
          cars.at[idx, 'model_trim'] = row['model'] + ' ' + row['trim']
      cars['title'] = cars['year'] + ' ' + cars['make'] + ' ' + cars['model_trim']

      return cars
    else:
      error_df = pd.DataFrame()
      error_df.at[0, 'error'] = 'Data Validation'
      error_df.at[0, 'dealership'] = dealership_info['dealership_name']
      error_df.at[0, 'date'] = datetime.now(tz = None)
      error_df.at[0, 'url'] = url
      return error_df

def get_fafama_inventory_data(soup, dealership_info, url):
    # Initialize empty data frame & dictionary
    cars = pd.DataFrame()
    cars_dict = {}

    # Add title
    title = pi.parse_subsection(soup, 'div', 'h2', 'ml-0 ml-lg-5 pt-4 pb-2 border-bottom', 'color m-0 ebiz-vdp-title')
    valid_len_data = len(title)

    # Parse year, make, model_trim, vehicle_type, model, trim
    years = pi.get_valid_year(title)
    makes, model_trim, vehicle_type = pi.get_car_make_model_type(title)
    models = [None] * valid_len_data
    trim = [None] * valid_len_data

    # Add mileage col
    miles = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'li', 'ml-0 ml-lg-5 pt-4 pb-2 border-bottom', 'mileage-units', 'get_text'))

    # Add price
    car_prices = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'div', 'ml-0 ml-lg-5 pt-4 pb-2 border-bottom', 'price-item active mt-3 mt-md-0', 'get_text'))

    # Misc car information
    exterior_color = pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'exterior')
    interior_color = pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'interior')
    transmission = pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'transmission')
    engine = pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'engine')
    drivetrain = [None] * valid_len_data
    vin = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'li', 'ml-0 ml-lg-5 pt-4 pb-2 border-bottom', 'vin', 'get_text'), 'VIN #')

    # Append all parsed data to cars_list
    cars_dict['title'] = title
    cars_dict['year'] = years
    cars_dict['make'] = makes
    cars_dict['model_trim'] = model_trim
    cars_dict['vehicle_type'] = vehicle_type
    cars_dict['model'] = models
    cars_dict['trim'] = trim
    cars_dict['vehicle_mileage'] = miles
    cars_dict['price'] = car_prices
    cars_dict['exterior_color'] = exterior_color
    cars_dict['interior_color'] = interior_color
    cars_dict['transmission'] = transmission
    cars_dict['engine'] = engine
    cars_dict['drivetrain'] = drivetrain
    cars_dict['vin'] = vin

    # Check if data is valid
    is_valid = pi.data_length_validation(cars_dict, valid_len_data)

    if (is_valid):
      # If valid create cars dataframe to return
      for key in cars_dict:
        pi.add_column_df(cars, cars_dict[key], key)

      # Add dealership info
      cars['dealership_name'] = dealership_info['dealership_name']
      cars['dealership_address'] = dealership_info['address']
      cars['dealership_zipcode'] = dealership_info['zipcode']
      cars['dealership_city'] = dealership_info['city']
      cars['dealership_state'] = dealership_info['state']
      cars['inventory_url'] = dealership_info['url']
      cars['scraped_date'] = datetime.now(tz = None)

      # Additional changes to data
      pi.fix_vehicle_type(cars)
      cars['title'] = cars['year'] + ' ' + cars['title']

      return cars
    else:
      error_df = pd.DataFrame()
      error_df.at[0, 'error'] = 'Data Validation'
      error_df.at[0, 'dealership'] = dealership_info['dealership_name']
      error_df.at[0, 'date'] = datetime.now(tz = None)
      error_df.at[0, 'url'] = url
      return error_df

def get_newton_auto_inventory_data(soup, dealership_info, url):
    # Initialize empty data frame & dictionary
    cars = pd.DataFrame()
    cars_dict = {}

    # Add title
    title = pi.parse_subsection(soup, 'div', 'h3', 'vehicle-snapshot__information', 'vehicle-snapshot__title')
    valid_len_data = len(title)

    # Prse year, make, model_trim, vehicle_type, model, trim
    years = pi.get_valid_year(title)
    makes, model_trim, vehicle_type = pi.get_car_make_model_type(title)
    models = [None] * valid_len_data
    trim = [None] * valid_len_data

    # Parse numeric data (price; mileage - has same class name)
    miles_and_price = pi.convert_to_numeric_type(pi.parse_subsection_all(soup, 'div', 'div', 'vehicle-snapshot__information', 'vehicle-snapshot__main-info font-primary'))
    car_prices = [el for idx, el in enumerate(miles_and_price) if idx % 2 == 0]
    miles = [el for idx, el in enumerate(miles_and_price) if idx % 2 != 0]

    # Misc car information
    vehicle_info = pi.parse_tag(soup, 'div', 'vehicle-snapshot__info-text-container')

    # Colors
    exterior_color = vehicle_info[1::6]
    exterior_color = [el.replace('Exterior Color', '').strip() for el in exterior_color]
    interior_color = vehicle_info[3::6]
    interior_color = [el.replace('Interior Color', '').strip() for el in interior_color]
    # Transmission
    transmission = vehicle_info[2::6]
    transmission = [el.replace('Transmission', '').strip() for el in transmission]
    # Engine
    engine = vehicle_info[::6]
    engine = [el.replace('Engine', '').strip() for el in engine]
    # Drive Train
    drivetrain = vehicle_info[4::6]
    drivetrain = [el.replace('Drivetrain', '').strip() for el in drivetrain]
    # No VIN that can be scraped
    vin = [None] * valid_len_data

    # Append all parsed data to cars_list
    cars_dict['title'] = title
    cars_dict['year'] = years
    cars_dict['make'] = makes
    cars_dict['model_trim'] = model_trim
    cars_dict['vehicle_type'] = vehicle_type
    cars_dict['model'] = models
    cars_dict['trim'] = trim
    cars_dict['vehicle_mileage'] = miles
    cars_dict['price'] = car_prices
    cars_dict['exterior_color'] = exterior_color
    cars_dict['interior_color'] = interior_color
    cars_dict['transmission'] = transmission
    cars_dict['engine'] = engine
    cars_dict['drivetrain'] = drivetrain
    cars_dict['vin'] = vin

    # Check if data is valid
    is_valid = pi.data_length_validation(cars_dict, valid_len_data)

    if (is_valid):
      # If valid create cars dataframe to return
      for key in cars_dict:
        pi.add_column_df(cars, cars_dict[key], key)

      # Add dealership info
      cars['dealership_name'] = dealership_info['dealership_name']
      cars['dealership_address'] = dealership_info['address']
      cars['dealership_zipcode'] = dealership_info['zipcode']
      cars['dealership_city'] = dealership_info['city']
      cars['dealership_state'] = dealership_info['state']
      cars['inventory_url'] = dealership_info['url']
      cars['scraped_date'] = datetime.now(tz = None)

      # Additional changes to data
      cars['title'] = cars['year'] + ' ' + cars['title']

      return cars
    else:
      error_df = pd.DataFrame()
      error_df.at[0, 'error'] = 'Data Validation'
      error_df.at[0, 'dealership'] = dealership_info['dealership_name']
      error_df.at[0, 'date'] = datetime.now(tz = None)
      error_df.at[0, 'url'] = url
      return error_df

def get_blasius_inventory_data(soup, dealership_info, url):
    # Initialize empty data frame & dictionary
    cars = pd.DataFrame()
    cars_dict = {}

    # Add title
    title = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'div', 'vehicle', 'v-title', 'get_text'))
    valid_len_data = len(title)

    # Parse year, make, model_trim, vehicle_type, model, trim
    years = pi.get_valid_year(title)
    makes, model_trim, vehicle_type = pi.get_car_make_model_type(title)
    models = pi.parse_subsection_attr_all(soup, 'content', 'div', 'meta'
                          , main_section_class = 'vehicle-info'
                          , sub_section_attr_parse_key = 'itemprop'
                          , sub_section_attr_parse_value = 'model')
    # Not easily prasable for this dealership - set to None
    trim = [None] * valid_len_data

    # Add mileage col
    miles = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'span', 'vehicle', 'spec-value spec-value-miles'))

    # Add price
    car_prices = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'span', 'vehicle', 'starting-price-value'))

    # Misc car information
    exterior_color = pi.parse_subsection(soup, 'div', 'span', 'v-spec hidden-grid', 'spec-value spec-value-exteriorcolor')
    interior_color = pi.parse_subsection(soup, 'div', 'span', 'v-spec hidden-grid', 'spec-value spec-value-interiorcolor')
    transmission = pi.parse_subsection(soup, 'div', 'span', 'v-spec hidden-grid', 'spec-value spec-value-transmission')
    engine = pi.parse_subsection(soup, 'div', 'span', 'v-spec hidden-grid', 'spec-value spec-value-enginedescription')
    drivetrain = pi.parse_subsection(soup, 'div', 'span', 'v-spec hidden-grid', 'spec-value spec-value-drivetrain')
    vin = pi.parse_attr(soup, 'data-cg-vin')[::2]

    # Append all parsed data to cars_list
    cars_dict['title'] = title
    cars_dict['year'] = years
    cars_dict['make'] = makes
    cars_dict['model_trim'] = model_trim
    cars_dict['vehicle_type'] = vehicle_type
    cars_dict['model'] = models
    cars_dict['trim'] = trim
    cars_dict['vehicle_mileage'] = miles
    cars_dict['price'] = car_prices
    cars_dict['exterior_color'] = exterior_color
    cars_dict['interior_color'] = interior_color
    cars_dict['transmission'] = transmission
    cars_dict['engine'] = engine
    cars_dict['drivetrain'] = drivetrain
    cars_dict['vin'] = vin

    # Check if data is valid
    is_valid = pi.data_length_validation(cars_dict, valid_len_data)

    if (is_valid):
      # If valid create cars dataframe to return
      for key in cars_dict:
        pi.add_column_df(cars, cars_dict[key], key)

      # Add dealership info
      cars['dealership_name'] = dealership_info['dealership_name']
      cars['dealership_address'] = dealership_info['address']
      cars['dealership_zipcode'] = dealership_info['zipcode']
      cars['dealership_city'] = dealership_info['city']
      cars['dealership_state'] = dealership_info['state']
      cars['inventory_url'] = dealership_info['url']
      cars['scraped_date'] = datetime.now(tz = None)

      # Additional changes to data
      pi.fix_vehicle_type(cars)
      cars['title'] = cars['year'] + ' ' + cars['title']

      return cars
    else:
      error_df = pd.DataFrame()
      error_df.at[0, 'error'] = 'Data Validation'
      error_df.at[0, 'dealership'] = dealership_info['dealership_name']
      error_df.at[0, 'date'] = datetime.now(tz = None)
      error_df.at[0, 'url'] = url
      return error_df

def get_avon_inventory_data(soup, dealership_info, url):
    # Initialize empty data frame & dictionary
    cars = pd.DataFrame()
    cars_dict = {}

    # Add title
    title = pi.parse_subsection_attr(soup, 'aria-label', 'div', 'a', 'i11r-vehicle')
    valid_len_data = len(title)

    # Parse year, make, model_trim, vehicle_type, model, trim
    years = pi.get_valid_year(title)
    makes, model_trim, vehicle_type = pi.get_car_make_model_type(title)
    # Avon has a separate element containing vehicle type
    vehicle_type = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optBody', 'get_text'), 'Body Type')
    models = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optModel', 'get_text'), 'Model')
    trim = pi.parse_subsection(soup, 'div', 'span', 'i11r-vehicle', 'vehicleTrim')

    # Add mileage col
    miles = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optMileage', 'get_text'))

    # Add price
    car_prices = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'span', 'i11r-vehicle', 'price-2'))

    # Misc car information
    exterior_color = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optColor', 'get_text'), 'Color')
    interior_color = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optInteriorColor', 'get_text'), 'Interior Color')
    transmission = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optTrans2', 'get_text'), 'Trans')
    engine = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optEngine2', 'get_text'), 'Engine')
    drivetrain = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optDrive', 'get_text'), 'Drive')
    vin =  pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optVin', 'get_text'), 'VIN')

    # Append all parsed data to cars_list
    cars_dict['title'] = title
    cars_dict['year'] = years
    cars_dict['make'] = makes
    cars_dict['model_trim'] = model_trim
    cars_dict['vehicle_type'] = vehicle_type
    cars_dict['model'] = models
    cars_dict['trim'] = trim
    cars_dict['vehicle_mileage'] = miles
    cars_dict['price'] = car_prices
    cars_dict['exterior_color'] = exterior_color
    cars_dict['interior_color'] = interior_color
    cars_dict['transmission'] = transmission
    cars_dict['engine'] = engine
    cars_dict['drivetrain'] = drivetrain
    cars_dict['vin'] = vin

    # Check if data is valid
    is_valid = pi.data_length_validation(cars_dict, valid_len_data)

    if (is_valid):
      # If valid create cars dataframe to return
      for key in cars_dict:
        pi.add_column_df(cars, cars_dict[key], key)

      # Add dealership info
      cars['dealership_name'] = dealership_info['dealership_name']
      cars['dealership_address'] = dealership_info['address']
      cars['dealership_zipcode'] = dealership_info['zipcode']
      cars['dealership_city'] = dealership_info['city']
      cars['dealership_state'] = dealership_info['state']
      cars['inventory_url'] = dealership_info['url']
      cars['scraped_date'] = datetime.now(tz = None)

      # Additional changes
      cars['title'] = cars['year'].apply(str) + ' ' + cars['make'] + ' ' + cars['model_trim']

      return cars
    else:
      error_df = pd.DataFrame()
      error_df.at[0, 'error'] = 'Data Validation'
      error_df.at[0, 'dealership'] = dealership_info['dealership_name']
      error_df.at[0, 'date'] = datetime.now(tz = None)
      error_df.at[0, 'url'] = url
      return error_df

def get_johns_auto_inventory_data(soup, dealership_info, url):
    # Initialize empty data frame & dictionary
    cars = pd.DataFrame()
    cars_dict = {}

    # Add title
    title = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'h4', 'row no-gutters invMainCell', 'd-md-none titleWrapPhoneView', 'get_text'))
    valid_len_data = len(title)

    # Parse year, make, model_trim, vehicle_type, model, trim
    years = pi.get_valid_year(title)
    makes, model_trim, vehicle_type = pi.get_car_make_model_type(title)
    # No model data available that is easily parsable
    models = [None] * valid_len_data
    trim = pi.parse_subsection(soup, 'div', 'span', 'row no-gutters invMainCell', 'vehicleTrim', 'get_text')

    # Miles
    miles = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optMileage', 'get_text'))

    # Prices
    car_prices = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'span', 'row no-gutters invMainCell', 'lblPrice'))

    # Misc car information
    exterior_color = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optColor', 'get_text'), 'Color')
    interior_color = [None] * valid_len_data # No interior color available
    transmission = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optTrans', 'get_text'), 'Trans')
    engine = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optEngine', 'get_text'), 'Engine')
    drivetrain = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optDrive', 'get_text'), 'Drive')
    vin = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optVin', 'get_text'), 'VIN')

    # Append all parsed data to cars_list
    cars_dict['title'] = title
    cars_dict['year'] = years
    cars_dict['make'] = makes
    cars_dict['model_trim'] = model_trim
    cars_dict['vehicle_type'] = vehicle_type
    cars_dict['model'] = models
    cars_dict['trim'] = trim
    cars_dict['vehicle_mileage'] = miles
    cars_dict['price'] = car_prices
    cars_dict['exterior_color'] = exterior_color
    cars_dict['interior_color'] = interior_color
    cars_dict['transmission'] = transmission
    cars_dict['engine'] = engine
    cars_dict['drivetrain'] = drivetrain
    cars_dict['vin'] = vin

    # Check if data is valid
    is_valid = pi.data_length_validation(cars_dict, valid_len_data)

    if (is_valid):
      # If valid create cars dataframe to return
      for key in cars_dict:
        pi.add_column_df(cars, cars_dict[key], key)

      # Add dealership info
      cars['dealership_name'] = dealership_info['dealership_name']
      cars['dealership_address'] = dealership_info['address']
      cars['dealership_zipcode'] = dealership_info['zipcode']
      cars['dealership_city'] = dealership_info['city']
      cars['dealership_state'] = dealership_info['state']
      cars['inventory_url'] = dealership_info['url']
      cars['scraped_date'] = datetime.now(tz = None)

      return cars
    else:
      error_df = pd.DataFrame()
      error_df.at[0, 'error'] = 'Data Validation'
      error_df.at[0, 'dealership'] = dealership_info['dealership_name']
      error_df.at[0, 'date'] = datetime.now(tz = None)
      error_df.at[0, 'url'] = url
      return error_df

def get_jm_auto_inventory_data(soup, dealership_info, url):
    # Initialize empty data frame & dictionary
    cars = pd.DataFrame()
    cars_dict = {}

    # Parse title
    title = pi.parse_subsection_attr(soup, 'title','div', 'a', 'thumbnail', 'listitemlink')
    valid_len_data = len(title)

    # Parse year, make, model_trim, vehicle_type, model, trim
    years = pi.convert_to_numeric_type(pi.parse_main_section_attr_text_all(soup, 'div', 'thumbnail', 'itemprop', 'vehicleModelDate'))
    makes = pi.parse_main_section_attr_text_all(soup, 'div', 'thumbnail', 'itemprop', 'manufacturer')
    models = pi.parse_main_section_attr_text_all(soup, 'div', 'thumbnail', 'itemprop', 'model')
    trim = pi.parse_main_section_attr_text_all(soup, 'div', 'thumbnail', 'itemprop', 'vehicleConfiguration')
    model_trim = [None] * valid_len_data
    vehicle_type = [None] * valid_len_data

    # Miles
    miles = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'li', 'thumbnail', 'list-group-item mileage', 'get_text'))

    # Prices
    car_prices = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'div', 'thumbnail', 'pricetag', 'get_text'))

    # Misc car information
    exterior_color = pi.clean_text_data(pi.parse_main_section_attr_text_all(soup, 'div', 'thumbnail', 'itemprop', 'color'))
    interior_color = pi.clean_text_data(pi.parse_main_section_attr_text_all(soup, 'div', 'thumbnail', 'itemprop', 'vehicleInteriorColor'))
    transmission = pi.clean_text_data(pi.parse_main_section_attr_text_all(soup, 'div', 'thumbnail', 'itemprop', 'vehicleTransmission'))
    engine = pi.clean_text_data(pi.parse_main_section_attr_text_all(soup, 'div', 'thumbnail', 'itemprop', 'vehicleEngine'))
    drivetrain = pi.clean_text_data(pi.parse_main_section_attr_text_all(soup, 'div', 'thumbnail', 'itemprop', 'driveWheelConfiguration'))
    vin = pi.clean_text_data(pi.parse_main_section_attr_text_all(soup, 'div', 'thumbnail', 'itemprop', 'vehicleIdentificationNumber'))

    # Append all parsed data to cars_list
    cars_dict['title'] = title
    cars_dict['year'] = years
    cars_dict['make'] = makes
    cars_dict['model_trim'] = model_trim
    cars_dict['vehicle_type'] = vehicle_type
    cars_dict['model'] = models
    cars_dict['trim'] = trim
    cars_dict['vehicle_mileage'] = miles
    cars_dict['price'] = car_prices
    cars_dict['exterior_color'] = exterior_color
    cars_dict['interior_color'] = interior_color
    cars_dict['transmission'] = transmission
    cars_dict['engine'] = engine
    cars_dict['drivetrain'] = drivetrain
    cars_dict['vin'] = vin

    # Check if data is valid
    is_valid = pi.data_length_validation(cars_dict, valid_len_data)

    if (is_valid):
      # If valid create cars dataframe to return
      for key in cars_dict:
        pi.add_column_df(cars, cars_dict[key], key)

      # Add dealership info
      cars['dealership_name'] = dealership_info['dealership_name']
      cars['dealership_address'] = dealership_info['address']
      cars['dealership_zipcode'] = dealership_info['zipcode']
      cars['dealership_city'] = dealership_info['city']
      cars['dealership_state'] = dealership_info['state']
      cars['inventory_url'] = dealership_info['url']
      cars['scraped_date'] = datetime.now(tz = None)

      # Make other changes
      cars['model_trim'] = cars['model'] + ' ' + cars['trim']
      cars['title'] = cars['year'].apply(str) + ' ' + cars['make'] + ' ' + cars['model_trim']

      return cars
    else:
      error_df = pd.DataFrame()
      error_df.at[0, 'error'] = 'Data Validation'
      error_df.at[0, 'dealership'] = dealership_info['dealership_name']
      error_df.at[0, 'date'] = datetime.now(tz = None)
      error_df.at[0, 'url'] = url
      return error_df

def get_ct_auto_inventory_data(soup, dealership_info, url):
    # Initialize empty data frame & dictionary
    cars = pd.DataFrame()
    cars_dict = {}

    # Parse title
    # For this dealership - we need to make the change later

    # Parse year, make, model_trim, vehicle_type, model, trim
    years = pi.convert_to_numeric_type(pi.parse_main_section_attr_text_all(soup, 'div', 'invItems item col-xs-6 col-lg-6 list-group-item'
                                    , 'itemprop', 'vehicleModelDate'))
    makes = pi.parse_main_section_attr_text_all(soup, 'div', 'invItems item col-xs-6 col-lg-6 list-group-item'
                                    , 'itemprop', 'manufacturer')
    valid_len_data = len(makes)
    models = pi.parse_main_section_attr_text_all(soup, 'div', 'invItems item col-xs-6 col-lg-6 list-group-item'
                                    , 'itemprop', 'model')
    trim = pi.parse_main_section_attr_text_all(soup, 'div', 'invItems item col-xs-6 col-lg-6 list-group-item'
                                    , 'itemprop', 'vehicleConfiguration')
    title = [None] * valid_len_data
    model_trim = [None] * valid_len_data
    vehicle_type = [None] * valid_len_data

    # Miles
    miles = pi.convert_to_numeric_type(
              pi.parse_subsection(soup, 'div', 'li', 'invItems item col-xs-6 col-lg-6 list-group-item'
                    , 'list-group-item mileage', 'get_text'))

    # Prices
    car_prices = pi.convert_to_numeric_type(
                    pi.parse_main_section_attr_text_all(soup, 'div', 'invItems item col-xs-6 col-lg-6 list-group-item'
                                    , 'itemprop', 'price'))

    # Misc car information
    exterior_color = pi.clean_text_data(
                        pi.parse_subsection(soup, 'div', 'li', 'invItems item col-xs-6 col-lg-6 list-group-item'
                        , 'list-group-item InvExteriorcolor', 'get_text'), 'Exterior')
    interior_color = [None] * valid_len_data
    transmission = pi.clean_text_data(
                        pi.parse_subsection(soup, 'div', 'li', 'invItems item col-xs-6 col-lg-6 list-group-item'
                        , 'list-group-item InvTransmissiontype', 'get_text'), 'Transmission')
    engine = pi.clean_text_data(
                        pi.parse_subsection(soup, 'div', 'li', 'invItems item col-xs-6 col-lg-6 list-group-item'
                        , 'list-group-item InvEnginetype', 'get_text'), 'Engine')
    drivetrain = pi.parse_main_section_attr_text_all(soup, 'div', 'invItems item col-xs-6 col-lg-6 list-group-item'
                                , 'itemprop', 'driveWheelConfiguration')
    vin = pi.clean_text_data(
            pi.parse_subsection(soup, 'div', 'li', 'invItems item col-xs-6 col-lg-6 list-group-item', 'list-group-item InvVin', 'get_text'), 'VIN')

    # Append all parsed data to cars_list
    cars_dict['title'] = title
    cars_dict['year'] = years
    cars_dict['make'] = makes
    cars_dict['model_trim'] = model_trim
    cars_dict['vehicle_type'] = vehicle_type
    cars_dict['model'] = models
    cars_dict['trim'] = trim
    cars_dict['vehicle_mileage'] = miles
    cars_dict['price'] = car_prices
    cars_dict['exterior_color'] = exterior_color
    cars_dict['interior_color'] = interior_color
    cars_dict['transmission'] = transmission
    cars_dict['engine'] = engine
    cars_dict['drivetrain'] = drivetrain
    cars_dict['vin'] = vin

    # Check if data is valid
    is_valid = pi.data_length_validation(cars_dict, valid_len_data)

    if (is_valid):
      # If valid create cars dataframe to return
      for key in cars_dict:
        pi.add_column_df(cars, cars_dict[key], key)

      # Add dealership info
      cars['dealership_name'] = dealership_info['dealership_name']
      cars['dealership_address'] = dealership_info['address']
      cars['dealership_zipcode'] = dealership_info['zipcode']
      cars['dealership_city'] = dealership_info['city']
      cars['dealership_state'] = dealership_info['state']
      cars['inventory_url'] = dealership_info['url']
      cars['scraped_date'] = datetime.now(tz = None)

      # Make other changes
      cars['model_trim'] = cars['model'] + ' ' + cars['trim']
      cars['title'] = cars['year'].apply(str) + ' ' + cars['make'] + ' ' + cars['model_trim']

      return cars
    else:
      error_df = pd.DataFrame()
      error_df.at[0, 'error'] = 'Data Validation'
      error_df.at[0, 'dealership'] = dealership_info['dealership_name']
      error_df.at[0, 'date'] = datetime.now(tz = None)
      error_df.at[0, 'url'] = url
      return error_df

def get_irwin_auto_inventory_data(soup, dealership_info, url):
    # Initialize empty data frame & dictionary
    cars = pd.DataFrame()
    cars_dict = {}

    # Parse title
    # For this dealership - we need to make the change later

    # Parse year, make, model_trim, vehicle_type, model, trim
    title = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-name')
    valid_len_data = len(title)

    years = pi.convert_to_numeric_type(pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-year'))
    makes = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-make')
    models = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-model')
    trim = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-trim')

    model_trim = [None] * valid_len_data
    vehicle_type = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-bodystyle')

    # Miles
    miles = pi.convert_to_numeric_type(
      pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-mileage')
    )

    # Prices
    car_prices = [int(float(i)) for i in pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-price')]

    # Misc car information
    exterior_color = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-extcolor')
    interior_color = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-intcolor')
    transmission = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-trans')
    engine = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-engine')
    drivetrain = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-drivetrain')
    vin = pi.parse_class_attr(soup, 'div', 'row srpVehicle hasVehicleInfo', 'data-vin')

    # Append all parsed data to cars_list
    cars_dict['title'] = title
    cars_dict['year'] = years
    cars_dict['make'] = makes
    cars_dict['model_trim'] = model_trim
    cars_dict['vehicle_type'] = vehicle_type
    cars_dict['model'] = models
    cars_dict['trim'] = trim
    cars_dict['vehicle_mileage'] = miles
    cars_dict['price'] = car_prices
    cars_dict['exterior_color'] = exterior_color
    cars_dict['interior_color'] = interior_color
    cars_dict['transmission'] = transmission
    cars_dict['engine'] = engine
    cars_dict['drivetrain'] = drivetrain
    cars_dict['vin'] = vin

    # Check if data is valid
    is_valid = pi.data_length_validation(cars_dict, valid_len_data)

    if (is_valid):
      # If valid create cars dataframe to return
      for key in cars_dict:
        pi.add_column_df(cars, cars_dict[key], key)

      # Add dealership info
      cars['dealership_name'] = dealership_info['dealership_name']
      cars['dealership_address'] = dealership_info['address']
      cars['dealership_zipcode'] = dealership_info['zipcode']
      cars['dealership_city'] = dealership_info['city']
      cars['dealership_state'] = dealership_info['state']
      cars['inventory_url'] = dealership_info['url']
      cars['scraped_date'] = datetime.now(tz = None)

      # Make other changes
      cars['model_trim'] = cars['model'] + ' ' + cars['trim']

      return cars
    else:
      error_df = pd.DataFrame()
      error_df.at[0, 'error'] = 'Data Validation'
      error_df.at[0, 'dealership'] = dealership_info['dealership_name']
      error_df.at[0, 'date'] = datetime.now(tz = None)
      error_df.at[0, 'url'] = url
      return error_df

def get_stream_auto_outlet_inventory_data(soup, dealership_info, url):
  # Initialize empty data frame & dictionary
  cars = pd.DataFrame()
  cars_dict = {}

  # Parse title
  # Parse year, make, model_trim, vehicle_type, model, trim
  title = pi.clean_text_data(pi.parse_subsection_all(soup, 'h4', 'span', 'srp-vehicle-title'))
  valid_len_data = len(title)

  years = pi.get_valid_year(title)
  makes, model_trim, vehicle_type = pi.get_car_make_model_type(title)
  trim = [None] * valid_len_data
  models = [None] * valid_len_data

  # Prices
  car_prices =  pi.convert_to_numeric_type(
    pi.parse_subsection(soup, 'div', 'span', 'columns medium-8', 'price-value right', 'get_text')
  )

  # Misc car information
  results = pi.get_row_subsection_data(soup, ('div', 'medium-8 medium-pull-4 columns'), ('div', 'srp-vehicle-data'))
  vehicle_data = []
  for section in results:
      sub_data = []
      for el in section:
          el_data = [x.get_text() for x in el.findAll('div', 'column')]
          sub_data += el_data
      vehicle_data.append(sub_data)

  vehicle_misc_info = {
    'exterior_color': [],
    'interior_color': [],
    'transmission': [],
    'engine': [],
    'drivetrain': [],
    'vin': [],
    'mileage': []
  }


  for i in range(len(vehicle_data)):
    row = {}
    for col in vehicle_data[i]:
      if 'Ext. Color' in col:
        cleaned_str = col.replace('Ext. Color: ', '')
        row['exterior_color'] = cleaned_str
      elif 'Int. Color' in col:
        cleaned_str = col.replace('Int. Color: ', '')
        row['interior_color'] = cleaned_str
      elif 'Transmission' in col:
        cleaned_str = col.replace('Transmission: ', '')
        row['transmission'] = cleaned_str
      elif 'Mileage' in col:
        cleaned_str = col.replace('Mileage: ', '').replace(',', '')
        row['mileage'] = cleaned_str
      elif 'Drivetrain' in col:
        cleaned_str = col.replace('Drivetrain: ', '')
        row['drivetrain'] = cleaned_str
      elif 'Engine' in col:
        cleaned_str = col.replace('Engine: ', '')
        row['engine'] = cleaned_str
      elif 'VIN' in col:
        cleaned_str = col.split(' ')[1].strip()
        row['vin'] = cleaned_str
    for key in ['exterior_color', 'interior_color', 'drivetrain', 'transmission', 'mileage', 'engine', 'vin']:
      if key in row:
          vehicle_misc_info[key].append(row[key])
      else:
          vehicle_misc_info[key].append(None)



  # Append all parsed data to cars_list
  cars_dict['title'] = title
  cars_dict['year'] = years
  cars_dict['make'] = makes
  cars_dict['model_trim'] = model_trim
  cars_dict['vehicle_type'] = vehicle_type
  cars_dict['model'] = models
  cars_dict['trim'] = trim
  cars_dict['vehicle_mileage'] = vehicle_misc_info['mileage']
  cars_dict['price'] = car_prices
  cars_dict['exterior_color'] = vehicle_misc_info['exterior_color']
  cars_dict['interior_color'] = vehicle_misc_info['interior_color']
  cars_dict['transmission'] = vehicle_misc_info['transmission']
  cars_dict['engine'] = vehicle_misc_info['engine']
  cars_dict['drivetrain'] =vehicle_misc_info['drivetrain']
  cars_dict['vin'] = vehicle_misc_info['vin']

  # Check if data is valid
  is_valid = pi.data_length_validation(cars_dict, valid_len_data)

  if (is_valid):
    # If valid create cars dataframe to return
    for key in cars_dict:
      pi.add_column_df(cars, cars_dict[key], key)

    # Add dealership info
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)

    return cars
  else:
    error_df = pd.DataFrame()
    error_df.at[0, 'error'] = 'Data Validation'
    error_df.at[0, 'dealership'] = dealership_info['dealership_name']
    error_df.at[0, 'date'] = datetime.now(tz = None)
    error_df.at[0, 'url'] = url
    return error_df
