import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from config import settings

engine = create_engine(f'postgresql://{settings.username}:{settings.password}@{settings.host}:{settings.port}/{settings.database}')

def query(sql_query):
  result = pd.read_sql_query(sqlalchemy.text(sql_query), engine)
  return result
