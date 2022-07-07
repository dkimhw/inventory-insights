"""
Script scrapes dealership data and moves data from staging to production inventory database
"""

import get_inventory_data as gid
import productionize as p

if __name__ == '__main__':
  gid.get_dealership_inventory_data()
  p.productionize()
