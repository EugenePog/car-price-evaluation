import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics

from sklearn.feature_extraction import DictVectorizer

from xgboost import XGBRegressor
import pickle
from sklearn.metrics import accuracy_score

from prefect import flow, task

num_f = ['model_age', 'm_from_car_reg', 'power_kw', 'mileage_in_km']
cat_f = ['brand', 'model', 'color', 'transmission_type', 'fuel_type']
target = ['price_in_euro']
preprocessed_data = 'data/car-price-processed-data.parquet'
model_location = 'models/xgb_regressor.bin'
TEST_SIZE = 0.2

#@task(retries=3, retry_delay_seconds=2, name="Read preprocessed data")
def data_load(data_path):
    #loading the data from file
    df = pd.read_parquet(data_path)
    
    #separation of the data on train and test datasets
    X_train, X_test, Y_train, Y_test = train_test_split(df[num_f+cat_f], df[target].values, test_size=TEST_SIZE, random_state=0)

    return X_train, X_test, Y_train, Y_test

@task(log_prints=True, name="Train the model")
def run_model_train():
     
    #loading of train and test datasets 
    X_train, X_test, Y_train, Y_test = data_load(preprocessed_data)
        
    #creating dummy variables for X_train
    X_train[cat_f] = X_train[cat_f].astype(str)
    train_dict = X_train[cat_f].to_dict(orient = 'records')

    dv = DictVectorizer()
    X_train_vect = dv.fit_transform(train_dict)

    #the same for X_test
    X_test[cat_f] = X_test[cat_f].astype(str)
    test_dict = X_test[cat_f].to_dict(orient = 'records')
    X_test_vect = dv.transform(test_dict)

    # fit model on training data
    model = XGBRegressor()
    model.fit(X_train_vect, Y_train)

    # make predictions for test data
    Y_pred_on_train = model.predict(X_train_vect)
    # evaluate predictions
    RSME_on_train = metrics.mean_squared_error(Y_train, Y_pred_on_train, squared = False)

    # make predictions for test data
    Y_pred_on_test = model.predict(X_test_vect)
    # evaluate predictions
    RSME_on_test = metrics.mean_squared_error(Y_test, Y_pred_on_test, squared = False)

    #logging metrics to mlflow
    #mlflow.log_metric('rmse_on_train_dataset', RSME_on_train)
    #mlflow.log_metric('rmse_on_test_dataset', RSME_on_test)

    #save the model
    with open(model_location, 'wb') as f_out:
        pickle.dump((dv, model),f_out)

if __name__ == '__main__':
    run_model_train()