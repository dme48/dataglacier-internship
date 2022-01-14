import pickle
from flask import Flask, request, render_template

with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def render_form():
    """Renders the html containing the webapp form"""
    return render_template('simple_form.html')

@app.route('/predict', methods=['POST'])
def render_prediction():
    """Uses the user input to predict and render the result"""
    X = [float(x) for x in request.form.values()]
    prediction = round(model.predict([X])[0])
    output_text = f"The predicted age of the crab is {prediction} years."
    return render_template('simple_form.html', prediction_text=output_text)

if __name__ == "__main__":
    app = Flask(__name__)
    app.run()