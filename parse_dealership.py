
import parse_inventory as pi
import pandas as pd
from datetime import datetime

# Functions to parse specific dealership web data
def get_direct_auto_inventory_data(soup, dealership_info):    
    # Initialize empty data frame
    cars = pd.DataFrame()
    
    # Add title
    title = pi.parseColumn(soup, 'h2', 'ebiz-vdp-title color m-0')    
    pi.add_column_df(cars, title, 'title')

    # Add vehicle manufacture date
    years = pi.get_valid_year(title)
    pi.add_column_df(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = pi.get_car_make_model_type(title)
    pi.add_column_df(cars, makes, 'make')
    pi.add_column_df(cars, models, 'model_trim')
    pi.add_column_df(cars, vtypes, 'vehicle_type')

    # Model & Trim
    # Not easily prasable for this dealership - set to None
    cars['model'] = None
    cars['trim'] = None

    # Add mileage col
    miles = pi.get_numeric_vehicle_data(soup, 'li', 'mileage-units')
    pi.add_column_df(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = pi.get_numeric_vehicle_data(soup, 'div', 'price-item')
    pi.add_column_df(cars, car_prices, 'price')

    # Add Colors & transmission & other cols
    pi.add_column_df(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'exterior'), 'exterior_color')
    pi.add_column_df(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'interior'), 'interior_color')
    pi.add_column_df(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'transmission'), 'transmission')
    pi.add_column_df(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'engine'), 'engine')
    cars['drivetrain'] = None
    pi.add_column_df(cars, pi.parseColumn(soup, 'li', 'vin'), 'vin')
    cars['vin'] = cars['vin'].str.replace('VIN #: ', '')
    
    # Add dealership info + scrape date
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)
    
    return cars


def get_bostonyan_inventory_data(soup, dealership_info):
    # Scrape inventory HTML
    # response = requests.get(dealership_info['url'], headers = headers)
    # soup = BeautifulSoup(response.text, "html.parser")

    # Initialize empty data frame
    cars = pd.DataFrame()

    # Add vehicle title
    title = pi.parseColumn(soup, 'a', 'accent-color1')
    pi.add_column_df(cars, title, 'title')

    # Add vehicle manufacture date
    years = pi.get_valid_year(title)
    pi.add_column_df(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = pi.get_car_make_model_type(title)
    pi.add_column_df(cars, makes, 'make')
    pi.add_column_df(cars, models, 'model_trim')
    pi.add_column_df(cars, vtypes, 'vehicle_type')

    # Model & Trim
    # Not easily prasable for this dealership - set to None
    cars['model'] = None
    cars['trim'] = None

    # Add mileage col
    miles = pi.get_numeric_vehicle_data(soup, 'span', 'mileage')
    pi.add_column_df(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = pi.get_numeric_vehicle_data(soup, 'div', 'pricevalue1 accent-color1')
    pi.add_column_df(cars, car_prices, 'price')

    # Add Colors & transmission & other cols
    pi.add_column_df(cars, pi.parseColumn(soup,'span', 'Extcolor'), 'exterior_color')
    pi.add_column_df(cars, pi.parseColumn(soup,'span', 'Intcolor'), 'interior_color')
    pi.add_column_df(cars, pi.parseColumn(soup,'div', 'transmission'), 'transmission')
    pi.add_column_df(cars, pi.parseColumn(soup,'div', 'engine'), 'engine')
    cars['drivetrain'] = None    
    pi.add_column_df(cars, pi.parseColumn(soup,'span', 'vin'), 'vin')

    # Add dealership info + scrape date
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)

    return cars

def get_fafama_inventory_data(soup, dealership_info):
    # Initialize empty data frame
    cars = pd.DataFrame()
    
    # Add title
    title = pi.parseColumn(soup, 'h2', 'color m-0 ebiz-vdp-title')    
    pi.add_column_df(cars, title, 'title')

    # Add vehicle manufacture date
    years = pi.get_valid_year(title)
    pi.add_column_df(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = pi.get_car_make_model_type(title)
    pi.add_column_df(cars, makes, 'make')
    pi.add_column_df(cars, models, 'model_trim')
    pi.add_column_df(cars, vtypes, 'vehicle_type')
    pi.fix_vehicle_type(cars)

    # Model & Trim
    # Not easily prasable for this dealership - set to None
    cars['model'] = None
    cars['trim'] = None

    # Add mileage col
    miles = pi.get_numeric_vehicle_data(soup, 'li', 'mileage-units')
    pi.add_column_df(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = pi.get_numeric_vehicle_data(soup, 'div', 'price-item active mt-3 mt-md-0')
    pi.add_column_df(cars, car_prices, 'price')

    # Add Colors & transmission & other cols
    pi.add_column_df(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'exterior'), 'exterior_color')
    pi.add_column_df(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'interior'), 'interior_color')
    pi.add_column_df(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'transmission'), 'transmission')
    pi.add_column_df(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'engine'), 'engine')
    cars['drivetrain'] = None    
    pi.add_column_df(cars, pi.parseColumn(soup, 'li', 'vin'), 'vin')
    cars['vin'] = cars['vin'].str.replace('VIN #: ', '')
    
    # Add dealership info + scrape date
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)
    
    return cars

