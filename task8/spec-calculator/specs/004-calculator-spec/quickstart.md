# Quickstart Guide: Calculator

This guide provides basic instructions on how to use the Calculator API.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install Flask
    ```

2.  **Run the API Server**:
    Navigate to the project root directory and run:
    ```bash
    python app.py
    ```
    The API will be accessible at `http://127.0.0.1:5000`.

## Usage

To calculate an expression, send a POST request to the `/calculate` endpoint with a JSON body containing the expression.

### Example Request (Successful Calculation)

```bash
curl -X POST http://127.0.0.1:5000/calculate \
-H "Content-Type: application/json" \
-d '{"expression": "2+2"}'
```

### Example Successful Response

```json
{
  "result": 4
}
```

### Example Request (Division by Zero Error)

```bash
curl -X POST http://127.0.0.1:5000/calculate \
-H "Content-Type: application/json" \
-d '{"expression": "10/0"}'
```

### Example Error Response (Division by Zero)

```json
{
  "error": "Division by zero"
}
```

### Example Request (Invalid Input Error)

```bash
curl -X POST http://127.0.0.1:5000/calculate \
-H "Content-Type: application/json" \
-d '{"expression": "2+"}'
```

### Example Error Response (Invalid Input)

```json
{
  "error": "Invalid expression: not enough operands for operator"
}
```
