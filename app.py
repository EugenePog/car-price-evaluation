from flask import Flask, render_template, request, jsonify
from xgboost import XGBRegressor
import pickle
import mlflow
from mlflow.tracking import MlflowClient

app = Flask(__name__)

TRACKING_SERVER_HOST = "ec2-3-90-186-17.compute-1.amazonaws.com"
preprocessor_addition = "/artifacts/preprocessor/preprocessor.bin"
for_downloads = 'models/'
preprocessor_location = for_downloads + 'preprocessor.bin'
filter_string = "name = 'car-price-prediction-xgbregressor'"

client = MlflowClient(f"http://{TRACKING_SERVER_HOST}:5000")

def predict_car_price(brand, model, color, transmission_type, fuel_type):
    
    #getting model, registered in mlflow with name, coded in 'filter_string' and in production stage (take the 1st model in the stage, assuming that only 1 model for the given name has production stage) 
    prod_version = ''
    for ver in client.search_model_versions(filter_string=filter_string):
        if ver.current_stage == 'Production':
            prod_version = ver
            break

    #take the model by it path
    prod_version_source = prod_version.source
    price_predictor = mlflow.xgboost.load_model(prod_version_source)

    #download preprocessor locally from mlflow
    prod_version_preprocessor_source = prod_version_source[:prod_version_source.index("/artifacts")]+preprocessor_addition
    mlflow.artifacts.download_artifacts(artifact_uri=prod_version_preprocessor_source, dst_path=for_downloads)

    #open preprocessor using pickle, preprocess the input data and apply model to given data 
    with open(preprocessor_location, 'rb') as f_in:
        dv = pickle.load(f_in)

        input_dict = [{'brand': brand, 'model': model, 'color': color, 'transmission_type': transmission_type, 'fuel_type': fuel_type}]
    
        input_vect = dv.transform(input_dict)
        predicted_price = price_predictor.predict(input_vect)

        return round(predicted_price.tolist()[0], 2)

def get_models_for_brand(brand):
    return models.get(brand, [])

brands = ['alfa-romeo', 'aston-martin', 'audi', 'bentley', 'bmw', 'cadillac',
       'chevrolet', 'chrysler', 'citroen', 'dacia', 'daewoo', 'daihatsu',
       'dodge', 'ferrari', 'fiat', 'ford', 'honda', 'hyundai', 'infiniti',
       'isuzu', 'jaguar', 'jeep', 'kia', 'lada', 'lamborghini', 'lancia',
       'land-rover', 'maserati', 'mazda', 'mercedes-benz', 'mini',
       'mitsubishi', 'nissan', 'opel', 'peugeot', 'porsche', 'proton',
       'renault', 'rover', 'saab', 'seat', 'skoda', 'smart', 'ssangyong',
       'toyota', 'volkswagen', 'volvo']
