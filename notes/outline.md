
## Next Steps:
1. Script to move data in staging to production & wiping staging (Done)
2. Build out data validations when parsing dealerships (Done)
    - If len of each data col is different it's not valid
    - If not valid:
        - Do not append the data to inventory_staging
        - Add to a table in cars.db that logs what the error was
    - Else:
        - Add to inventory_staging
3. Add up to 15 dealerships - currently at 8
4. Start working on dash
5. Build out the main dashboard page
6. Build out a 2nd dashboard page
7. Additional dealerships to parse


## Run Scripts in Order
1. `python get_inventory_data.py`
2. `python move_to_prod.py`


## Low-Hanging Questions:
* Avg year that dealerships stock (Done)
* Avg miles that dealerships stock (Done)
* Avg price that dealerships stock (Done)
* Make distribution Bar Graph - Count (Done)
* Price change over time
* Make distribution change over time
* Total inventory over time
* Avg inventory on hand
    * Not sure if this one is super helpful
    * Because the types of inventory varies depending on the size of the dealership right
    * I guess if I had a better cluster of dealerships sizes and samples
* % of transmission difference

Tables:
 * Make
    * Avg price
    * Count
    * % of total
    * Avg year
    * Avg mileage
    * Count of different models
 * Most popular year + make + model stocked



## Harder Questions
* Avg length to sale
* Pick a car and see price that they are charging
