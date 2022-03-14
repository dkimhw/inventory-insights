
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
import re


################################################
# Helper functions #
################################################

# Parse a specific tag + class
def parseColumn(soup, html_tag, html_class):
    dataColumn = soup.find_all(html_tag, class_=html_class)
    new_col_list = []
    
    for i in range(0, len(dataColumn)):
        new_col_list.append(dataColumn[i].get_text())
        
    return new_col_list

# Add new column to data frame
def addColumnDF(df, arr, col_name):
    df_tmp = pd.DataFrame(arr, columns = [col_name])
    df[col_name] = df_tmp[col_name]

# Grab vehicle manufacture year
def get_valid_year(soup, html_tag, html_class):
    models = parseColumn(soup, html_tag, html_class)
    new_col_list = []
    
    for model in models:
        new_col_list.append(model[0:4])
        
    return new_col_list

def fix_vehicle_type(df):
    # Check van & cargo
    for idx, row in df.iterrows():
        if 'van' in row['title'].lower() and 'cargo' in row['title'].lower() :
            row['vehicle_type'] = 'Cargo Van'
        elif 'sav' in row['title'].lower():
            row['vehicle_type'] = 'SUV'

# Make & Model & Vehicle Type
def get_car_make_model_type(soup, html_tag, html_class):
    full_titles = parseColumn(soup, html_tag, html_class)
    makes = []
    models = []
    vehicle_types = []
    valid_makes = ['BMW', 'Audi', 'Toyota', 'Lexus', 'Ford', 'Honda'
                   , 'Hyundai', 'Kia', 'Chevrolet', 'Jeep', 'Nissan', 'Volkswagen'
                   , 'Mitsubishi', 'Mazda', 'GMC', 'Cadillac', 'Land Rover', 'Dodge'  
                   , 'Jaguar', 'Volvo'         
                   , 'Subaru', 'Ram', 'Chrysler', 'Acura', 'Mercedes-Benz', 'Infiniti']
    
    valid_vehicle_type = ['Sedan', 'SUV', 'Coupe', 'Wagon', 'Hatchback', 'Truck', 'Cargo Van', 'Van']
    
    # Remove years
    for idx in range(len(full_titles)):
        full_titles[idx] = full_titles[idx][5:]
        
    for model in full_titles:
        clean_model = ''
        stripped_make = ''
        stripped_type = ''
        for make in valid_makes:
            if make.lower() in model.lower():
                stripped_make = make
                clean_model = model.replace(make, '')
        
        for vt in valid_vehicle_type:
            if vt.lower() in clean_model.lower():
                stripped_type = vt
                clean_model = clean_model.replace(vt, '')
                
        if (stripped_make != ''):
            makes.append(stripped_make.strip())
        else:
            makes.append(None) # if none matches add a none
        
        if (stripped_type != ''):
            vehicle_types.append(stripped_type.strip())
        else:
            vehicle_types.append(None) # if none matches add a none
        
        models.append(clean_model.strip()) 

    return makes, models, vehicle_types

# def get_numeric_vehicle_data(html_tag, html_class):
#     scraped_mileages = parseColumn(html_tag, html_class)
#     mileages = []
    
#     for mileage in scraped_mileages:
#         mileages.append(int(re.sub("[^0-9]", "", mileage)))
    
#     return mileages

def get_numeric_vehicle_data(soup, html_tag, html_class):
    scraped_data = parseColumn(soup, html_tag, html_class)
    parsed_data = []
    numeric_data = []
    
    for el in scraped_data:
        parsed_data.append(re.sub("[^0-9]", "", el))
        
    for data in parsed_data:
        if data == '':
            numeric_data.append(np.nan)
        else:
            numeric_data.append(int(data))
    
    return numeric_data

# Use for when vehicle data doesn't have specific class names
def get_misc_vehicle_data(soup, html_tag, html_class, vehicle_data_type):
    misc_vehicle_data = parseColumn(soup, html_tag, html_class)
    vehicle_data_list = []
    for row in misc_vehicle_data:
        if vehicle_data_type not in row.lower():
            vehicle_data_list.append(None)
            continue

        for el in row.split('\n'):
            if vehicle_data_type.lower() in el.lower():
                vehicle_data_list.append(el.split(':')[1].strip())
    return vehicle_data_list

