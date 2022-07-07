
import sqlite3
import pandas as pd

CONN = sqlite3.connect('../data/cars.db')

def query(sql_query):
  result = pd.read_sql_query(sql_query, CONN)
  return result
