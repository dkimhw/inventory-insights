import pandas as pd
import numpy as np
import re
import sqlite3
import datetime


##########################################
# HTML Parsing Helper Functions
##########################################

# Parses all the HTML elements under a given section
# Can give a specific attribute to look for and returns 
# the text associated with each tag that has the key-value you are looking for
def parse_main_section_attr_text_all(soup
                              , main_section
                              , main_section_class = None
                              , sub_section_attr_parse_key = None # If you have a specific subsection to grab based on attribute (usually when there is no class to identify)
                              , sub_section_attr_parse_value = None):
    col_data = []
    if main_section_class is None:
        main = soup.findAll(main_section)
    else:
        main = soup.findAll(main_section, main_section_class)
    
    for el in main:
        sub_data = el.findAll()
        appendedData = False
        for sd in sub_data:
            if sub_section_attr_parse_key is not None and sub_section_attr_parse_value is not None:
                if sd.get(sub_section_attr_parse_key) == sub_section_attr_parse_value:
                    col_data.append(sd.getText())
                    appendedData = True
            else:
                col_data.append(sd.getText())
                appendedData = True
        if (appendedData == False):
            col_data.append(None)

    return col_data

# Function returns the contents of elements with a specific attribute under specific main & subsection
# It will loop over all subsections to return the elements with attribute name
# You can all pass in specific attr key-value pair that you are looking for (i.e. the subsection has multiple elements with same attribute_name)
def parse_subsection_attr_all(soup
                              , attribute_name # The specific attribute content you want to parse out
                              , main_section
                              , sub_section
                              , main_section_class = None
                              , sub_section_class = None
                              , sub_section_attr_parse_key = None # If you have a specific subsection to grab based on attribute (usually when there is no class to identify)
                              , sub_section_attr_parse_value = None):
    col_data = []
    if main_section_class is None:
        main = soup.findAll(main_section)
    else:
        main = soup.findAll(main_section, main_section_class)
    
    for el in main:
        if sub_section_class is None:
            sub_data = el.findAll(sub_section)
        else:
            sub_data = el.findAll(sub_section, { "class" : sub_section_class})

        for sd in sub_data:
            if sub_section_attr_parse_key is not None and sub_section_attr_parse_value is not None:
                if sd.get(sub_section_attr_parse_key) == sub_section_attr_parse_value:
                    col_data.append(sd.get(attribute_name))
            else:
                col_data.append(sd.get(attribute_name))
    return col_data


# Parse subsection of the passed in HTML Data & returns data for a specific attribute of that subsection
# This function only looks at the first subsection; if there are multiple subsections that need to be parsed out use parse_subsection_attr_all
def parse_subsection_attr(soup
                          , attribute_name
                          , main_section
                          , sub_section
                          , main_section_class = None
                          , sub_section_class = None):
    col_data = []
    if main_section_class is None:
        main = soup.findAll(main_section)
    else:
        main = soup.findAll(main_section, main_section_class)
    
    for el in main:
        if sub_section_class is None:
            sub_data = el.find(sub_section)
        else:
            sub_data = el.find(sub_section, { "class" : sub_section_class})
                
        if sub_data is None:
            col_data.append(None)
        else:
            col_data.append(sub_data.attrs[attribute_name])
    return col_data

# Parse subsection of the HTML data
# But instead of only taking the first subsection 
# It finds and loops through all subsection with given arguments
def parse_subsection_all(soup
                    , main_section
                    , sub_section
                    , main_section_class = None
                    , sub_section_class = None
                    , parse_type = None):
    col_data = []
    if main_section_class is None:
        main = soup.findAll(main_section)
    else:
        main = soup.findAll(main_section, main_section_class)    

    for el in main:
        if sub_section_class is None:
            sub_data = el.findAll(sub_section)
        else:
            sub_data = el.findAll(sub_section, { "class" : sub_section_class})

        for sd in sub_data:
            # If subsection is missing append One
            if sd is None:
                col_data.append(None)
            else:
                if parse_type == 'get_text':
                    parsed = sd.get_text()
                else:
                    parsed = sd.string
                col_data.append(parsed)
    return col_data

# Parse subsection of the HTML data
# Can pass in specific classes for main sections and subsections for more targeted  
# Parse Type = can specify string (the direct content) or specify get_text which will return text of all selected elements in subsection
def parse_subsection(soup
                    , main_section
                    , sub_section
                    , main_section_class = None
                    , sub_section_class = None
                    , parse_type = None):
    col_data = []
    if main_section_class is None:
        main = soup.findAll(main_section)
    else:
        main = soup.findAll(main_section, main_section_class)    

    for el in main:
        if sub_section_class is None:
            sub_data = el.find(sub_section)
        else:
            sub_data = el.find(sub_section, { "class" : sub_section_class})

        # If subsection is missing append One
        if sub_data is None:
            col_data.append(None)
        else:
            if parse_type == 'get_text':
                parsed = sub_data.get_text()
            else:
                parsed = sub_data.string
            col_data.append(parsed)
    return col_data

