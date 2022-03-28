
## Next Steps:
1. Script to move data in staging to production & wiping staging
    - Done
2. Build out data validations when parsing dealerships
    - If len of each data col is different it's not valid
    - If not valid: 
        - Do not append the data to inventory_staging
        - Add to a table in cars.db that logs what the error was
    - Else:
        - Add to inventory_staging
3. Start working on dash
4. Build out the main dashboard page
5. Build out a 2nd dashboard page
6. Additional dealerships to parse




## Low-Hanging Questions:
* Avg year that dealerships stock
* Avg miles that dealerships stock
* Make distribution
* Avg price that dealerships stock
* Avg price per make that they stock
* Price change over time
* Make distribution change over time
* Total inventory over time
* Avg inventory on hand
    * Not sure if this one is super helpful
    * Because the types of inventory varies depending on the size of the dealership right
    * I guess if I had a better cluster of dealerships sizes and samples
* % of transmission difference


## Harder Questions
* Avg length to sale
* Pick a car and see price that they are charging
