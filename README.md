# commodityPricing
**Report**: [Click here](https://drive.google.com/file/d/0B8n2hg8DJKztZHRTTi1SZDdEYkhtTmlQazdEMV9yOWd0eGtR/view)

Has a restAPI framework and the database for making requests and getting the prices for various commodities in each APMC across Maharashtra. Additionally algorithms to bring stationarity to the data and the outlier removal is also present
## Contents
* Input data
* DB schema
* RestAPICode
* Database update code
* Requirements.txt
* Figures.py to generate the plots for the various valies

## Tech stack
* Database - Mongodb
* RestAPI - Flask micro-framwork (jinja server)
* OS - Ubuntu 16.04
* Language - python

## How to run
1. Install mongoDB server and start the server 
2. Run pip  install -r requirements.txt to install all dependencies 
3. Run main.py to put all the into the database as separate groups
4. Run restAPI.py to start the server
5. Run the following commands in your browser to get the corresponding values
   * localhost:8080/actualPrices/<APMC>/<COMMODITY>
   * localhost:8080/stationaryPrices/<APMC>/<COMMODITY>


## Future work
1. Compute the fluctuation through the RestAPI commands
2. Add more sophistication to the algorithm to be able to calculate distance and quantity based models
3. Test Enviornment
4. Develop a front end GUI