models = {'alfa-romeo': ['Alfa Romeo GTV', 'Alfa Romeo 164', 'Alfa Romeo Spider', 'Alfa Romeo 145', 'Alfa Romeo 155', 'Alfa Romeo 146', 'Alfa Romeo', 'Alfa Romeo 156', 'Alfa Romeo 166', 'Alfa Romeo 147', 'Alfa Romeo Alfa 6', 'Alfa Romeo GT', 'Alfa Romeo 159', 'Alfa Romeo Brera', 'Alfa Romeo Sportwagon', 'Alfa Romeo MiTo', 'Alfa Romeo Giulietta', 'Alfa Romeo 4C', 'Alfa Romeo Giulia', 'Alfa Romeo Stelvio', 'Alfa Romeo Tonale'], 'aston-martin': ['Aston Martin DB7', 'Aston Martin Vanquish', 'Aston Martin DB9', 'Aston Martin V8', 'Aston Martin Vantage', 'Aston Martin DBS', 'Aston Martin Rapide', 'Aston Martin', 'Aston Martin Virage', 'Aston Martin DB11'], 'audi': ['Audi A4', 'Audi A6', 'Audi A8', 'Audi S8', 'Audi Cabriolet', 'Audi A3', 'Audi 80', 'Audi TT', 'Audi S6', 'Audi S3', 'Audi S4', 'Audi A2', 'Audi Allroad', 'Audi RS4', 'Audi A6 allroad', 'Audi RS6', 'Audi A5', 'Audi Q7', 'Audi QUATTRO', 'Audi S5', 'Audi R8', 'Audi TTS', 'Audi Q5', 'Audi A4 allroad', 'Audi TT RS', 'Audi A1', 'Audi A7', 'Audi RS5', 'Audi Q3', 'Audi RS3', 'Audi S7', 'Audi SQ5', 'Audi RS Q3', 'Audi', 'Audi RS7', 'Audi S1', 'Audi SQ7', 'Audi Q2', 'Audi Q8', 'Audi e-tron', 'Audi SQ8', 'Audi SQ2', 'Audi RS Q8', 'Audi Q4 e-tron', 'Audi e-tron GT', 'Audi 50', 'Audi Q8 e-tron'], 'bentley': ['Bentley Continental', 'Bentley Azure', 'Bentley Turbo R', 'Bentley Arnage', 'Bentley Continental GT', 'Bentley Flying Spur', 'Bentley Continental GTC', 'Bentley', 'Bentley Mulsanne', 'Bentley Bentayga'], 'bmw': ['BMW 320', 'BMW 540', 'BMW 520', 'BMW 318', 'BMW Z3', 'BMW 316', 'BMW 528', 'BMW 523', 'BMW 750', 'BMW 328', 'BMW M3', 'BMW Z3 M', 'BMW 725', 'BMW 525', 'BMW 740', 'BMW 323', 'BMW 728', 'BMW 735', 'BMW M5', 'BMW 730', 'BMW 550', 'BMW 840', 'BMW 325', 'BMW 535', 'BMW 330', 'BMW 530', 'BMW X5', 'BMW', 'BMW 745', 'BMW Z4', 'BMW 116', 'BMW X3', 'BMW 760', 'BMW 645', 'BMW 220', 'BMW 120', 'BMW 118', 'BMW 545', 'BMW 630', 'BMW Z4 M', 'BMW X3 M', 'BMW 335', 'BMW M6', 'BMW 130', 'BMW 650', 'BMW 635', 'BMW 123', 'BMW 125', 'BMW 135', 'BMW X6', 'BMW X1', 'BMW X6 M', 'BMW 128', 'BMW X5 M', 'BMW Active Hybrid 7', 'BMW 640', 'BMW 1er M Coupé', 'BMW 114', 'BMW M550', 'BMW 435', 'BMW 420', 'BMW 518', 'BMW 428', 'BMW i3', 'BMW M4', 'BMW 235', 'BMW 425', 'BMW X4', 'BMW 430', 'BMW 218', 'BMW i8', 'BMW 228', 'BMW M2', 'BMW 225', 'BMW 418', 'BMW Active Hybrid 3', 'BMW 216', 'BMW 340', 'BMW X4 M', 'BMW 240', 'BMW 140', 'BMW 440', 'BMW 230', 'BMW M1', 'BMW X2', 'BMW M850', 'BMW X2 M', 'BMW X7', 'BMW M8', 'BMW 850', 'BMW X7 M', 'BMW 620', 'BMW 223', 'BMW i4', 'BMW iX3', 'BMW iX', 'BMW iX1', 'BMW i5', 'BMW 214'], 'cadillac': ['Cadillac Eldorado', 'Cadillac STS', 'Cadillac Seville', 'Cadillac', 'Cadillac Escalade', 'Cadillac CTS', 'Cadillac SRX', 'Cadillac BLS', 'Cadillac ATS', 'Cadillac XT5', 'Cadillac CT6', 'Cadillac XT4', 'Cadillac XT6'], 'chevrolet': ['Chevrolet C1500', 'Chevrolet Chevy Van', 'Chevrolet Kalos', 'Chevrolet Matiz', 'Chevrolet Spark', 'Chevrolet Orlando', 'Chevrolet Captiva', 'Chevrolet Aveo', 'Chevrolet Cruze', 'Chevrolet Trax', 'Chevrolet Camaro', 'Chevrolet Corvette', 'Chevrolet Tahoe', 'Chevrolet Express', 'Chevrolet Bolt', 'Chevrolet Silverado', 'Chevrolet Suburban', 'Chevrolet Blazer', 'Chevrolet Trailblazer', 'Chevrolet Colorado', 'Chevrolet 2500'], 'chrysler': ['Chrysler Pacifica', 'Chrysler Ram Van', 'Chrysler 200'], 'citroen': ['Citroen Xantia', 'Citroen C3', 'Citroen C5', 'Citroen C4', 'Citroen C8', 'Citroen C2', 'Citroen Xsara Picasso', 'Citroen C1', 'Citroen Xsara', 'Citroen Jumper', 'Citroen Berlingo', 'Citroen C4 Picasso', 'Citroen Jumpy', 'Citroen C-Crosser', 'Citroen Grand C4 Picasso', 'Citroen C6', 'Citroen', 'Citroen C3 Picasso', 'Citroen Nemo', 'Citroen DS3', 'Citroen DS4', 'Citroen C-Zero', 'Citroen DS5', 'Citroen Grand C4 SpaceTourer', 'Citroen C4 Aircross', 'Citroen C4 Cactus', 'Citroen C4 SpaceTourer', 'Citroen Spacetourer', 'Citroen C3 Aircross', 'Citroen C-Elysée', 'Citroen C5 Aircross', 'Citroen DS', 'Citroen C5 X', 'Citroen C35', 'Citroen Ami', 'Citroen E-C4 Electric', 'Citroen E-C4 X'], 'dacia': ['Dacia Sandero', 'Dacia Logan', 'Dacia Duster', 'Dacia Lodgy', 'Dacia Dokker', 'Dacia', 'Dacia Pick Up', 'Dacia Spring', 'Dacia Jogger'], 'daewoo': ['Daewoo Espero', 'Daewoo Nubira', 'Daewoo Matiz', 'Daewoo Lanos', 'Daewoo Rezzo', 'Daewoo Kalos', 'Daewoo Tacuma', 'Daewoo Evanda', 'Daewoo Lacetti'], 'daihatsu': ['Daihatsu Cuore', 'Daihatsu Applause', 'Daihatsu Move', 'Daihatsu Terios', 'Daihatsu Sirion', 'Daihatsu YRV', 'Daihatsu Copen', 'Daihatsu Trevis', 'Daihatsu Materia', 'Daihatsu Charade'], 'dodge': ['Dodge Caliber', 'Dodge Nitro', 'Dodge Journey', 'Dodge Avenger', 'Dodge Charger', 'Dodge Durango', 'Dodge RAM', 'Dodge Challenger', 'Dodge Grand Caravan'], 'ferrari': ['Ferrari Mondial', 'Ferrari 348', 'Ferrari 456', 'Ferrari 360', 'Ferrari 612', 'Ferrari F430', 'Ferrari 575', 'Ferrari California'], 'fiat': ['Fiat Doblo', 'Fiat Punto', 'Fiat New Panda', 'Fiat Stilo', 'Fiat Panda', 'Fiat Ulysse', 'Fiat Idea', 'Fiat Grande Punto', 'Fiat Punto Evo', 'Fiat', 'Fiat Scudo', 'Fiat Multipla', 'Fiat Bravo', 'Fiat Sedici', 'Fiat 500', 'Fiat Ducato', 'Fiat 500L', 'Fiat Qubo', 'Fiat Fiorino', 'Fiat 500C', 'Fiat Linea', 'Fiat Seicento', 'Fiat Croma', 'Fiat Strada', 'Fiat Freemont', 'Fiat 500X', 'Fiat Tipo', 'Fiat Fullback', 'Fiat Talento', 'Fiat 124 Spider', 'Fiat 500e', 'Fiat 595 Abarth', 'Fiat E-Doblo'], 'ford': ['Ford Probe', 'Ford Mustang', 'Ford Windstar', 'Ford Escort', 'Ford Transit', 'Ford Transit Bus', 'Ford Focus', 'Ford Mondeo', 'Ford Fiesta', 'Ford Galaxy', 'Ford Ka/Ka+', 'Ford Fusion', 'Ford Maverick', 'Ford Streetka', 'Ford F 150', 'Ford Puma', 'Ford Focus C-Max', 'Ford Transit Connect', 'Ford Tourneo', 'Ford C-Max', 'Ford Tourneo Connect', 'Ford', 'Ford S-Max', 'Ford Ranger', 'Ford F 250', 'Ford Focus CC', 'Ford Expedition', 'Ford Crown', 'Ford Kuga', 'Ford Flex', 'Ford Grand C-Max', 'Ford Edge', 'Ford B-Max', 'Ford Transit Custom', 'Ford Tourneo Custom', 'Ford Explorer', 'Ford Tourneo Courier', 'Ford EcoSport', 'Ford Grand Tourneo', 'Ford Transit Courier', 'Ford M', 'Ford F 350', 'Ford Taurus', 'Ford Courier', 'Ford Gran Torino', 'Ford Ranger Raptor', 'Ford Mustang Mach-E', 'Ford Bronco', 'Ford E-Transit'], 'honda': ['Honda CR-V', 'Honda Accord', 'Honda Civic', 'Honda Jazz', 'Honda Insight', 'Honda Stream', 'Honda HR-V', 'Honda Odyssey', 'Honda e'], 'hyundai': ['Hyundai SANTA FE', 'Hyundai ELANTRA', 'Hyundai Matrix', 'Hyundai Terracan', 'Hyundai TUCSON', 'Hyundai SONATA', 'Hyundai H-1', 'Hyundai Getz', 'Hyundai Atos', 'Hyundai ACCENT', 'Hyundai i10', 'Hyundai i30', 'Hyundai i20', 'Hyundai', 'Hyundai iX35', 'Hyundai iX20', 'Hyundai iX55', 'Hyundai i40', 'Hyundai Genesis Coupe', 'Hyundai VELOSTER', 'Hyundai Grand Santa Fe', 'Hyundai Genesis', 'Hyundai H 350', 'Hyundai IONIQ', 'Hyundai KONA', 'Hyundai NEXO', 'Hyundai KONA Elektro', 'Hyundai BAYON', 'Hyundai IONIQ 5', 'Hyundai STARIA', 'Hyundai IONIQ 6'], 'infiniti': ['Infiniti FX', 'Infiniti G37', 'Infiniti EX35', 'Infiniti EX30', 'Infiniti M37', 'Infiniti QX30', 'Infiniti Q70', 'Infiniti EX37', 'Infiniti M30', 'Infiniti M35', 'Infiniti Q50', 'Infiniti QX70', 'Infiniti QX50', 'Infiniti Q30', 'Infiniti Q60', 'Infiniti QX60', 'Infiniti QX80'], 'isuzu': ['Isuzu Trooper', 'Isuzu D-Max', 'Isuzu'], 'jaguar': ['Jaguar XKR', 'Jaguar X-Type', 'Jaguar XF', 'Jaguar XJ', 'Jaguar XK', 'Jaguar F-Type', 'Jaguar F-Pace', 'Jaguar XE', 'Jaguar E-Pace', 'Jaguar I-Pace'], 'jeep': ['Jeep Grand Cherokee', 'Jeep Cherokee', 'Jeep Wrangler', 'Jeep Commander', 'Jeep Compass', 'Jeep Patriot', 'Jeep Renegade', 'Jeep', 'Jeep Gladiator', 'Jeep Avenger'], 'kia': ['Kia Shuma', 'Kia Sportage', 'Kia Rio', 'Kia Cerato', 'Kia Opirus', 'Kia Sorento', 'Kia Picanto', "Kia Ceed / cee'd", 'Kia Carnival', "Kia ProCeed / pro_cee'd", 'Kia Carens', 'Kia Soul', "Kia Ceed SW / cee'd SW", 'Kia', 'Kia Venga', 'Kia Optima', 'Kia Niro', 'Kia Stonic', 'Kia Stinger', 'Kia XCeed', 'Kia e-Niro', 'Kia EV6'], 'lada': ['Lada Nova', 'Lada', 'Lada Niva', 'Lada 111', 'Lada Kalina', 'Lada Priora', 'Lada Taiga', 'Lada Granta', 'Lada Urban', 'Lada Vesta', 'Lada 4x4'], 'lamborghini': ['Lamborghini Gallardo'], 'lancia': ['Lancia Dedra', 'Lancia Y', 'Lancia Delta', 'Lancia Kappa', 'Lancia Ypsilon', 'Lancia Lybra', 'Lancia ZETA', 'Lancia Thesis', 'Lancia Phedra', 'Lancia MUSA', 'Lancia Thema', 'Lancia Voyager', 'Lancia Flavia'], 'land-rover': ['Land Rover Defender', 'Land Rover Freelander', 'Land Rover Range Rover Sport', 'Land Rover Discovery', 'Land Rover Range Rover Evoque', 'Land Rover Range Rover', 'Land Rover Discovery Sport', 'Land Rover', 'Land Rover Range Rover Velar'], 'maserati': ['Maserati Ghibli', 'Maserati Quattroporte', 'Maserati 3200', 'Maserati Spyder', 'Maserati 4200', 'Maserati Coupe', 'Maserati GranSport', 'Maserati GranTurismo', 'Maserati GranCabrio', 'Maserati Levante', 'Maserati Grecale'], 'mazda': ['Mazda MX-5', 'Mazda 323', 'Mazda 3', 'Mazda 2', 'Mazda Tribute', 'Mazda 6', 'Mazda 5', 'Mazda RX-8', 'Mazda CX-7', 'Mazda', 'Mazda BT-50', 'Mazda CX-5', 'Mazda CX-3', 'Mazda CX-9', 'Mazda CX-30', 'Mazda MX-30', 'Mazda CX-60'], 'mercedes-benz': ['Mercedes-Benz SL 500', 'Mercedes-Benz E 220', 'Mercedes-Benz SL 280', 'Mercedes-Benz SL 320', 'Mercedes-Benz 200', 'Mercedes-Benz E 320', 'Mercedes-Benz G 300', 'Mercedes-Benz CL 420', 'Mercedes-Benz C 180', 'Mercedes-Benz C 200', 'Mercedes-Benz E 250', 'Mercedes-Benz G 230', 'Mercedes-Benz E 200', 'Mercedes-Benz C 220', 'Mercedes-Benz S 600', 'Mercedes-Benz C 250', 'Mercedes-Benz G 320', 'Mercedes-Benz S 500', 'Mercedes-Benz E 36 AMG', 'Mercedes-Benz', 'Mercedes-Benz SL 600', 'Mercedes-Benz S 350', 'Mercedes-Benz C 280', 'Mercedes-Benz E 420', 'Mercedes-Benz 220', 'Mercedes-Benz S 280', 'Mercedes-Benz S 300', 'Mercedes-Benz S 320', 'Mercedes-Benz Sprinter', 'Mercedes-Benz E 230', 'Mercedes-Benz 300', 'Mercedes-Benz CE 300', 'Mercedes-Benz SLK 200', 'Mercedes-Benz C 230', 'Mercedes-Benz SLK 230', 'Mercedes-Benz E 280', 'Mercedes-Benz CLK 200', 'Mercedes-Benz V 230', 'Mercedes-Benz CLK 230', 'Mercedes-Benz CL 500', 'Mercedes-Benz C 36 AMG', 'Mercedes-Benz CLK 320', 'Mercedes-Benz CL 600', 'Mercedes-Benz E 240', 'Mercedes-Benz Vito', 'Mercedes-Benz E 290', 'Mercedes-Benz A 140', 'Mercedes-Benz A 160', 'Mercedes-Benz ML 320', 'Mercedes-Benz G 500', 'Mercedes-Benz E 55 AMG', 'Mercedes-Benz C 43 AMG', 'Mercedes-Benz C 240', 'Mercedes-Benz Marco Polo', 'Mercedes-Benz G 55 AMG', 'Mercedes-Benz E 270', 'Mercedes-Benz 240', 'Mercedes-Benz ML 430', 'Mercedes-Benz S 430', 'Mercedes-Benz A 170', 'Mercedes-Benz E 300', 'Mercedes-Benz CLK 430', 'Mercedes-Benz E 430', 'Mercedes-Benz 320', 'Mercedes-Benz A 190', 'Mercedes-Benz C 320', 'Mercedes-Benz 230', 'Mercedes-Benz CLK 55 AMG', 'Mercedes-Benz V 280', 'Mercedes-Benz 500', 'Mercedes-Benz S 400', 'Mercedes-Benz SLK 320', 'Mercedes-Benz ML 270', 'Mercedes-Benz S 55 AMG', 'Mercedes-Benz V 220', 'Mercedes-Benz G 290', 'Mercedes-Benz ML 55 AMG', 'Mercedes-Benz SLK 32 AMG', 'Mercedes-Benz 600', 'Mercedes-Benz SLR', 'Mercedes-Benz SL 63 AMG', 'Mercedes-Benz G 400', 'Mercedes-Benz A 180', 'Mercedes-Benz C 32 AMG', 'Mercedes-Benz CL 200', 'Mercedes-Benz CLC', 'Mercedes-Benz V', 'Mercedes-Benz C 270', 'Mercedes-Benz ML 500', 'Mercedes-Benz CLK 240', 'Mercedes-Benz E 500', 'Mercedes-Benz Vaneo', 'Mercedes-Benz CLK 500', 'Mercedes-Benz A 210', 'Mercedes-Benz 170', 'Mercedes-Benz SL 55 AMG', 'Mercedes-Benz 180', 'Mercedes-Benz SLK', 'Mercedes-Benz G 270', 'Mercedes-Benz CLK 270', 'Mercedes-Benz CL 180', 'Mercedes-Benz ML 400', 'Mercedes-Benz SL 350', 'Mercedes-Benz CL 220', 'Mercedes-Benz E 400', 'Mercedes-Benz ML 350', 'Mercedes-Benz CL 55 AMG', 'Mercedes-Benz CE 220', 'Mercedes-Benz Viano', 'Mercedes-Benz CLK', 'Mercedes-Benz A 150', 'Mercedes-Benz A 200', 'Mercedes-Benz E 350', 'Mercedes-Benz 350', 'Mercedes-Benz SLK 350', 'Mercedes-Benz C 55 AMG', 'Mercedes-Benz E 50 AMG', 'Mercedes-Benz CLS 55 AMG', 'Mercedes-Benz CLS 350', 'Mercedes-Benz CLS 500', 'Mercedes-Benz B 170', 'Mercedes-Benz B 200', 'Mercedes-Benz B 180', 'Mercedes-Benz CLK 350', 'Mercedes-Benz SLK 280', 'Mercedes-Benz C 160', 'Mercedes-Benz SLK 55 AMG', 'Mercedes-Benz C 350', 'Mercedes-Benz B 150', 'Mercedes-Benz CLK 280', 'Mercedes-Benz SL 65 AMG', 'Mercedes-Benz CLS 320', 'Mercedes-Benz 280', 'Mercedes-Benz Vario', 'Mercedes-Benz R 500', 'Mercedes-Benz S 450', 'Mercedes-Benz ML 280', 'Mercedes-Benz R 350', 'Mercedes-Benz R 320', 'Mercedes-Benz S 65 AMG', 'Mercedes-Benz S 420', 'Mercedes-Benz E 63 AMG', 'Mercedes-Benz CL 63 AMG', 'Mercedes-Benz ML 420', 'Mercedes-Benz CLK 63 AMG', 'Mercedes-Benz CLS 63 AMG', 'Mercedes-Benz ML 63 AMG', 'Mercedes-Benz CLK 220', 'Mercedes-Benz GL 420', 'Mercedes-Benz GL 320', 'Mercedes-Benz C 300', 'Mercedes-Benz GLC 250', 'Mercedes-Benz R 280', 'Mercedes-Benz S 63 AMG', 'Mercedes-Benz R 63 AMG', 'Mercedes-Benz CL 65 AMG', 'Mercedes-Benz C 450', 'Mercedes-Benz GLK 280', 'Mercedes-Benz GLK 320', 'Mercedes-Benz G 280', 'Mercedes-Benz GL 450', 'Mercedes-Benz C 63 AMG', 'Mercedes-Benz CLS 280', 'Mercedes-Benz GLK 350', 'Mercedes-Benz GL 500', 'Mercedes-Benz SL 300', 'Mercedes-Benz GLK 220', 'Mercedes-Benz B 160', 'Mercedes-Benz GLK 300', 'Mercedes-Benz ML 450', 'Mercedes-Benz GL 350', 'Mercedes-Benz R 300', 'Mercedes-Benz CLS 300', 'Mercedes-Benz ML 300', 'Mercedes-Benz GLK 200', 'Mercedes-Benz GLK 250', 'Mercedes-Benz G 350', 'Mercedes-Benz SLK 300', 'Mercedes-Benz ML 250', 'Mercedes-Benz SLK 250', 'Mercedes-Benz CLS 250', 'Mercedes-Benz V 250', 'Mercedes-Benz E 550', 'Mercedes-Benz V 200', 'Mercedes-Benz A 250', 'Mercedes-Benz B 250', 'Mercedes-Benz A 220', 'Mercedes-Benz G 63 AMG', 'Mercedes-Benz S 550', 'Mercedes-Benz B 220', 'Mercedes-Benz S 250', 'Mercedes-Benz CLS', 'Mercedes-Benz Citan', 'Mercedes-Benz GL 63 AMG', 'Mercedes-Benz Atego', 'Mercedes-Benz CLA 180', 'Mercedes-Benz CLA 200', 'Mercedes-Benz CLA 250', 'Mercedes-Benz CLA 220', 'Mercedes-Benz A 45 AMG', 'Mercedes-Benz GLS 500', 'Mercedes-Benz CLA 45 AMG', 'Mercedes-Benz GLA 200', 'Mercedes-Benz GLA 220', 'Mercedes-Benz GLA 250', 'Mercedes-Benz GLA 45 AMG', 'Mercedes-Benz AMG GT', 'Mercedes-Benz CLS 400', 'Mercedes-Benz S 260', 'Mercedes-Benz GLS 63 AMG', 'Mercedes-Benz CL', 'Mercedes-Benz CLS 220', 'Mercedes-Benz SLS', 'Mercedes-Benz C 400', 'Mercedes-Benz GLE 63 AMG', 'Mercedes-Benz GLE 500', 'Mercedes-Benz GLE 350', 'Mercedes-Benz GLC 220', 'Mercedes-Benz GLA 180', 'Mercedes-Benz GLS 400', 'Mercedes-Benz SLC 43 AMG', 'Mercedes-Benz GLE 250', 'Mercedes-Benz GLE 400', 'Mercedes-Benz GLE 450', 'Mercedes-Benz SL 400', 'Mercedes-Benz GL 400', 'Mercedes-Benz GLE 43 AMG', 'Mercedes-Benz G', 'Mercedes-Benz G 65 AMG', 'Mercedes-Benz E 43 AMG', 'Mercedes-Benz B Electric Drive', 'Mercedes-Benz GLS 350', 'Mercedes-Benz SLC 250', 'Mercedes-Benz GLC 350', 'Mercedes-Benz SLC 200', 'Mercedes-Benz SLC 300', 'Mercedes-Benz SLC 180', 'Mercedes-Benz GLC 43 AMG', 'Mercedes-Benz GLC 300', 'Mercedes-Benz X 250', 'Mercedes-Benz 250', 'Mercedes-Benz S 560', 'Mercedes-Benz X 220', 'Mercedes-Benz GLC 63 AMG', 'Mercedes-Benz GLS 450', 'Mercedes-Benz CLS 450', 'Mercedes-Benz E 450', 'Mercedes-Benz X 350', 'Mercedes-Benz E 53 AMG', 'Mercedes-Benz CLS 53 AMG', 'Mercedes-Benz Maybach S-Klasse', 'Mercedes-Benz GLE 300', 'Mercedes-Benz GLE 53 AMG', 'Mercedes-Benz V 300', 'Mercedes-Benz A 35 AMG', 'Mercedes-Benz GLC 200', 'Mercedes-Benz GLB 250', 'Mercedes-Benz GLC 400', 'Mercedes-Benz CLA 35 AMG', 'Mercedes-Benz SL 450', 'Mercedes-Benz S 560 E', 'Mercedes-Benz EQC 400', 'Mercedes-Benz GLE 580', 'Mercedes-Benz GLB 200', 'Mercedes-Benz GLB 220', 'Mercedes-Benz GLA 35 AMG', 'Mercedes-Benz GLS 580', 'Mercedes-Benz EQA 250', 'Mercedes-Benz EQA', 'Mercedes-Benz GLB 180', 'Mercedes-Benz GLB 35 AMG', 'Mercedes-Benz EQV 300', 'Mercedes-Benz EQA 300', 'Mercedes-Benz T-Class', 'Mercedes-Benz EQS', 'Mercedes-Benz EQB 350', 'Mercedes-Benz EQA 350', 'Mercedes-Benz EQE 300', 'Mercedes-Benz EQB 300', 'Mercedes-Benz EQB 250', 'Mercedes-Benz EQE 350', 'Mercedes-Benz EQE 43', 'Mercedes-Benz EQE 500'], 'mini': ['MINI Cooper', 'MINI Cooper S', 'MINI Cooper Cabrio', 'MINI One', 'MINI Cooper S Cabrio', 'MINI One D', 'MINI One Cabrio', 'MINI Cooper D', 'MINI Cooper Clubman', 'MINI Cooper D Clubman', 'MINI', 'MINI Cooper S Clubman', 'MINI One Clubman', 'MINI John Cooper Works Clubman', 'MINI Cooper S Countryman', 'MINI John Cooper Works Cabrio', 'MINI Cooper Countryman', 'MINI Cooper SD Clubman', 'MINI One Countryman', 'MINI Cooper D Cabrio', 'MINI Cooper D Countryman', 'MINI Cooper SD', 'MINI Cooper SD Countryman', 'MINI One D Clubman', 'MINI One D Countryman', 'MINI John Cooper Works', 'MINI Cooper S Roadster', 'MINI Cooper Roadster', 'MINI Cooper SD Coupe', 'MINI Cooper SD Roadster', 'MINI Cooper SD Cabrio', 'MINI John Cooper Works Roadster', 'MINI Cooper S Paceman', 'MINI John Cooper Works Countryman', 'MINI Cooper Coupe', 'MINI Cooper Paceman', 'MINI Cooper SD Paceman', 'MINI Cooper S Coupe', 'MINI John Cooper Works Paceman', 'MINI Cooper SE Countryman', 'MINI Cooper SE'], 'mitsubishi': ['Mitsubishi Galant', 'Mitsubishi Carisma', 'Mitsubishi Space Gear', 'Mitsubishi Space Runner', 'Mitsubishi Space Star', 'Mitsubishi L200', 'Mitsubishi Grandis', 'Mitsubishi Lancer', 'Mitsubishi Colt', 'Mitsubishi Outlander', 'Mitsubishi ASX', 'Mitsubishi I-MiEV', 'Mitsubishi', 'Mitsubishi Pajero', 'Mitsubishi Eclipse Cross', 'Mitsubishi Eclipse'], 'nissan': ['Nissan Almera Tino', 'Nissan Micra', 'Nissan Serena', 'Nissan Almera', 'Nissan Primastar', 'Nissan Primera', 'Nissan Terrano', 'Nissan Navara', 'Nissan 350Z', 'Nissan', 'Nissan X-Trail', 'Nissan Note', 'Nissan Pathfinder', 'Nissan Murano', 'Nissan Qashqai', 'Nissan Patrol', 'Nissan Kubistar', 'Nissan Pixo', 'Nissan Qashqai+2', 'Nissan Pick Up', 'Nissan Tiida', 'Nissan Evalia', 'Nissan Juke', 'Nissan NV200', 'Nissan Leaf', 'Nissan NV400', 'Nissan Cabstar', 'Nissan 370Z', 'Nissan Pulsar', 'Nissan GT-R', 'Nissan E-NV200', 'Nissan NP300', 'Nissan Titan', 'Nissan NV300', 'Nissan NV250', 'Nissan Ariya', 'Nissan Townstar', 'Nissan Interstar', 'Nissan Townstar EV', 'Nissan Frontier'], 'opel': ['Opel Tigra', 'Opel Corsa', 'Opel Omega', 'Opel Astra', 'Opel Vectra', 'Opel Frontera', 'Opel Zafira', 'Opel Combo', 'Opel', 'Opel Agila', 'Opel Speedster', 'Opel Movano', 'Opel Vivaro', 'Opel Meriva', 'Opel Signum', 'Opel Antara', 'Opel GT', 'Opel Insignia', 'Opel Zafira Tourer', 'Opel Ampera', 'Opel Mokka', 'Opel Adam', 'Opel Cascada', 'Opel Mokka X', 'Opel Karl', 'Opel Corsa-e', 'Opel Grandland X', 'Opel Grandland', 'Opel Crossland X', 'Opel Crossland', 'Opel Combo Life', 'Opel Ampera-E', 'Opel Combo-e Life', 'Opel Zafira Life', 'Opel Mokka-E', 'Opel Rocks-e', 'Opel Campo', 'Opel Vivaro-e'], 'peugeot': ['Peugeot 807', 'Peugeot 307', 'Peugeot 206', 'Peugeot Partner', 'Peugeot 407', 'Peugeot 406', 'Peugeot 1007', 'Peugeot Boxer', 'Peugeot 107', 'Peugeot 207', 'Peugeot 607', 'Peugeot 308', 'Peugeot 4007', 'Peugeot', 'Peugeot Expert', 'Peugeot 3008', 'Peugeot 5008', 'Peugeot Bipper', 'Peugeot RCZ', 'Peugeot 508', 'Peugeot iOn', 'Peugeot 208', 'Peugeot 2008', 'Peugeot 108', 'Peugeot 4008', 'Peugeot Camper', 'Peugeot Traveller', 'Peugeot Rifter', 'Peugeot e-2008', 'Peugeot 408', 'Peugeot e-208'], 'porsche': ['Porsche 911', 'Porsche 993', 'Porsche Boxster', 'Porsche 996', 'Porsche Cayenne', 'Porsche Targa', 'Porsche 997', 'Porsche Carrera GT', 'Porsche Cayman', 'Porsche Panamera', 'Porsche 991', 'Porsche Macan', 'Porsche 918', 'Porsche 718', 'Porsche 992', 'Porsche', 'Porsche Taycan'], 'proton': ['Proton 316'], 'renault': ['Renault R 11', 'Renault Kangoo', 'Renault Twingo', 'Renault Master', 'Renault Scenic', 'Renault Megane', 'Renault Laguna', 'Renault Espace', 'Renault Clio', 'Renault', 'Renault Modus', 'Renault Trafic', 'Renault Grand Espace', 'Renault Grand Scenic', 'Renault Vel Satis', 'Renault Koleos', 'Renault Grand Modus', 'Renault Rapid', 'Renault Wind', 'Renault Latitude', 'Renault Twizy', 'Renault ZOE', 'Renault Captur', 'Renault Kangoo Z.E.', 'Renault Kadjar', 'Renault R 6', 'Renault Talisman', 'Renault Alpine A110', 'Renault Alaskan', 'Renault Arkana', 'Renault Express', 'Renault Austral', 'Renault Megane E-Tech'], 'rover': ['Rover 214', 'Rover MINI', 'Rover 416', 'Rover 620', 'Rover 825', 'Rover 75', 'Rover Rover', 'Rover 25', 'Rover 45', 'Rover Streetwise', 'Rover'], 'saab': ['Saab 900', 'Saab 9000', 'Saab 9-5', 'Saab 9-3', 'Saab 93', 'Saab 9-7X', 'Saab 9-4X'], 'seat': ['SEAT Ibiza', 'SEAT Toledo', 'SEAT Cordoba', 'SEAT Leon', 'SEAT Altea', 'SEAT Arosa', 'SEAT Alhambra', 'SEAT Altea XL', 'SEAT Exeo', 'SEAT Mii', 'SEAT Ateca', 'SEAT', 'SEAT Arona', 'SEAT Tarraco', 'SEAT Leon e-Hybrid'], 'skoda': ['Skoda Fabia', 'Skoda Octavia', 'Skoda Superb', 'Skoda Roomster', 'Skoda Praktik', 'Skoda Yeti', 'Skoda Citigo', 'Skoda Rapid/Spaceback', 'Skoda', 'Skoda Kodiaq', 'Skoda Karoq', 'Skoda 135', 'Skoda Scala', 'Skoda Kamiq', 'Skoda Enyaq'], 'smart': ['smart city-coupé/city-cabrio', 'smart', 'smart forTwo', 'smart roadster', 'smart forFour', 'smart brabus', 'smart smart #1'], 'ssangyong': ['SsangYong Korando', 'SsangYong REXTON', 'SsangYong Kyron', 'SsangYong Actyon', 'SsangYong Rodius', 'SsangYong Tivoli', 'SsangYong XLV', 'SsangYong MUSSO', 'SsangYong'], 'toyota': ['Toyota RAV 4', 'Toyota Corolla', 'Toyota Land Cruiser', 'Toyota Yaris', 'Toyota Corolla Verso', 'Toyota Avensis', 'Toyota Avensis Verso', 'Toyota Hiace', 'Toyota Aygo', 'Toyota Prius', 'Toyota', 'Toyota Previa', 'Toyota Auris', 'Toyota Hilux', 'Toyota Dyna', 'Toyota Camry', 'Toyota Verso', 'Toyota Urban Cruiser', 'Toyota iQ', 'Toyota Sienna', 'Toyota Verso-S', 'Toyota GT86', 'Toyota Prius+', 'Toyota Proace', 'Toyota Tacoma', 'Toyota Aygo X', 'Toyota C-HR', 'Toyota Tundra', 'Toyota Mirai', 'Toyota 4-Runner', 'Toyota Supra', 'Toyota Proace City', 'Toyota MR 2', 'Toyota Highlander', 'Toyota Yaris Cross', 'Toyota GR86', 'Toyota bZ4X', 'Toyota Corolla Cross', 'Toyota FJ Cruiser'], 'volkswagen': ['Volkswagen T4 Kombi', 'Volkswagen T4 Caravelle', 'Volkswagen T4', 'Volkswagen Polo', 'Volkswagen', 'Volkswagen Passat Variant', 'Volkswagen Golf', 'Volkswagen T4 Multivan', 'Volkswagen Corrado', 'Volkswagen Golf Cabriolet', 'Volkswagen Bus', 'Volkswagen Käfer', 'Volkswagen T4 Allstar', 'Volkswagen Vento', 'Volkswagen Golf GTI', 'Volkswagen T4 California', 'Volkswagen Passat', 'Volkswagen Golf Variant', 'Volkswagen Caddy', 'Volkswagen LT', 'Volkswagen Sharan', 'Volkswagen Beetle', 'Volkswagen Lupo', 'Volkswagen Bora', 'Volkswagen New Beetle', 'Volkswagen Polo GTI', 'Volkswagen Phaeton', 'Volkswagen Touran', 'Volkswagen T5 Multivan', 'Volkswagen Touareg', 'Volkswagen up!', 'Volkswagen T5 Transporter', 'Volkswagen Polo Sedan', 'Volkswagen Golf Plus', 'Volkswagen T5 Caravelle', 'Volkswagen Polo Cross', 'Volkswagen T5 Kombi', 'Volkswagen T5', 'Volkswagen T5 Shuttle', 'Volkswagen Jetta', 'Volkswagen Fox', 'Volkswagen T5 California', 'Volkswagen Eos', 'Volkswagen T2', 'Volkswagen Crafter', 'Volkswagen Transporter', 'Volkswagen Tiguan', 'Volkswagen Cross Golf', 'Volkswagen Cross Touran', 'Volkswagen Passat CC', 'Volkswagen Scirocco', 'Volkswagen CC', 'Volkswagen Amarok', 'Volkswagen Passat Alltrack', 'Volkswagen Golf R', 'Volkswagen Golf GTD', 'Volkswagen T6 Caravelle', 'Volkswagen Polo R WRC', 'Volkswagen Golf Sportsvan', 'Volkswagen e-up!', 'Volkswagen T6 Multivan', 'Volkswagen T6 Transporter', 'Volkswagen T6 California', 'Volkswagen T6 Kombi', 'Volkswagen Golf GTE', 'Volkswagen e-Golf', 'Volkswagen Arteon', 'Volkswagen T-Roc', 'Volkswagen Tiguan Allspace', 'Volkswagen Atlas', 'Volkswagen T-Cross', 'Volkswagen T6.1 Multivan', 'Volkswagen T6.1 California', 'Volkswagen T6.1 Caravelle', 'Volkswagen ID.3', 'Volkswagen ID.4', 'Volkswagen T6.1 Transporter', 'Volkswagen T6.1 Kombi', 'Volkswagen T7 Multivan', 'Volkswagen Taigo', 'Volkswagen Grand California', 'Volkswagen ID. Buzz', 'Volkswagen ID.5'], 'volvo': ['Volvo 850', 'Volvo V70', 'Volvo 940', 'Volvo S80', 'Volvo C70', 'Volvo V40', 'Volvo S60', 'Volvo XC90', 'Volvo V50', 'Volvo XC70', 'Volvo S40', 'Volvo C30', 'Volvo XC60', 'Volvo V60', 'Volvo V40 Cross Country', 'Volvo V60 Cross Country', 'Volvo V90', 'Volvo S90', 'Volvo V90 Cross Country', 'Volvo XC40', 'Volvo C40', 'Volvo']}
colors = ['red', 'black', 'silver', 'grey', 'white', 'beige', 'blue',
       'green', 'yellow', 'gold', 'brown', 'bronze', 'violet', 'orange']
transmission_types = ['Manual', 'Unknown', 'Automatic', 'Semi-automatic']
fuel_types = ['Petrol', 'Diesel', 'Hybrid', 'LPG', 'Other', 'CNG',
       'Diesel Hybrid', 'Electric', 'Unknown', 'Ethanol', 'Hydrogen']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json
        brand = data['brand']
        model = data['model']
        color = data['color']
        transmission_type = data['transmission_type']
        fuel_type = data['fuel_type']

        predicted_price = predict_car_price(brand, model, color, transmission_type, fuel_type)

        result = {
            'predicted_price': predicted_price
        }
        return jsonify(result)

    return render_template('index.html', brands=brands, models=models, colors=colors,
                           transmission_types=transmission_types, fuel_types=fuel_types)

#application use ports:
# - 5010 for development
# - 5011 in production inside docker container
# - 5012 in production outside docker container
if __name__ == '__main__':
    app.run(debug=True, port=5010)
