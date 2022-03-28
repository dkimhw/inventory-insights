def data_length_validation(dict, valid_len):
  for key in dict:
    curr_key_len = len(dict[key])
    if (curr_key_len != valid_len):
      return False
  
  return True  



def get_jm_auto_inventory_data_test(soup, dealership_info, url):
    # Initialize empty data frame
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

    # Append all data to cars_list
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

    is_valid = pi.data_length_validation(cars_dict, valid_len_data)

    if (is_valid):
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
    