# Parse a specific tag with a specific class
def parse_tag(soup, html_tag, html_class):
    dataColumn = soup.find_all(html_tag, class_=html_class)
    new_col_list = []
    
    for i in range(0, len(dataColumn)):
        new_col_list.append(dataColumn[i].get_text().strip())
        
    return new_col_list

# Parse a specific tag with a specific attribute
def parse_class_attr(soup, html_tag, html_class, attribute_name):
    dataColumn = soup.find_all(html_tag, class_=html_class)
    new_col_list = []
    
    for i in range(0, len(dataColumn)):
        new_col_list.append(dataColumn[i].attrs[attribute_name].strip())
    
    return new_col_list


##########################################
# Other Misc Helper Functions for Parsing
##########################################

# Add new column to data frame
def add_column_df(df, arr, col_name):
    df_tmp = pd.DataFrame(arr, columns = [col_name])
    df[col_name] = df_tmp[col_name]

# Conver to numeric data (price/mileage)
def convert_to_numeric_type(lst):
    scraped_data = lst
    parsed_data = []
    numeric_data = []
    
    for el in scraped_data:
        if el is None:
            parsed_data.append('')
        else:
            cleaned_el = el.replace('Price Includes $750 Down Payment Assistance', '')
            parsed_data.append(re.sub("[^0-9]", "", cleaned_el))
        
    for data in parsed_data:
        if data == '':
            numeric_data.append(np.nan)
        else:
            numeric_data.append(int(data))
    
    return numeric_data    

# Grab vehicle manufacture year
def get_valid_year(lst):
    models = lst
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
def get_car_make_model_type(lst):
    full_titles = lst
    makes = []
    models = []
    vehicle_types = []
    valid_makes = ['BMW', 'Audi', 'Toyota', 'Lexus', 'Ford', 'Honda'
                   , 'Hyundai', 'Kia', 'Chevrolet', 'Jeep', 'Nissan', 'Volkswagen'
                   , 'Mitsubishi', 'Mazda', 'GMC', 'Cadillac', 'Land Rover', 'Dodge'  
                   , 'Jaguar', 'Volvo', 'Alfa Romeo', 'MINI Cooper', 'Buick'
                   , 'Fiat', 'Tesla', 'Lincoln', 'Maserati', 'smart', 'Aston Martin'
                   , 'Porsche', 'Pontiac', 'Lamborghini', 'Rolls-Royce', 'Bentley'
                   , 'HUMMER', 'Mercury'
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

# Helper function to clean up scraped data where the scraped data will return
def clean_text_data(lst, string_to_rmv = None):
    cleaned_lst = []
    for el in lst:
        if el is None:
            cleaned_lst.append(None)            
        elif string_to_rmv is None:
            cleaned_lst.append(el.strip())       
        elif string_to_rmv.lower() in el.lower():
            cleaned_lst.append(el.split(':')[1].strip())            
    return cleaned_lst

def data_length_validation(dict, valid_len):
  for key in dict:
    curr_key_len = len(dict[key])
    if (curr_key_len != valid_len):
      return False
  
  return True  

##########################################
# Sqlite3 Inventory Parsing Helper Functions
##########################################

# Given a dataframe - adds it to a sqlite database table
def add_data_to_sqlite3(db_name, tbl_name, df):
    # Add data to a SQLite database
    conn = sqlite3.connect(db_name) # 'cars.db'
    df.to_sql(tbl_name, conn, if_exists='append', index=False)   

# Given a dataframe - adds it to a sqlite database table
def add_inventory_data_sqlite3(db_name, tbl_name, df):
    # Add data to a SQLite database
    conn = sqlite3.connect(db_name) # 'cars.db'
    df.to_sql(tbl_name, conn, if_exists='append', index=False)    

# Returns the last time a dealership was scraped
def days_since_last_scrape(dealership_name, db_name, tbl_name):
    # First check if the table exists
    conn = sqlite3.connect('cars.db')
    check_table = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tbl_name}';"
    tbl = pd.read_sql_query(check_table, conn)
    
    if (tbl['name'].empty):
        return np.nan
    else:
        conn = sqlite3.connect(db_name)
        sql_query = f"SELECT MAX(scraped_date) AS min_scraped_date from {tbl_name} WHERE dealership_name = '{dealership_name}'"
        result = pd.read_sql_query(sql_query, conn)
        past = pd.to_datetime(result['min_scraped_date'])[0]
        now = datetime.datetime.now()
        duration = now - past
        duration_in_s = duration.total_seconds()
        days  = divmod(duration_in_s, 86400)[0]
        
        return days


##########################################
# To Refactor & Get Rid of Later
##########################################

# Parse a specific tag + class
def parseColumn(soup, html_tag, html_class):
    dataColumn = soup.find_all(html_tag, class_=html_class)
    new_col_list = []
    
    for i in range(0, len(dataColumn)):
        new_col_list.append(dataColumn[i].get_text().strip())
        
    return new_col_list

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

# Parse out data from attributes of elements
def parse_attr(soup, attr_name):
    attrs = []
    for elm in soup.find_all('span'):
        if attr_name in elm.attrs:
            if elm.attrs[attr_name] != '':
                attrs.append(elm.attrs[attr_name])
    return attrs