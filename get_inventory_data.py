
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
import re


################################################
# Helper functions #
################################################

# Parse a specific tag + class
def parseColumn(html_tag, html_class):
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
def get_valid_year(html_tag, html_class):
    models = parseColumn(html_tag, html_class)
    new_col_list = []
    
    for model in models:
        new_col_list.append(model[0:4])
        
    return new_col_list

# Make & Model & Vehicle Type
def get_car_make_model_type(html_tag, html_class):
    full_titles = parseColumn(html_tag, html_class)
    makes = []
    models = []
    vehicle_types = []
    valid_makes = ['BMW', 'Audi', 'Toyota', 'Lexus', 'Ford', 'Honda'
                   , 'Hyundai', 'Kia', 'Chevrolet', 'Jeep', 'Nissan'
                   , 'Subaru', 'Ram', 'Chrysler', 'Acura', 'Mercedes-Benz', 'Infiniti']
    
    valid_vehicle_type = ['Sedan', 'SUV', 'Coupe', 'Wagon']
    
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

def get_mileage(html_tag, html_class):
    scraped_mileages = parseColumn(html_tag, html_class)
    mileages = []
    
    for mileage in scraped_mileages:
        mileages.append(int(re.sub("[^0-9]", "", mileage)))
    
    return mileages



# Dealership Info Dictionary
dealerships = {
    'Bostonyan Auto Group': {
        'url': 'https://www.bostonyanautogroup.com/view-inventory',
        'dealership_name': 'Bostonyan Auto Group',
        'address': '119 Worcester St',
        'zipcode': '01760',
        'city': 'Natick',
        'state': 'MA'
    }
}


# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
  # Set scrapping parameters
  headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
  }
  URL = dealerships['Bostonyan Auto Group']['url']

  # Scrape inventory HTML
  response = requests.get(URL, headers = headers)
  soup = BeautifulSoup(response.text, "html.parser")

  # Initialize empty data frame
  cars = pd.DataFrame()

  # Add vehicle manufacture date
  years = get_valid_year('a', 'accent-color1')
  addColumnDF(cars, years, 'year')

  # Add make, models, and vehicle type
  makes, models, vtypes = get_car_make_model_type('a', 'accent-color1')
  addColumnDF(cars, makes, 'make')
  addColumnDF(cars, models, 'models')
  addColumnDF(cars, vtypes, 'vehicle_type')

  # Add mileage col
  miles = get_mileage('span', 'mileage')
  addColumnDF(cars, miles, 'vehicle_mileage')

  # Add Colors & transmission & other cols
  addColumnDF(cars, parseColumn('span', 'Extcolor'), 'exterior_color')
  addColumnDF(cars, parseColumn('span', 'Intcolor'), 'interior_color')
  addColumnDF(cars, parseColumn('div', 'transmission'), 'transmission')
  addColumnDF(cars, parseColumn('div', 'fuel'), 'fuel')
  addColumnDF(cars, parseColumn('div', 'engine'), 'engine')
  addColumnDF(cars, parseColumn('span', 'vin'), 'vin')

  # Add dealership info + scrape date
  cars['dealership_name'] = dealerships['Bostonyan Auto Group']['dealership_name']
  cars['dealership_address'] = dealerships['Bostonyan Auto Group']['address']
  cars['dealership_zipcode'] = dealerships['Bostonyan Auto Group']['zipcode']
  cars['dealership_city'] = dealerships['Bostonyan Auto Group']['city']
  cars['dealership_state'] = dealerships['Bostonyan Auto Group']['state']
  cars['inventory_url'] = dealerships['Bostonyan Auto Group']['url']
  cars['scraped_date'] = datetime.now(tz = None)

  # Add data to a SQLite database
  conn = sqlite3.connect('cars.db')
  cars.to_sql('inventory', conn, if_exists='append', index=False)
