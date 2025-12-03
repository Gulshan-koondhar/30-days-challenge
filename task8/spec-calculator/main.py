from calculator.parser import Parser, InvalidExpressionError
from calculator.evaluator import Evaluator, DivisionByZeroError, UnsupportedOperationError
from calculator.errors import CalculatorError

def calculate_expression(expression: str) -> float | str:
    parser = Parser()
    evaluator = Evaluator()
    try:
        rpn_tokens = parser.parse(expression)
        result = evaluator.evaluate(rpn_tokens)
        return result
    except (InvalidExpressionError, DivisionByZeroError, UnsupportedOperationError) as e:
        return str(e)
    except CalculatorError as e:
        return f"An unexpected calculator error occurred: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    while True:
        user_input = input("Enter expression (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        if not user_input.strip():
            print("Please enter an expression.")
            continue

        result = calculate_expression(user_input)
        print(f"Result: {result}")