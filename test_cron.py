from datetime import datetime
import pandas as pd
from pathlib import Path  

data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
data = pd.DataFrame.from_dict(data)
filepath = Path('/Users/davidkim/Documents/python_projects/dealership_competitor_dash/out.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
data.to_csv(filepath)  