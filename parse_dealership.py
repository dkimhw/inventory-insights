
import parse_inventory as pi
import pandas as pd
from datetime import datetime

# Functions to parse specific dealership web data
def get_direct_auto_inventory_data(soup, dealership_info):    
    # Initialize empty data frame
    cars = pd.DataFrame()
    
    # Add title
    title = pi.parseColumn(soup, 'h2', 'ebiz-vdp-title color m-0')    
    pi.addColumnDF(cars, title, 'title')

    # Add vehicle manufacture date
    years = pi.get_valid_year(soup, 'h2', 'ebiz-vdp-title color m-0')
    pi.addColumnDF(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = pi.get_car_make_model_type(soup, 'h2', 'ebiz-vdp-title color m-0')
    pi.addColumnDF(cars, makes, 'make')
    pi.addColumnDF(cars, models, 'models')
    pi.addColumnDF(cars, vtypes, 'vehicle_type')

    # Add mileage col
    miles = pi.get_numeric_vehicle_data(soup, 'li', 'mileage-units')
    pi.addColumnDF(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = pi.get_numeric_vehicle_data(soup, 'div', 'price-item')
    pi.addColumnDF(cars, car_prices, 'price')

    # Add Colors & transmission & other cols
    pi.addColumnDF(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'exterior'), 'exterior_color')
    pi.addColumnDF(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'interior'), 'interior_color')
    pi.addColumnDF(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'transmission'), 'transmission')
    pi.addColumnDF(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'engine'), 'engine')
    cars['drivetrain'] = None
    pi.addColumnDF(cars, pi.parseColumn(soup, 'li', 'vin'), 'vin')
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
    pi.addColumnDF(cars, title, 'title')

    # Add vehicle manufacture date
    years = pi.get_valid_year(soup, 'a', 'accent-color1')
    pi.addColumnDF(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = pi.get_car_make_model_type(soup, 'a', 'accent-color1')
    pi.addColumnDF(cars, makes, 'make')
    pi.addColumnDF(cars, models, 'models')
    pi.addColumnDF(cars, vtypes, 'vehicle_type')

    # Add mileage col
    miles = pi.get_numeric_vehicle_data(soup, 'span', 'mileage')
    pi.addColumnDF(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = pi.get_numeric_vehicle_data(soup, 'div', 'pricevalue1 accent-color1')
    pi.addColumnDF(cars, car_prices, 'price')

    # Add Colors & transmission & other cols
    pi.addColumnDF(cars, pi.parseColumn(soup,'span', 'Extcolor'), 'exterior_color')
    pi.addColumnDF(cars, pi.parseColumn(soup,'span', 'Intcolor'), 'interior_color')
    pi.addColumnDF(cars, pi.parseColumn(soup,'div', 'transmission'), 'transmission')
    pi.addColumnDF(cars, pi.parseColumn(soup,'div', 'engine'), 'engine')
    cars['drivetrain'] = None    
    pi.addColumnDF(cars, pi.parseColumn(soup,'span', 'vin'), 'vin')

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
    pi.addColumnDF(cars, title, 'title')

    # Add vehicle manufacture date
    years = pi.get_valid_year(soup, 'h2', 'color m-0 ebiz-vdp-title')
    pi.addColumnDF(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = pi.get_car_make_model_type(soup, 'h2', 'color m-0 ebiz-vdp-title')
    pi.addColumnDF(cars, makes, 'make')
    pi.addColumnDF(cars, models, 'models')
    pi.addColumnDF(cars, vtypes, 'vehicle_type')
    
    # Clean up vehicle type
    pi.fix_vehicle_type(cars)

    # Add mileage col
    miles = pi.get_numeric_vehicle_data(soup, 'li', 'mileage-units')
    pi.addColumnDF(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = pi.get_numeric_vehicle_data(soup, 'div', 'price-item active mt-3 mt-md-0')
    pi.addColumnDF(cars, car_prices, 'price')

    # Add Colors & transmission & other cols
    pi.addColumnDF(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'exterior'), 'exterior_color')
    pi.addColumnDF(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'interior'), 'interior_color')
    pi.addColumnDF(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'transmission'), 'transmission')
    pi.addColumnDF(cars, pi.get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'engine'), 'engine')
    cars['drivetrain'] = None    
    pi.addColumnDF(cars, pi.parseColumn(soup, 'li', 'vin'), 'vin')
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
    pi.addColumnDF(cars, title, 'title')        

    # Add vehicle manufacture date
    years = pi.get_valid_year(soup, 'h3', 'vehicle-snapshot__title')   
    pi.addColumnDF(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = pi.get_car_make_model_type(soup, 'h3', 'vehicle-snapshot__title')
    pi.addColumnDF(cars, makes, 'make')
    pi.addColumnDF(cars, models, 'models')
    pi.addColumnDF(cars, vtypes, 'vehicle_type')

    # Parse numeric data (price; mileage - has same class name)
    miles_and_price = pi.get_numeric_vehicle_data(soup, 'div', 'vehicle-snapshot__main-info font-primary')
    car_prices = [el for idx, el in enumerate(miles_and_price) if idx % 2 == 0]
    miles = [el for idx, el in enumerate(miles_and_price) if idx % 2 != 0]
    pi.addColumnDF(cars, miles, 'vehicle_mileage')
    pi.addColumnDF(cars, car_prices, 'price')

    # Add Colors & transmission & other cols
    vehicle_info = pi.parseColumn(soup, 'div', 'vehicle-snapshot__info-text-container')

    # Colors 
    exterior = vehicle_info[1::6]
    exterior = [el.replace('Exterior Color', '').strip() for el in exterior]   
    pi.addColumnDF(cars, exterior, 'exterior_color')  
    interior = vehicle_info[3::6]
    interior = [el.replace('Interior Color', '').strip() for el in interior]
    pi.addColumnDF(cars, interior, 'interior_color')  

    # Transmission
    transmission = vehicle_info[2::6]
    transmission = [el.replace('Transmission', '').strip() for el in transmission]
    pi.addColumnDF(cars, transmission, 'transmission')  

    # Engine
    engine = vehicle_info[::6]
    engine = [el.replace('Engine', '').strip() for el in engine]
    pi.addColumnDF(cars, engine, 'engine')  

    # Drive Train
    drivetrain = vehicle_info[4::6]
    drivetrain = [el.replace('Drivetrain', '').strip() for el in drivetrain]    
    pi.addColumnDF(cars, drivetrain, 'drivetrain')   

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
    pi.addColumnDF(cars, title, 'title')        
    
    # Add vehicle manufacture date
    years = pi.get_valid_year(soup, 'div', 'v-title')   
    pi.addColumnDF(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = pi.get_car_make_model_type(soup, 'div', 'v-title')
    pi.addColumnDF(cars, makes, 'make')
    pi.addColumnDF(cars, models, 'models')
    pi.addColumnDF(cars, vtypes, 'vehicle_type')

    # Clean up vehicle type
    pi.fix_vehicle_type(cars)

    # Add mileage col
    miles = pi.get_numeric_vehicle_data(soup, 'span', 'spec-value spec-value-miles')[::2]
    pi.addColumnDF(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = pi.get_numeric_vehicle_data(soup, 'div', 'mod-vehicle-price mod-vehicle-price-responsive1 mod-vehicle-price-listing')[::2]
    pi.addColumnDF(cars, car_prices, 'price')    

    # Add Colors & transmission & other cols
    pi.addColumnDF(cars, pi.parse_subsection(soup, 'div', 'v-spec hidden-grid', 'span', 'spec-value spec-value-exteriorcolor'), 'exterior_color')
    pi.addColumnDF(cars, pi.parse_subsection(soup, 'div', 'v-spec hidden-grid', 'span', 'spec-value spec-value-interiorcolor'), 'interior_color')
    pi.addColumnDF(cars, pi.parse_subsection(soup, 'div', 'v-spec hidden-grid', 'span', 'spec-value spec-value-transmission'), 'transmission')
    pi.addColumnDF(cars, pi.parse_subsection(soup, 'div', 'v-spec hidden-grid', 'span', 'spec-value spec-value-enginedescription'), 'engine')
    pi.addColumnDF(cars, pi.parse_subsection(soup, 'div', 'v-spec hidden-grid', 'span', 'spec-value spec-value-drivetrain'), 'drivetrain')
    pi.addColumnDF(cars, pi.parse_attr(soup, 'data-cg-vin')[::2], 'vin')

    # Add dealership info + scrape date
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)

    return cars    


# mod-vehicle-price mod-vehicle-price-responsive1 mod-vehicle-price-listing
# mod-vehicle-price mod-vehicle-price-responsive1 mod-vehicle-price-listing