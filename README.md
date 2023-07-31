# car-price-evaluation
The service Car price evaluation offers persons a web page with inputs that helpes to make evaluation of the reasonable price for used car.
Use cases:
- a person wants to estimate price for the car that he wants to sell
- a person wants to check if the price for the car he wants to buy is fair

Instruction for linux users:
1. copy project from github to your local machine
2. create environment in the project directory: 
    pipenv install --python=3.9
    pipenv run pip install -r requirements.txt 
3. run environment:
    pipenv shell
4. run mlflow (with correct environment):
    mlflow ui --backend-store-uri sqlite:///mlflow.db
    mlflow is awailable on http://127.0.0.1:5000
5. create prefect project:
    prefect init
6. run prefect and worker in it:
    prefect server start
    prefect worker start -p car_price
    prefect is awailable on http://127.0.0.1:4200 
7. run application:
    python app.py
    application is awailable on http://127.0.0.1:5010/
8. optional. if you want to rebuild the model, run:
    python orchestrate_train.py