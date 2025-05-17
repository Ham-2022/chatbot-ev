import random
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/vehicle_data', methods=['GET'])
def get_vehicle_data():
    data = {
        'voltage': round(random.uniform(3.5, 4.2), 2),
        'current': round(random.uniform(0.5, 2.0), 2),
        'temperature': round(random.uniform(15, 45), 1),
        'state_of_charge': round(random.uniform(50, 100), 1),
        'state_of_health': round(random.uniform(80, 100), 1)
    }
    return jsonify(data)
# mock_api.py (Placeholder for future Azure API integration)
def call_qna_maker(question):
    # Placeholder for calling Azure QnA Maker API
    return "This is a mock response from the Azure QnA Maker."

def azure_speech_to_text():
    # Placeholder for Azure Speech-to-Text API
    return "Simulated speech input."

def azure_text_to_speech(response):
    # Placeholder for Azure Text-to-Speech API
    print(f"Azure Speaking: {response}")

if __name__ == '__main__':
    app.run(debug=True)
