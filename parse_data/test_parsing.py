
from curses.ascii import TAB
import parse_inventory as pi
import parse_dealership
import requests
import re
from bs4 import BeautifulSoup
import numpy as np

# Dealership Info Dictionary
# Dealership Info Dictionary
dealerships = {
    'Irwin Automotive Group': {
        'url': 'https://www.irwinzone.com/searchused.aspx?pn=50',
        'pagination_url': 'https://www.irwinzone.com/searchused.aspx?pn=50&pt=2',
        'dealership_name': 'Irwin Automotive Group',
        'address': '59 Bisson Avenue',
        'zipcode': '03246',
        'city': 'Laconia',
        'state': 'NH'
    }
}



# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
  # Set scrapping parameters
  headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
  }

  TABLE_NAME = 'inventory_test'
  ERROR_TBL_NAME = 'parsing_errors'
  DB_NAME = 'cars_test.db'
  TIME_BTWN_SCRAPE = 21


  for key in dealerships:
    print("Processing: ", key)
    if key == 'Irwin Automotive Group':
        days_since= pi.days_since_last_scrape(key, DB_NAME, TABLE_NAME)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_irwin_auto_inventory_data(soup, dealerships[key], dealerships[key]['url'])

            if 'error' in data.columns:
                pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
            else:
                pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

            # Parse out other pages if there are any available
            pagination_url = dealerships[key]['pagination_url']
            page_counter = 2

            while (True):
                response = requests.get(pagination_url, headers = headers)
                soup_pagination = BeautifulSoup(response.text, "html.parser")
                title = pi.parse_class_attr(soup_pagination, 'div', 'row srpVehicle hasVehicleInfo', 'data-name')

                print(pagination_url)
                if len(title) == 0:
                    break
                else:
                    data = parse_dealership.get_irwin_auto_inventory_data(soup_pagination, dealerships[key], pagination_url)
                    if 'error' in data.columns:
                        pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
                    else:
                        pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

                page_counter += 1
                pagination_url = re.sub('pt=[0-9]+', f'pt={page_counter}', pagination_url)
