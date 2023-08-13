from data_cleansing_and_feature_engenering import run_data_cleansing_and_feature_engenering
from model_train import run_model_train
import mlflow
from prefect import flow, task

# public DNS of the EC2 instance
TRACKING_SERVER_HOST = "ec2-3-90-186-17.compute-1.amazonaws.com" 

@flow
def main_flow() -> None:
    """The main training pipeline"""

    #setting up mlflow 
    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
    mlflow.set_experiment('car-price-prediction-xgbregressor-1')    

    # Load and transform the data
    run_data_cleansing_and_feature_engenering()

    # Train  
    run_model_train()

    #Send message OK
    #send_message_task('ok')

if __name__ == "__main__":
    main_flow()