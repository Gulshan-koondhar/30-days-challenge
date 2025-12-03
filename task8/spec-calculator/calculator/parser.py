"""
A parser for mathematical expressions.
Converts infix expressions to Reverse Polish Notation (RPN).
"""

from .errors import InvalidExpressionError

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Parser:
    def __init__(self):
        self.operators = {
            '+': {'precedence': 1, 'associativity': 'left'},
            '-': {'precedence': 1, 'associativity': 'left'},
            '*': {'precedence': 2, 'associativity': 'left'},
            '/': {'precedence': 2, 'associativity': 'left'},
        }

    def tokenize(self, expression: str) -> list[Token]:
        """Converts an infix expression string into a list of tokens."""
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isspace():
                i += 1
                continue
            elif char.isdigit() or (char == '.' and i + 1 < len(expression) and expression[i+1].isdigit()):
                # Handle numbers (integers and floats)
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(Token('NUMBER', float(expression[i:j])))
                i = j
                continue
            elif char in self.operators:
                tokens.append(Token('OPERATOR', char))
            elif char == '(':
                tokens.append(Token('LPAREN', char))
            elif char == ')':
                tokens.append(Token('RPAREN', char))
            else:
                raise InvalidExpressionError(f"Unknown character: {char}")
            i += 1
        return tokens

    def infix_to_rpn(self, expression: str) -> list[Token]:
        """Converts an infix expression to Reverse Polish Notation (RPN) using the Shunting-Yard algorithm."""
        tokens = self.tokenize(expression)
        output_queue = []    # Stores the RPN output
        operator_stack = []  # Stores operators and parentheses

        for token in tokens:
            if token.type == 'NUMBER':
                output_queue.append(token)
            elif token.type == 'OPERATOR':
                # Pop operators from stack to output queue based on precedence and associativity
                while (operator_stack and operator_stack[-1].type == 'OPERATOR' and
                       ((self.operators[token.value]['associativity'] == 'left' and
                         self.operators[token.value]['precedence'] <= self.operators[operator_stack[-1].value]['precedence']) or
                        (self.operators[token.value]['associativity'] == 'right' and
                         self.operators[token.value]['precedence'] < self.operators[operator_stack[-1].value]['precedence']))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token.type == 'LPAREN':
                operator_stack.append(token)
            elif token.type == 'RPAREN':
                # Pop operators until a left parenthesis is found
                while operator_stack and operator_stack[-1].type != 'LPAREN':
                    output_queue.append(operator_stack.pop())
                if not operator_stack or operator_stack[-1].type != 'LPAREN':
                    raise InvalidExpressionError("Mismatched parentheses")
                operator_stack.pop() # Discard the left parenthesis
        
        # Pop any remaining operators from the stack to the output queue
        while operator_stack:
            if operator_stack[-1].type == 'LPAREN':
                raise InvalidExpressionError("Mismatched parentheses") # Mismatched left parenthesis
            output_queue.append(operator_stack.pop())

        return output_queue

    def parse(self, expression: str):
        # For this stage, we are returning RPN. In later stages, this could build an AST.
        return self.infix_to_rpn(expression)