
from curses.ascii import TAB
import parse_inventory as pi
import parse_dealership
import requests
import re
from bs4 import BeautifulSoup
import numpy as np

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
    },
    'Newton Automotive Sales': {
        'url': 'https://www.newtonautoandsales.com/cars-for-sale',
        'pagination_url': 'https://www.newtonautoandsales.com/cars-for-sale?PageNumber=2&Sort=MakeAsc&StockNumber=&Condition=&BodyStyle=&Make=&MaxPrice=&Mileage=&SoldStatus=AllVehicles&StockNumber=',
        'dealership_name': 'Newton Automotive Sales',
        'address': '249 Centre Street',
        'zipcode': '02458',
        'city': 'Newton',
        'state': 'MA'
    },
    'Blasius Boston': {
        'url': 'https://www.blasiusboston.com/used-cars-holliston-ma',
        'pagination_url': 'https://www.blasiusboston.com/used-cars-holliston-ma?page=2',
        'dealership_name': 'Blasius Boston',
        'address': '1286 Washington Street',
        'zipcode': '01746',
        'city': 'Holliston',
        'state': 'MA'
    },
    'Avon Auto Brokers': {
        'url': 'https://avonautobrokers.com/newandusedcars?clearall=1',
        'pagination_url': 'https://avonautobrokers.com/newandusedcars?page=2',
        'dealership_name': 'Avon Auto Brokers',
        'address': '159 Memorial Drive',
        'zipcode': '02322',
        'city': 'Avon',
        'state': 'MA'
    }, 
    'Johns Auto Sales': {
        'url': 'https://johnsautosales.com/newandusedcars?clearall=1',
        'pagination_url': 'https://johnsautosales.com/newandusedcars?page=2',
        'dealership_name': "John's Auto Sales",
        'address': '181 Somerville Avenue',
        'zipcode': '02143',
        'city': 'Somerville',
        'state': 'MA'
    },
    'JM Automotive': {
        'url': 'https://www.jmautomotive.com/cars-for-sale-in-Naugatuck-CT-Hartford-New-Haven/used_cars',
        'pagination_url': 'https://www.jmautomotive.com/inventory.aspx?pg=2&sort=12&limit=50&vstatus=1&status=6',
        'dealership_name': 'J&M Automotive',
        'address': '756/820 New Haven Road',
        'zipcode': '06770',
        'city': 'Naugatuck',
        'state': 'CT'
    }
}


# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
  # Set scrapping parameters
  headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
  }

  TABLE_NAME = 'test'
  ERROR_TBL_NAME = 'parsing_errors_test'
  DB_NAME = 'cars.db'

  for key in dealerships:
    print("Processing: ", key)
    if key == 'Bostonyan Auto Group':
        days_since= pi.days_since_last_scrape(key, DB_NAME, TABLE_NAME)

        # Only import if not in table or if days since > 14
        if np.isnan(days_since) or days_since > 14:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")        
            data = parse_dealership.get_bostonyan_inventory_data(soup, dealerships[key], dealerships[key]['url'])
            
            if 'error' in data.columns:
                pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
            else:
                pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)