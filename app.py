import random
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/phase-change-diagram', methods=['GET'])
def phase_change_diagram():
    # receive pressure as a query parameter
    pressure = request.args.get('pressure', default=None, type=float)
    # need to return specific_volume_liquid and specific_volume_vapor in a JSON response
    if pressure is None:
        return jsonify({"error": "Pressure parameter is required"}), 400
    if pressure < 0:
        return jsonify({"error": "Pressure must be a non-negative value"}), 400

    return jsonify({
        "specific_volume_liquid": saturated_liquid_volume(pressure),
        "specific_volume_vapor": saturated_vapor_volume(pressure)
    }), 200, {"Content-Type": "application/json"}

def saturated_vapor_volume(pressure):
    if pressure < 0.05:
        return 30 + (0.0035 - 30) * (pressure - 0.05) / (10 - 0.05)
    else:
        return 0.0035 + (30 - 0.0035) * (pressure - 10) / (0.05 - 10)
    

def saturated_liquid_volume(pressure):
    if pressure < 0.05:
        return 0.00105 + (0.0035 - 0.00105) * (pressure - 0.05) / (10 - 0.05)
    else:
        return 0.0035 + (0.00105 - 0.0035) * (pressure - 10) / (0.05 - 10)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))