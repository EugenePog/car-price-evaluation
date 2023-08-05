# Car price evaluation project - Web Application

# Application description
Problem Description:
The Car Price Evaluation web application offers a user-friendly interface for individuals looking to estimate the reasonable price for a used car. It provides a convenient and efficient way for users to assess the value of their vehicle if they intend to sell it, or to determine whether the price of a car they plan to purchase is fair. By leveraging various inputs and data points, the application aims to offer accurate and reliable price evaluations, making the car buying and selling process more transparent and informed.

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


# Installation instruction for users:
1. copy project from github to your local machine
2. create environment in the project directory: 
    pipenv install --python=3.9
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