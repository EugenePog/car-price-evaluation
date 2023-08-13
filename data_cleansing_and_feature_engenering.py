import pandas as pd
import numpy as np
import datetime as dt
#import click

from datetime import date

import sys

from prefect import flow, task

num_f = ['model_age', 'm_from_car_reg', 'power_kw', 'mileage_in_km']
cat_f = ['brand', 'model', 'color', 'transmission_type', 'fuel_type']
target = ['price_in_euro']
raw_data = 'data/car-price-raw-data.csv'
preprocessed_data = 'data/car-price-processed-data.parquet'
CAR_PRICE_LOW_THD, CAR_PRICE_UP_THD = 1000, 100000
CAR_MILAGE_LOW_THD, CAR_MILAGE_UP_THD = 0, 400000

@task(retries=3, retry_delay_seconds=2, name="Read raw data")
def load_data(file_name, price_lower_threshold = 500, price_upper_threshold = 500000, milage_lower_threshold = 0, milage_upper_threshold = 400000):
    #read the file to dataframe
    df = pd.read_csv(file_name)

    today = date.today()
    
    #cleansing year: non digit values and values out of range
    df = df[df['year'].apply(lambda x:x.isdigit())]
    df['year'] = df['year'].astype(int) 
    df = df[df['year'].apply(lambda x:x>=1995 and x<=int(today.year))]
    
    #registration date transformation to datatime type
    df['registration_date'] = pd.to_datetime(df['registration_date'])
    
    #remove power_kw records with NaN, types convertions
    df = df[df['power_kw'].apply(lambda x: str(x) != 'nan')]
    df['power_kw'] = df['power_kw'].astype(int)
    
    #remove records with NaN mileage
    df = df[df['mileage_in_km'].apply(lambda x: str(x) != 'nan')]
    df = df[(df['mileage_in_km'] >= milage_lower_threshold) & (df['mileage_in_km'] <= milage_upper_threshold)]
    
    #remove price records with NaN, types convertions, remove outliers
    df = df[df['price_in_euro'].apply(lambda x: str(x) != 'nan')]
    df['price_in_euro'] = df['price_in_euro'].astype(int)
    df = df[(df['price_in_euro'] >= price_lower_threshold) & (df['price_in_euro'] <= price_upper_threshold)]
    
    #remove records with NaN, types convertions for categorical features
    df['brand'] = df['brand'].astype(str)
    df['model'] = df['model'].astype(str)
    df['color'] = df['color'].astype(str)
    df['transmission_type'] = df['transmission_type'].astype(str)
    df['fuel_type'] = df['fuel_type'].astype(str)
    df = df[df['brand'].apply(lambda x: str(x) != 'nan')]
    df = df[df['model'].apply(lambda x: str(x) != 'nan')]
    df = df[df['color'].apply(lambda x: str(x) != 'nan')]
    df = df[df['transmission_type'].apply(lambda x: str(x) != 'nan')]
    df = df[df['fuel_type'].apply(lambda x: str(x) != 'nan')]
  
    return df

@task(retries=3, retry_delay_seconds=2, name="Add features to the data")
def feature_eng(df):
    today = date.today()    
    
    #calculation of model age: current year - year in years
    df['model_age'] = df['year'].apply(lambda x:int(today.year)-x)
    
    #calculation of months from gegistration till now attribute
    df['m_from_car_reg'] = df['registration_date'].apply(lambda x: (int(today.year) - x.year)*12 + int(today.month) - x.month)
    #do not take cars with registration in the future
    df = df[df['m_from_car_reg'].apply(lambda x:x>=0)]
        
    return df[cat_f+num_f+target]

#@click.command()
#@click.option(
#    "--raw_data_path",
#    default=raw_data,
#    help="Location where the raw car price data is saved"
#)
#@click.option(
#    "--preprocessed_data_path",
#    default=preprocessed_data,
#    help="Location where the resulting files will be saved"
#)
#processing and saving the data
#@task(retries=3, retry_delay_seconds=2, name="Process the data and save preprocessed data to parquet file")
def run_data_cleansing_and_feature_engenering(raw_data_path: str = raw_data, preprocessed_data_path: str = preprocessed_data):
    df1 = load_data(raw_data_path, price_lower_threshold = CAR_PRICE_LOW_THD, price_upper_threshold = CAR_PRICE_UP_THD, milage_lower_threshold = CAR_MILAGE_LOW_THD, milage_upper_threshold = CAR_MILAGE_UP_THD)
    df1 = feature_eng(df1)
    df1.to_parquet(preprocessed_data_path)

if __name__ == '__main__':
    run_data_cleansing_and_feature_engenering()