def get_newton_auto_inventory_data(soup, dealership_info):
    # Initialize empty data frame
    cars = pd.DataFrame()

    # Add title
    title = pi.parseColumn(soup, 'h3', 'vehicle-snapshot__title')
    pi.add_column_df(cars, title, 'title')        

    # Add vehicle manufacture date
    years = pi.get_valid_year(title)   
    pi.add_column_df(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = pi.get_car_make_model_type(title)
    pi.add_column_df(cars, makes, 'make')
    pi.add_column_df(cars, models, 'model_trim')
    pi.add_column_df(cars, vtypes, 'vehicle_type')

    # Model & Trim
    # Not easily prasable for this dealership - set to None
    cars['model'] = None
    cars['trim'] = None

    # Parse numeric data (price; mileage - has same class name)
    miles_and_price = pi.get_numeric_vehicle_data(soup, 'div', 'vehicle-snapshot__main-info font-primary')
    car_prices = [el for idx, el in enumerate(miles_and_price) if idx % 2 == 0]
    miles = [el for idx, el in enumerate(miles_and_price) if idx % 2 != 0]
    pi.add_column_df(cars, miles, 'vehicle_mileage')
    pi.add_column_df(cars, car_prices, 'price')

    # Add Colors & transmission & other cols
    vehicle_info = pi.parseColumn(soup, 'div', 'vehicle-snapshot__info-text-container')

    # Colors 
    exterior = vehicle_info[1::6]
    exterior = [el.replace('Exterior Color', '').strip() for el in exterior]   
    pi.add_column_df(cars, exterior, 'exterior_color')  
    interior = vehicle_info[3::6]
    interior = [el.replace('Interior Color', '').strip() for el in interior]
    pi.add_column_df(cars, interior, 'interior_color')  

    # Transmission
    transmission = vehicle_info[2::6]
    transmission = [el.replace('Transmission', '').strip() for el in transmission]
    pi.add_column_df(cars, transmission, 'transmission')  

    # Engine
    engine = vehicle_info[::6]
    engine = [el.replace('Engine', '').strip() for el in engine]
    pi.add_column_df(cars, engine, 'engine')  

    # Drive Train
    drivetrain = vehicle_info[4::6]
    drivetrain = [el.replace('Drivetrain', '').strip() for el in drivetrain]    
    pi.add_column_df(cars, drivetrain, 'drivetrain')   

    # No VIN that can be scraped
    cars['vin'] = None
    
    # Add dealership info + scrape date
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)
    
    return cars

