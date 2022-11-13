# Group Overview

## Project Description

#### What it does

*ForEx* is a Flask application where you can update forex rates, download a csv file with forex rates and display rates overtime in a area chart
#### Technologies used
Please see requirements.txt

## Instructions:

To run this app you need to do the following:  
1. Clone the repo to your local  
2. This app uses a postgres database. You will need to have a connection string to you database. Please read this [article](https://medium.com/@averinjr/simple-flask-apps-for-finance-part-3-d7870c4c5825) on medium make initial preparation of the database
3. To run the application you need to create environmental variables and include them into .env file. Please check [this tutorial](https://www.youtube.com/watch?v=CJjSOzb0IYs) for learning how to use the .env file. The variable you will need:  
    SECRET KEY - key from openexchangerates.org API  
    conn_string - connection string to your database  
5. Install the dependencies from requirements.txt  
6. You are ready to go
