
from os import path

from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Get the directory where this script is located
SCRIPT_DIR = path.dirname(path.abspath(__file__))

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York'
    }
    return jsonify(data)

@app.route("/churn_count", methods=['GET'])
def churn_count():
    csv_path = path.join(SCRIPT_DIR, 'data', 'Telco-Customer-Churn.csv')
    df = pd.read_csv(csv_path)
    result = list(df['Churn'].value_counts())
    return result

@app.route("/languages")
def languages():
    data = request.args
    print(data)
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
