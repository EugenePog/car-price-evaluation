# Car price evaluation project - Web Application

# Application description
Problem:
The Car Price Evaluation is a web application that offers a user-friendly interface for individuals looking to estimate the reasonable price for a used car. It provides a convenient and efficient way for users to assess the value of their vehicle if they intend to sell it, or to determine whether the price of a car they plan to purchase is fair. By leveraging various inputs and data points, the application aims to offer accurate and reliable price evaluations, making the car buying and selling process more transparent and informed.

Features:
- Input Data: The application allows users to input essential details about the car they wish to evaluate, including make, model, year of manufacture, mileage, condition, and any additional features or modifications. 
- Data Analysis: Utilizing a comprehensive database and sophisticated algorithms, the application processes the provided information to perform an in-depth analysis of the car's market value.
- Comparative Analysis: For users looking to sell their car, the application compares the entered data with similar cars available in the market to determine a competitive and fair selling price.
- Fair Price Assessment: For users interested in purchasing a car, the application assesses whether the listed price is reasonable based on prevailing market trends and the car's specific attributes.

Use Cases:
- Estimating Selling Price:
  A person who intends to sell their car can use the Car Price Evaluation application to input the necessary details about their vehicle. The application will then process this information and generate an estimated selling price based on prevailing market trends, the car's condition, and comparable prices of similar cars.
- Verifying Fair Purchase Price:
  A prospective car buyer can utilize the application to assess whether the listed price of a used car is reasonable and fair. By providing the car's specifications and condition, the user will receive an evaluation that helps them make an informed decision during negotiations.

The Car Price Evaluation application aims to simplify the car pricing process, empowering both sellers and buyers with valuable insights to make well-informed decisions and ensure fair transactions.

# Data description:
Collection of car offers from one of Germany's largest car sales websites, AutoScout24. 
This scraped dataset on date 24.06.2023 contains a wide range of information about car offers, 
covering a cars manufactured from 1995 to 2023.

Car features:
    Brand: The brand or manufacturer of the car.
    Model: The specific model of the car.
    Color: The color of the car's exterior.
    Registration Date: The date when the car was registered (Month/Year).
    Year of Production: The year in which the car was manufactured.
    Price in Euro: The price of the car in Euros.
    Power: The power of the car in kilowatts (kW) and horsepower (ps).
    Transmission Type: The type of transmission (e.g., automatic, manual).
    Fuel Type: The type of fuel the car requires.
    Fuel Consumption: Information about the car's fuel consumption in L/100km ang g/km.
    Mileage: The total distance traveled by the car in km.
    Offer Description: Additional description provided in the car offer.

# Peer review criteria fit
+ Cloud
    0 points: Cloud is not used, things run only locally
    2 points: The project is developed on the cloud OR uses localstack (or similar tool) OR the project is deployed to Kubernetes or similar container management platforms
    4 points: The project is developed on the cloud and IaC tools are used for provisioning the infrastructure

+ Experiment tracking and model registry
    Both experiment tracking and model registry are used

+ Workflow orchestration
    2 points: Basic workflow orchestration
    4 points: Fully deployed workflow

+ Model deployment
    The model deployment code is containerized and could be deployed to cloud or special tools for model deployment are used

- Model monitoring
    0 points: No model monitoring
    2 points: Basic model monitoring that calculates and reports metrics
    4 points: Comprehensive model monitoring that sends alerts or runs a conditional workflow (e.g. retraining, generating debugging dashboard, switching to a different model) if the defined metrics threshold is violated

+ Reproducibility
    Instructions are clear, it's easy to run the code, and it works. The versions for all the dependencies are specified.

Best practices
-    There are unit tests (1 point)
-    There is an integration test (1 point)
-    Linter and/or code formatter are used (1 point)
-    There's a Makefile (1 point)
-    There are pre-commit hooks (1 point)
-    There's a CI/CD pipeline (2 points)


# Installation instruction for users:
1. copy project from github to your local machine
2. create environment in the project directory: 
    pipenv install --python=3.10
    pipenv run pip install -r requirements.txt 
3. run environment:
    pipenv shell
4. run mlflow (with correct environment):
    mlflow ui --backend-store-uri sqlite:///mlflow.db
    mlflow is available on http://127.0.0.1:5000
5. create prefect project:
    prefect init
6. run prefect and worker in it:
    prefect server start
    prefect worker start -p car_price
    prefect is available on http://127.0.0.1:4200 
7. run application:
    python app.py
    application is available on http://127.0.0.1:5010/
8. optional. if you want to rebuild the model, run:
    python orchestrate_train.py