def get_blasius_inventory_data(soup, dealership_info):
    # Initialize empty data frame
    cars = pd.DataFrame()

    # Add title
    title = pi.parseColumn(soup, 'div', 'v-title')
    pi.add_column_df(cars, title, 'title')        
    
    # Add vehicle manufacture date
    years = pi.get_valid_year(title)   
    pi.add_column_df(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = pi.get_car_make_model_type(title)
    pi.add_column_df(cars, makes, 'make')
    pi.add_column_df(cars, models, 'model_trim')
    pi.add_column_df(cars, vtypes, 'vehicle_type')
    pi.fix_vehicle_type(cars)

    # Model & Trim
    cars['model'] = pi.parse_subsection_attr_all(soup, 'content', 'div', 'meta'
                          , main_section_class = 'vehicle-info'
                          , sub_section_attr_parse_key = 'itemprop'
                          , sub_section_attr_parse_value = 'model')
    # Not easily prasable for this dealership - set to None
    cars['trim'] = None

    # Add mileage col
    miles = pi.get_numeric_vehicle_data(soup, 'span', 'spec-value spec-value-miles')[::2]
    pi.add_column_df(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = pi.get_numeric_vehicle_data(soup, 'div', 'mod-vehicle-price mod-vehicle-price-responsive1 mod-vehicle-price-listing')[::2]
    pi.add_column_df(cars, car_prices, 'price')    

    # Add Colors & transmission & other cols
    pi.add_column_df(cars, pi.parse_subsection(soup, 'div', 'span', 'v-spec hidden-grid', 'spec-value spec-value-exteriorcolor'), 'exterior_color')
    pi.add_column_df(cars, pi.parse_subsection(soup, 'div', 'span', 'v-spec hidden-grid', 'spec-value spec-value-interiorcolor'), 'interior_color')
    pi.add_column_df(cars, pi.parse_subsection(soup, 'div', 'span', 'v-spec hidden-grid', 'spec-value spec-value-transmission'), 'transmission')
    pi.add_column_df(cars, pi.parse_subsection(soup, 'div', 'span', 'v-spec hidden-grid', 'spec-value spec-value-enginedescription'), 'engine')
    pi.add_column_df(cars, pi.parse_subsection(soup, 'div', 'span', 'v-spec hidden-grid', 'spec-value spec-value-drivetrain'), 'drivetrain')
    pi.add_column_df(cars, pi.parse_attr(soup, 'data-cg-vin')[::2], 'vin')

    # Add dealership info + scrape date
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)

    return cars    

def get_avon_inventory_data(soup, dealership_info):
    # Initialize empty data frame
    cars = pd.DataFrame()

    # Add title
    title = pi.parse_subsection_attr(soup, 'aria-label', 'div', 'a', 'i11r-vehicle')
    pi.add_column_df(cars, title, 'title') 

    # Add vehicle manufacture date
    years = pi.get_valid_year(title)   
    pi.add_column_df(cars, years, 'year')

    # Add year, make, model, trim 
    makes, models, vtypes = pi.get_car_make_model_type(title)
    pi.add_column_df(cars, makes, 'make')
    pi.add_column_df(cars, models, 'model_trim')

    # Avon has a separate element containing vehicle type
    vtypes = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optBody', 'get_text'), 'Body Type')
    pi.add_column_df(cars, vtypes, 'vehicle_type')

    # Model & Trim
    # Trim is not paraseable easily (there is no section for it) for all dealerships
    # Same for Model - but when it's easily parsable - we should add it here
    model = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optModel', 'get_text'), 'Model')
    pi.add_column_df(cars, model, 'model')
    trim = pi.parse_subsection(soup, 'div', 'span', 'i11r-vehicle', 'vehicleTrim')
    pi.add_column_df(cars, trim, 'trim')

    # Add mileage col
    miles = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optMileage', 'get_text'))
    pi.add_column_df(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'span', 'i11r-vehicle', 'price-2'))
    pi.add_column_df(cars, car_prices, 'price')        

    # Add Colors & transmission & other cols
    pi.add_column_df(cars, pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optColor', 'get_text'), 'Color'), 'exterior_color')
    pi.add_column_df(cars, pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optInteriorColor', 'get_text'), 'Interior Color'), 'interior_color')
    pi.add_column_df(cars, pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optTrans2', 'get_text'), 'Trans'), 'transmission')
    pi.add_column_df(cars, pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optEngine2', 'get_text'), 'Engine'), 'engine')
    pi.add_column_df(cars, pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optDrive', 'get_text'), 'Drive'), 'drivetrain')
    pi.add_column_df(cars, pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'i11r-vehicle', 'i11r_optVin', 'get_text'), 'VIN'), 'vin')

    # Add dealership info + scrape date
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)

    return cars

def get_johns_auto_inventory_data(soup, dealership_info):
    # Initialize empty data frame
    cars = pd.DataFrame()

    # Add title
    title = pi.clean_text_data(pi.parse_subsection(soup, 'div', 'h4', 'row no-gutters invMainCell', 'd-md-none titleWrapPhoneView', 'get_text'))
    pi.add_column_df(cars, title, 'title') 

    # Add vehicle manufacture date
    years = pi.get_valid_year(title)   
    pi.add_column_df(cars, years, 'year')

    # Add year, make, model, trim 
    makes, models, vtypes = pi.get_car_make_model_type(title)
    pi.add_column_df(cars, makes, 'make')
    pi.add_column_df(cars, models, 'model_trim')
    pi.add_column_df(cars, vtypes, 'vehicle_type')

    # Model & Trim
    # No model data available that is easily parsable
    cars['model'] = None
    trim = pi.parse_subsection(soup, 'div', 'span', 'row no-gutters invMainCell', 'vehicleTrim', 'get_text')
    pi.add_column_df(cars, trim, 'trim')

    # Add mileage col
    miles = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optMileage', 'get_text'))
    pi.add_column_df(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = pi.convert_to_numeric_type(pi.parse_subsection(soup, 'div', 'span', 'row no-gutters invMainCell', 'lblPrice'))
    pi.add_column_df(cars, car_prices, 'price')      

    # Add Colors & transmission & other cols
    # No interior color available
    pi.add_column_df(cars, pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optColor', 'get_text'), 'Color'), 'exterior_color')
    cars['interior_color'] = None
    pi.add_column_df(cars, pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optTrans', 'get_text'), 'Trans'), 'transmission')
    pi.add_column_df(cars, pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optEngine', 'get_text'), 'Engine'), 'engine')
    pi.add_column_df(cars, pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optDrive', 'get_text'), 'Drive'), 'drivetrain')
    pi.add_column_df(cars, pi.clean_text_data(pi.parse_subsection(soup, 'div', 'p', 'row no-gutters invMainCell', 'optVin', 'get_text'), 'VIN'), 'vin')

    # Add dealership info + scrape date
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)

    return cars