# Scrape inventory HTML
def get_direct_auto_inventory_data(soup, dealership_info):    
    # Initialize empty data frame
    cars = pd.DataFrame()
    
    # Add title
    title = parseColumn(soup, 'h2', 'ebiz-vdp-title color m-0')    
    addColumnDF(cars, title, 'title')

    # Add vehicle manufacture date
    years = get_valid_year(soup, 'h2', 'ebiz-vdp-title color m-0')
    addColumnDF(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = get_car_make_model_type(soup, 'h2', 'ebiz-vdp-title color m-0')
    addColumnDF(cars, makes, 'make')
    addColumnDF(cars, models, 'models')
    addColumnDF(cars, vtypes, 'vehicle_type')

    # Add mileage col
    miles = get_numeric_vehicle_data(soup, 'li', 'mileage-units')
    addColumnDF(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = get_numeric_vehicle_data(soup, 'div', 'price-item')
    addColumnDF(cars, car_prices, 'price')

    # Add Colors & transmission & other cols
    addColumnDF(cars, get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'exterior'), 'exterior_color')
    addColumnDF(cars, get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'interior'), 'interior_color')
    addColumnDF(cars, get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'transmission'), 'transmission')
    addColumnDF(cars, get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'engine'), 'engine')
    addColumnDF(cars, parseColumn(soup, 'li', 'vin'), 'vin')
    cars['vin'] = cars['vin'].str.replace('VIN #: ', '')
    
    # Add dealership info + scrape date
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)
    
    # Add data to a SQLite database
    conn = sqlite3.connect('cars.db')
    cars.to_sql('inventory', conn, if_exists='append', index=False)


def get_bostonyan_inventory_data(soup, dealership_info):
    # Scrape inventory HTML
    # response = requests.get(dealership_info['url'], headers = headers)
    # soup = BeautifulSoup(response.text, "html.parser")

    # Initialize empty data frame
    cars = pd.DataFrame()

    # Add vehicle title
    title = parseColumn(soup, 'a', 'accent-color1')
    addColumnDF(cars, title, 'title')

    # Add vehicle manufacture date
    years = get_valid_year(soup, 'a', 'accent-color1')
    addColumnDF(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = get_car_make_model_type(soup, 'a', 'accent-color1')
    addColumnDF(cars, makes, 'make')
    addColumnDF(cars, models, 'models')
    addColumnDF(cars, vtypes, 'vehicle_type')

    # Add mileage col
    miles = get_numeric_vehicle_data(soup, 'span', 'mileage')
    addColumnDF(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = get_numeric_vehicle_data(soup, 'div', 'pricevalue1 accent-color1')
    addColumnDF(cars, car_prices, 'price')

    # Add Colors & transmission & other cols
    addColumnDF(cars, parseColumn(soup,'span', 'Extcolor'), 'exterior_color')
    addColumnDF(cars, parseColumn(soup,'span', 'Intcolor'), 'interior_color')
    addColumnDF(cars, parseColumn(soup,'div', 'transmission'), 'transmission')
    addColumnDF(cars, parseColumn(soup,'div', 'engine'), 'engine')
    addColumnDF(cars, parseColumn(soup,'span', 'vin'), 'vin')

    # Add dealership info + scrape date
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)

    # Add data to a SQLite database
    conn = sqlite3.connect('cars.db')
    cars.to_sql('inventory', conn, if_exists='append', index=False)

def get_fafama_inventory_data(soup, dealership_info):
    # Initialize empty data frame
    cars = pd.DataFrame()
    
    # Add title
    title = parseColumn(soup, 'h2', 'color m-0 ebiz-vdp-title')    
    addColumnDF(cars, title, 'title')

    # Add vehicle manufacture date
    years = get_valid_year(soup, 'h2', 'color m-0 ebiz-vdp-title')
    addColumnDF(cars, years, 'year')

    # Add make, models, and vehicle type
    makes, models, vtypes = get_car_make_model_type(soup, 'h2', 'color m-0 ebiz-vdp-title')
    addColumnDF(cars, makes, 'make')
    addColumnDF(cars, models, 'models')
    addColumnDF(cars, vtypes, 'vehicle_type')
    
    # Clean up vehicle type
    fix_vehicle_type(cars)

    # Add mileage col
    miles = get_numeric_vehicle_data(soup, 'li', 'mileage-units')
    addColumnDF(cars, miles, 'vehicle_mileage')

    # Add price
    car_prices = get_numeric_vehicle_data(soup, 'div', 'price-item active mt-3 mt-md-0')
    addColumnDF(cars, car_prices, 'price')

    # Add Colors & transmission & other cols
    addColumnDF(cars, get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'exterior'), 'exterior_color')
    addColumnDF(cars, get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'interior'), 'interior_color')
    addColumnDF(cars, get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'transmission'), 'transmission')
    addColumnDF(cars, get_misc_vehicle_data(soup, 'ul', 'small list-unstyled mb-0', 'engine'), 'engine')
    addColumnDF(cars, parseColumn(soup, 'li', 'vin'), 'vin')
    cars['vin'] = cars['vin'].str.replace('VIN #: ', '')
    
    # Add dealership info + scrape date
    cars['dealership_name'] = dealership_info['dealership_name']
    cars['dealership_address'] = dealership_info['address']
    cars['dealership_zipcode'] = dealership_info['zipcode']
    cars['dealership_city'] = dealership_info['city']
    cars['dealership_state'] = dealership_info['state']
    cars['inventory_url'] = dealership_info['url']
    cars['scraped_date'] = datetime.now(tz = None)
    
    # Add data to a SQLite database
    conn = sqlite3.connect('cars.db')
    cars.to_sql('inventory', conn, if_exists='append', index=False)    

