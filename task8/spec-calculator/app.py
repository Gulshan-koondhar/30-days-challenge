from flask import Flask, request, jsonify
from main import calculate_expression
from calculator.errors import CalculatorError, InvalidExpressionError, DivisionByZeroError, UnsupportedOperationError

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or 'expression' not in data:
        return jsonify({"error": "Missing 'expression' in request body"}), 400

    expression = data['expression']
    result = calculate_expression(expression)

    if isinstance(result, str):
        # It's an error message
        if "Division by zero" in result:
            return jsonify({"error": result}), 400
        elif "Invalid expression" in result or "Mismatched parentheses" in result or "Unknown character" in result:
            return jsonify({"error": result}), 400
        elif "Unsupported operator" in result:
            return jsonify({"error": result}), 400
        else:
            # Catch-all for unexpected CalculatorErrors or other Exceptions
            return jsonify({"error": f"Internal Server Error: {result}"}), 500
    else:
        # It's a successful calculation
        return jsonify({"result": result}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
