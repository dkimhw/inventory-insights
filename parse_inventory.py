import pandas as pd
import numpy as np
import re
import sqlite3
import datetime

# Parse subsection of data by using their classes but to ensure all vehicles are accounted
# even if the subsection is missing (append None in those cases)

def parse_subsection(soup, main_section, main_section_class, sub_section, sub_section_class):
    col_data = []

    for el in soup.findAll(main_section, main_section_class):
        sub_data = el.find(sub_section, { "class" : sub_section_class})
        if sub_data is None:
            col_data.append(None)
        else:
            col_data.append(sub_data.string)
    return col_data

# Parse out data from attributes of elements
def parse_attr(soup, attr_name):
    attrs = []
    for elm in soup.find_all('span'):
        if attr_name in elm.attrs:
            if elm.attrs[attr_name] != '':
                attrs.append(elm.attrs[attr_name])
    return attrs

# Parse a direct descendant
def parse_direct_children(soup, css_selector):
  data_col = soup.select(css_selector)
  # soup.select('h4 > a')[0].text.replace('\r', '').replace('\n', '').strip()
  new_col_list = []

  for i in range(0, len(data_col)):
    cleaned_text = data_col[i].text.replace('\r', '').replace('\n', '').strip()
    new_col_list.append(cleaned_text)

  return new_col_list

# Parse a specific tag + class
def parseColumn(soup, html_tag, html_class):
    dataColumn = soup.find_all(html_tag, class_=html_class)
    new_col_list = []
    
    for i in range(0, len(dataColumn)):
        new_col_list.append(dataColumn[i].get_text().strip())
        
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
        strip_model = model.strip()
        new_col_list.append(strip_model[0:4])
        
    return new_col_list

def fix_vehicle_type(df):
    # Check van & cargo
    for idx, row in df.iterrows():
        if 'van' in row['title'].lower() and 'cargo' in row['title'].lower() :
            row['vehicle_type'] = 'Cargo Van'
        elif 'sav' in row['title'].lower():
            row['vehicle_type'] = 'SUV'
        elif 'advance' in row['title'].lower() and 'Van' not in row['title']:
            row['vehicle_type'] = None

# Make & Model & Vehicle Type
def get_car_make_model_type(soup, html_tag, html_class):
    full_titles = parseColumn(soup, html_tag, html_class)
    makes = []
    models = []
    vehicle_types = []
    valid_makes = ['BMW', 'Audi', 'Toyota', 'Lexus', 'Ford', 'Honda'
                   , 'Hyundai', 'Kia', 'Chevrolet', 'Jeep', 'Nissan', 'Volkswagen'
                   , 'Mitsubishi', 'Mazda', 'GMC', 'Cadillac', 'Land Rover', 'Dodge'  
                   , 'Jaguar', 'Volvo', 'Alfa Romeo', 'MINI Cooper', 'Buick'
                   , 'Fiat', 'Tesla', 'Lincoln', 'Maserati', 'smart'
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
            make = make.strip()
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

def get_numeric_vehicle_data(soup, html_tag, html_class):
    scraped_data = parseColumn(soup, html_tag, html_class)
    parsed_data = []
    numeric_data = []
    
    for el in scraped_data:
        cleaned_el = el.replace('Price Includes $750 Down Payment Assistance', '')
        parsed_data.append(re.sub("[^0-9]", "", cleaned_el))
        
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

def add_inventory_data_sqlite3(db_name, tbl_name, df):
    # Add data to a SQLite database
    conn = sqlite3.connect(db_name) # 'cars.db'
    df.to_sql(tbl_name, conn, if_exists='append', index=False)    

def days_since_last_scrape(dealership_name, db_name, tbl_name):
    # First check if the table exists
    conn = sqlite3.connect('cars.db')
    check_table = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tbl_name}';"
    tbl = pd.read_sql_query(check_table, conn)
    
    if (tbl['name'].empty):
        return np.nan
    else:
        conn = sqlite3.connect(db_name)
        sql_query = f"SELECT MIN(scraped_date) AS min_scraped_date from {tbl_name} WHERE dealership_name = '{dealership_name}'"
        result = pd.read_sql_query(sql_query, conn)
        past = pd.to_datetime(result['min_scraped_date'])[0]
        now = datetime.datetime.now()
        duration = now - past
        duration_in_s = duration.total_seconds()
        days  = divmod(duration_in_s, 86400)[0]
        
        return days