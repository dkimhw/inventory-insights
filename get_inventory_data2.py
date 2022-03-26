
from curses.ascii import TAB
import parse_inventory as pi
import parse_dealership
import requests
import re
from bs4 import BeautifulSoup
import numpy as np

# Dealership Info Dictionary
dealerships = {
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

  TABLE_NAME = 'inventory_staging'
  DB_NAME = 'cars.db'

  for key in dealerships:
    print(key)
    if key == 'JM Automotive':
        days_since= pi.days_since_last_scrape(key, DB_NAME, TABLE_NAME)
        print(days_since)

        if np.isnan(days_since) or days_since > 14:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_jm_auto_inventory_data(soup, dealerships[key])
            pi.add_inventory_data_sqlite3(DB_NAME, TABLE_NAME, data)

            # Parse out other pages if there are any available
            pagination_url = dealerships[key]['pagination_url']
            page_counter = 2

            while (True):
                response = requests.get(pagination_url, headers = headers)
                soup_pagination = BeautifulSoup(response.text, "html.parser")   
                title = pi.parse_subsection_attr(soup_pagination, 'title','div', 'a', 'thumbnail', 'listitemlink')
                
                print(pagination_url)
                if len(title) == 0:
                    break
                else:
                    data = parse_dealership.get_jm_auto_inventory_data(soup_pagination, dealerships[key])
                    pi.add_inventory_data_sqlite3(DB_NAME, TABLE_NAME, data)
                
                page_counter += 1
                pagination_url = re.sub('pg=[0-9]+', f'pg={page_counter}', pagination_url)  