from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data for the dropdown options
# (Assuming you have the relevant price prediction logic)
def predict_car_price(brand, model, color, transmission_type, fuel_type):
    # Your price prediction logic goes here
    # For demonstration purposes, we're using a simple fixed price.
    return 25000

brands = ['Toyota', 'Honda', 'Ford', 'Chevrolet']
models = {'Toyota': ['Camry', 'Corolla', 'RAV4'],
          'Honda': ['Civic', 'Accord', 'CR-V'],
          'Ford': ['F-150', 'Mustang', 'Escape'],
          'Chevrolet': ['Silverado', 'Camaro', 'Equinox']}
colors = ['Red', 'Blue', 'Green', 'Black', 'White']
transmission_types = ['Automatic', 'Manual']
fuel_types = ['Gasoline', 'Diesel', 'Electric']

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

if __name__ == '__main__':
    app.run(debug=True, port=5010)
