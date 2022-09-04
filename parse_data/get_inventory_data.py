
from curses.ascii import TAB
import parse_inventory as pi
import parse_dealership
import requests
import re
from bs4 import BeautifulSoup
import numpy as np

# Set scrapping parameters
headers = {
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}

PROD_TABLE = 'inventory'
TABLE_NAME = 'inventory_staging'
ERROR_TBL_NAME = 'parsing_errors'
DB_NAME = '../data/cars.db'
TIME_BTWN_SCRAPE = 28

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
        'dealership_name': "Johns Auto Sales",
        'address': '181 Somerville Avenue',
        'zipcode': '02143',
        'city': 'Somerville',
        'state': 'MA'
    },
    'J&M Automotive': {
        'url': 'https://www.jmautomotive.com/cars-for-sale-in-Naugatuck-CT-Hartford-New-Haven/used_cars',
        'pagination_url': 'https://www.jmautomotive.com/inventory.aspx?pg=2&sort=12&limit=50&vstatus=1&status=6',
        'dealership_name': 'J&M Automotive',
        'address': '756/820 New Haven Road',
        'zipcode': '06770',
        'city': 'Naugatuck',
        'state': 'CT'
    },
    'CT Auto': {
        'url': 'https://www.ct-auto.com/cars-for-sale-in-Bridgeport-CT-Waterbury-Norwich/used_cars',
        'pagination_url': None,
        'dealership_name': 'CT Auto',
        'address': '7 Wayne Street',
        'zipcode': '06606',
        'city': 'Bridgeport',
        'state': 'CT'
    },
    'Irwin Automotive Group': {
        'url': 'https://www.irwinzone.com/searchused.aspx?pn=50',
        'pagination_url': 'https://www.irwinzone.com/searchused.aspx?pn=50&pt=2',
        'dealership_name': 'Irwin Automotive Group',
        'address': '59 Bisson Avenue',
        'zipcode': '03246',
        'city': 'Laconia',
        'state': 'NH'
    },
    'Stream Auto Outlet': {
        'url': 'https://www.streamautooutlet.com/inventory?type=used',
        'pagination_url': 'https://www.streamautooutlet.com/inventory?type=used&pg=2',
        'vehicle_detail_url': 'https://www.streamautooutlet.com',
        'dealership_name': 'Stream Auto Outlet',
        'address': '324 W Merrick Rd',
        'zipcode': '11580',
        'city': 'Valley Stream',
        'state': 'NY'
    }
}



