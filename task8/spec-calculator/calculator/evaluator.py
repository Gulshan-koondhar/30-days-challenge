"""
An evaluator for mathematical expressions in Reverse Polish Notation (RPN).
"""

from .errors import DivisionByZeroError, UnsupportedOperationError, InvalidExpressionError
from .parser import Token

class Evaluator:
    def __init__(self):
        pass

    def evaluate_rpn(self, rpn_tokens: list[Token]) -> float:
        """Evaluates a list of RPN tokens to produce a numerical result."""
        operand_stack = []

        for token in rpn_tokens:
            if token.type == 'NUMBER':
                operand_stack.append(token.value)
            elif token.type == 'OPERATOR':
                if len(operand_stack) < 2:
                    raise InvalidExpressionError("Invalid expression: not enough operands for operator")
                # Operators pop two operands, apply the operation, and push the result back.
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = self._apply_operator(operand1, operand2, token.value)
                operand_stack.append(result)

        if len(operand_stack) != 1:
            raise InvalidExpressionError("Invalid expression: too many operands")

        return operand_stack[0]

    def _apply_operator(self, operand1: float, operand2: float, operator: str) -> float:
        """Applies a given arithmetic operator to two operands."""
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2
        elif operator == '*':
            return operand1 * operand2
        elif operator == '/':
            if operand2 == 0:
                raise DivisionByZeroError("Division by zero")
            return operand1 / operand2
        else:
            raise UnsupportedOperationError(f"Unsupported operator: {operator}")

    def evaluate(self, expression_rpn: list[Token]) -> float:
        return self.evaluate_rpn(expression_rpn)