# Dealership Info Dictionary
dealerships = {
    'Bostonyan Auto Group': {
        'url': 'https://www.bostonyanautogroup.com/view-inventory',
        'pagination_url': '',
        'dealership_name': 'Bostonyan Auto Group',
        'address': '119 Worcester St',
        'zipcode': '01760',
        'city': 'Natick',
        'state': 'MA'
    },
    'Direct Auto Mecca': {
        'url': 'https://www.directautomecca.com/view-inventory.aspx',
        'pagination_url': 'https://www.directautomecca.com/inventory.aspx?_new=true&_used=true&_page=2',
        'dealership_name': 'Direct Auto Mecca',
        'address': '154 Waverly Street',
        'zipcode': '01760',
        'city': 'Natick',
        'state': 'MA'
    },
    'Fafama Auto Sales': {
        'url': 'https://www.fafama.com/used-cars.aspx',
        'pagination_url': 'https://www.fafama.com/inventory.aspx?_used=true&_page=2',
        'dealership_name': 'Fafama Auto Sales',
        'address': '5 Cape Road',
        'zipcode': '01757',
        'city': 'Milford',
        'state': 'MA'
    }    
}



# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
  # Set scrapping parameters
  headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
  }

  for key in dealerships:
    if key == 'Bostonyan Auto Group':
        # Start with parsing the first inventory page
        response = requests.get(dealerships[key]['url'], headers = headers)
        soup = BeautifulSoup(response.text, "html.parser")        
        get_bostonyan_inventory_data(soup, dealerships[key])
    elif key == 'Direct Auto Mecca':
        # Start with parsing the first inventory page
        response = requests.get(dealerships[key]['url'], headers = headers)
        soup = BeautifulSoup(response.text, "html.parser")
        get_direct_auto_inventory_data(soup, dealerships[key])

        # Parse out other pages if there are any available
        pagination_url = dealerships[key]['pagination_url']
        page_counter = 2

        while (True):
            response = requests.get(pagination_url, headers = headers)
            soup_pagination = BeautifulSoup(response.text, "html.parser")   
            title = parseColumn(soup_pagination, 'h2', 'ebiz-vdp-title color m-0')
            
            if len(title) == 0:
                break
            else:
                get_direct_auto_inventory_data(soup_pagination, dealerships[key])
            
            page_counter += 1
            pagination_url = re.sub('page=[0-9+]', f'page={page_counter}', pagination_url)   
    elif key == 'Fafama Auto Sales':
        # Start with parsing the first inventory page
        response = requests.get(dealerships[key]['url'], headers = headers)
        soup = BeautifulSoup(response.text, "html.parser")
        get_fafama_inventory_data(soup, dealerships[key])

        # Parse out other pages if there are any available
        pagination_url = dealerships[key]['pagination_url']
        page_counter = 2

        while (True):
            response = requests.get(pagination_url, headers = headers)
            soup_pagination = BeautifulSoup(response.text, "html.parser")   
            title = parseColumn(soup_pagination, 'h2', 'color m-0 ebiz-vdp-title')
            
            if len(title) == 0:
                break
            else:
                get_fafama_inventory_data(soup_pagination, dealerships[key])
            
            page_counter += 1
            pagination_url = re.sub('page=[0-9+]', f'page={page_counter}', pagination_url)   