def get_dealership_inventory_data():
  for key in dealerships:
    print("Processing: ", key)
    if key == 'Bostonyan Auto Group':
        days_since= pi.days_since_last_scrape(key, DB_NAME, PROD_TABLE)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_bostonyan_inventory_data(soup, dealerships[key], dealerships[key]['url'])

            if 'error' in data.columns:
                pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
            else:
                pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)
    elif key == 'Direct Auto Mecca':
        days_since= pi.days_since_last_scrape(key, DB_NAME, PROD_TABLE)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_direct_auto_inventory_data(soup, dealerships[key], dealerships[key]['url'])

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
                title = pi.parse_subsection(soup_pagination, 'div', 'h2', 'ml-0 ml-lg-5 pt-4 pb-2 border-bottom', 'ebiz-vdp-title color m-0')

                print(pagination_url)
                if len(title) == 0:
                    break
                else:
                    data = parse_dealership.get_direct_auto_inventory_data(soup_pagination, dealerships[key], pagination_url)
                    if 'error' in data.columns:
                        pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
                    else:
                        pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

                page_counter += 1
                pagination_url = re.sub('page=[0-9]+', f'page={page_counter}', pagination_url)
    elif key == 'Fafama Auto Sales':
        days_since= pi.days_since_last_scrape(key, DB_NAME, PROD_TABLE)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_fafama_inventory_data(soup, dealerships[key], dealerships[key]['url'])

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
                title = pi.parse_subsection(soup_pagination, 'div', 'h2', 'ml-0 ml-lg-5 pt-4 pb-2 border-bottom', 'color m-0 ebiz-vdp-title')

                print(pagination_url)
                if len(title) == 0:
                    break
                else:
                    data = parse_dealership.get_fafama_inventory_data(soup_pagination, dealerships[key], pagination_url)
                    if 'error' in data.columns:
                        pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
                    else:
                        pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

                page_counter += 1
                pagination_url = re.sub('page=[0-9]+', f'page={page_counter}', pagination_url)
    elif key == 'Newton Automotive Sales':
        days_since= pi.days_since_last_scrape(key, DB_NAME, PROD_TABLE)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_newton_auto_inventory_data(soup, dealerships[key], dealerships[key]['url'])

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
                title = pi.parse_subsection(soup_pagination, 'div', 'h3', 'vehicle-snapshot__information', 'vehicle-snapshot__title')

                print(pagination_url)
                if len(title) == 0:
                    break
                else:
                    data = parse_dealership.get_newton_auto_inventory_data(soup_pagination, dealerships[key], pagination_url)
                    if 'error' in data.columns:
                        pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
                    else:
                        pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

                page_counter += 1
                pagination_url = re.sub('PageNumber=[0-9]+', f'PageNumber={page_counter}', pagination_url)
    elif key == 'Blasius Boston':
        days_since= pi.days_since_last_scrape(key, DB_NAME, PROD_TABLE)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_blasius_inventory_data(soup, dealerships[key], dealerships[key]['url'])

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
                title = pi.clean_text_data(pi.parse_subsection(soup_pagination, 'div', 'div', 'vehicle', 'v-title', 'get_text'))

                print(pagination_url)
                if len(title) == 0:
                    break
                else:
                    data = parse_dealership.get_blasius_inventory_data(soup_pagination, dealerships[key], pagination_url)
                    if 'error' in data.columns:
                        pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
                    else:
                        pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

                page_counter += 1
                pagination_url = re.sub('page=[0-9]+', f'page={page_counter}', pagination_url)
    elif key == 'Avon Auto Brokers':
        days_since= pi.days_since_last_scrape(key, DB_NAME, PROD_TABLE)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_avon_inventory_data(soup, dealerships[key], dealerships[key]['url'])

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
                title = pi.parse_subsection_attr(soup_pagination, 'aria-label', 'div', 'a', 'i11r-vehicle')
                print(pagination_url)

                if len(title) == 0:
                    break
                else:
                    data = parse_dealership.get_avon_inventory_data(soup_pagination, dealerships[key], pagination_url)
                    if 'error' in data.columns:
                        pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
                    else:
                        pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

                page_counter += 1
                pagination_url = re.sub('page=[0-9]+', f'page={page_counter}', pagination_url)
    elif key == 'Johns Auto Sales':
        days_since= pi.days_since_last_scrape(key, DB_NAME, PROD_TABLE)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_johns_auto_inventory_data(soup, dealerships[key], dealerships[key]['url'])

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
                title = pi.clean_text_data(pi.parse_subsection(soup_pagination, 'div', 'h4', 'row no-gutters invMainCell', 'd-md-none titleWrapPhoneView', 'get_text'))

                print(pagination_url)
                if len(title) == 0:
                    break
                else:
                    data = parse_dealership.get_johns_auto_inventory_data(soup_pagination, dealerships[key], pagination_url)
                    if 'error' in data.columns:
                        pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
                    else:
                        pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

                page_counter += 1
                pagination_url = re.sub('page=[0-9]+', f'page={page_counter}', pagination_url)
    elif key == 'J&M Automotive':
        days_since= pi.days_since_last_scrape(key, DB_NAME, PROD_TABLE)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_jm_auto_inventory_data(soup, dealerships[key], dealerships[key]['url'])

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
                title = pi.parse_subsection_attr(soup_pagination, 'title','div', 'a', 'thumbnail', 'listitemlink')

                print(pagination_url)
                if len(title) == 0:
                    break
                else:
                    data = parse_dealership.get_jm_auto_inventory_data(soup_pagination, dealerships[key], pagination_url)
                    if 'error' in data.columns:
                        pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
                    else:
                        pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

                page_counter += 1
                pagination_url = re.sub('pg=[0-9]+', f'pg={page_counter}', pagination_url)
    elif key == 'CT Auto':
        days_since= pi.days_since_last_scrape(key, DB_NAME, PROD_TABLE)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_ct_auto_inventory_data(soup, dealerships[key], dealerships[key]['url'])

            if 'error' in data.columns:
                pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
            else:
                pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

            # No additional pages to parse
    elif key == 'Irwin Automotive Group':
        days_since= pi.days_since_last_scrape(key, DB_NAME, PROD_TABLE)

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
    elif key == 'Stream Auto Outlet':
        days_since= pi.days_since_last_scrape(key, DB_NAME, TABLE_NAME)

        if np.isnan(days_since) or days_since > TIME_BTWN_SCRAPE:
            # Start with parsing the first inventory page
            response = requests.get(dealerships[key]['url'], headers = headers)
            soup = BeautifulSoup(response.text, "html.parser")
            data = parse_dealership.get_stream_auto_outlet_inventory_data(soup, dealerships[key], dealerships[key]['url'], headers)

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
                title = pi.clean_text_data(pi.parse_subsection_all(soup_pagination, 'h4', 'span', 'srp-vehicle-title'))

                print(pagination_url)
                if len(title) == 0:
                    break
                else:
                    data = parse_dealership.get_stream_auto_outlet_inventory_data(soup_pagination, dealerships[key], pagination_url, headers)
                    if 'error' in data.columns:
                        pi.add_data_to_sqlite3(DB_NAME, ERROR_TBL_NAME, data)
                    else:
                        pi.add_data_to_sqlite3(DB_NAME, TABLE_NAME, data)

                page_counter += 1
                pagination_url = re.sub('pg=[0-9]+', f'pg={page_counter}', pagination_url)
