import psycopg2
from sqlalchemy import create_engine
from datetime import date, timedelta
import requests
import pandas as pd
import json
from dotenv import load_dotenv
import os


########Config########################
def configure():
    load_dotenv()

configure()

conn_string = os.getenv('conn_string')

SECRET_KEY = os.getenv('SECRET_KEY')


def create_fx_table(df, base):
    fx = df[['date', 'ccy'] + [base]]
    return fx


def create_query_visual(start_date,
 end_date, currency):

    db = create_engine(conn_string)
    conn = db.connect()
    df = pd.read_sql('''

    SELECT * FROM forex_rates
    WHERE date >= {}
    AND date <= {}
    AND ccy = {};

    '''.format(start_date, end_date, currency.upper()), con=conn)
    conn.close()

    return df

def create_query_download(start_date="'2019-01-01'",
 end_date="'"+str(date.today().strftime('%Y-%m-%d'))+"'"):

	db = create_engine(conn_string)
	conn = db.connect()
	df = pd.read_sql('''

	SELECT * FROM forex_rates
	WHERE date >= {}
	AND date <= {};

	'''.format(start_date, end_date), con=conn)
	conn.close()

	return df




###########################Update rates###############################

def create_dates():
    db = create_engine(conn_string)
    conn = db.connect()
    first_date = pd.read_sql('''

    SELECT MAX(date) FROM forex_rates;

    ''', con=conn).squeeze()+timedelta(1)
    conn.close()

    last_date = date.today()-timedelta(1)
    return first_date, last_date


def generate_list_of_dates(first_date, last_date):
    """
    This function generates a list of subsequent days between two dates.
    Before runing this function you need to make these imports:
    - from datetime import date, timedelta

    OUTPUT
    dates:list - a list of of dates

    """
    dates = list()
    start_date = first_date
    end_date = last_date
    delta = timedelta(days=1)
    while start_date <= end_date:
        dates.append(start_date)
        start_date += delta

    return dates


def get_rates(dates, SECRET_KEY):
    """
    This function queries exchange rates from openexchangerates.com using API
    and returns a list of rates for the specified period
    Before running this function you will need to make these imports:
    - import requests

    INPUT:
    dates:list - a list of dates in datetime format
    SECRET_KEY:str - secret key from you API

    OUTPUT:
    rates:list - a list of dates with a json with rates with base USD

    """
    rates = list()
    for d in dates:
        URL = 'https://openexchangerates.org/api/historical/{}.json?app_id={}'.format(d.strftime('%Y-%m-%d'), SECRET_KEY)
        response = requests.get(URL)
        display = response.json()['rates']
        rates.append(display)
    return rates

def create_fx_table_upload(dates, rates):
    """
    This function converts a list of JSON files and a list of dates into a dataframe
    Before running this function you will need to make these imports:
    - import pandas as pd

    INPUT:
    dates:list - a list of of dates
    rates:list - a list of dates with a json with rates with base USD

    OUTPUT:
    fx:DataFrame - a dataframe with date, ccy, rate USD, rate EUR columns
    """
    date_list = list()
    keys = list()
    values = list()

    for i in range(len(rates)):
        for key in rates[i]:
            date_list.append(dates[i])
            keys.append(key)
            values.append(rates[i][key])
    fx = pd.DataFrame()
    fx['date'] = date_list
    fx['ccy'] = keys
    fx['rate'] = values
    df_eur = fx[fx['ccy']=='EUR']
    fx = fx.merge(df_eur[['date','rate']], on='date', how='left')
    fx['rate_eur'] = fx['rate_x']/fx['rate_y']
    fx.columns = ['date', 'ccy', 'USD', 'rate_y', 'EUR']
    fx.drop('rate_y',axis=1, inplace=True)
    fx['date'] = pd.to_datetime(fx['date'])

    return fx

def import_to_db():
    first_date, last_date = create_dates()
    if first_date >= date.today():
        pass
    else:
        dates = generate_list_of_dates(first_date, last_date)
        rates = get_rates(dates, SECRET_KEY)
        fx = create_fx_table_upload(dates, rates)

        db = create_engine(conn_string)
        conn = db.connect()
        fx.to_sql('forex_rates', con=conn, if_exists='append', index=False)
        conn.close()
