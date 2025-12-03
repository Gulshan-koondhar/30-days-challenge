import unittest
from main import calculate_expression
from calculator.parser import Parser, Token
from calculator.evaluator import Evaluator
from calculator.errors import InvalidExpressionError, DivisionByZeroError

class TestCalculator(unittest.TestCase):

    def test_basic_addition(self):
        self.assertEqual(calculate_expression("2+2"), 4.0)
        self.assertEqual(calculate_expression("  5 + 3  "), 8.0)

    def test_basic_subtraction(self):
        self.assertEqual(calculate_expression("5-3"), 2.0)
        self.assertEqual(calculate_expression("10 - 7"), 3.0)

    def test_basic_multiplication(self):
        self.assertEqual(calculate_expression("2*3"), 6.0)
        self.assertEqual(calculate_expression("4 * 5"), 20.0)

    def test_basic_division(self):
        self.assertEqual(calculate_expression("6/3"), 2.0)
        self.assertEqual(calculate_expression("10 / 2"), 5.0)

    def test_mixed_basic_operations(self):
        self.assertEqual(calculate_expression("2+3*4"), 14.0) # 2 + 12
        self.assertEqual(calculate_expression("10-4/2"), 8.0) # 10 - 2

    def test_division_by_zero(self):
        self.assertEqual(calculate_expression("5/0"), "Division by zero")
        self.assertEqual(calculate_expression("10 / (5 - 5)"), "Division by zero")

    def test_invalid_expression(self):
        self.assertEqual(calculate_expression("2+"), "Invalid expression: not enough operands for operator")
        self.assertEqual(calculate_expression("(2+3"), "Mismatched parentheses")
        self.assertEqual(calculate_expression("abc"), "Unknown character: a")

    def test_single_number(self):
        self.assertEqual(calculate_expression("123"), 123.0)
        self.assertEqual(calculate_expression("12.5"), 12.5)

    def test_parentheses(self):
        self.assertEqual(calculate_expression("(2+3)*4"), 20.0)
        self.assertEqual(calculate_expression("10/(5-3)"), 5.0)
        self.assertEqual(calculate_expression(" ( ( 1 + 2 ) * 3 ) / 3 "), 3.0)

    def test_floating_point_numbers(self):
        self.assertAlmostEqual(calculate_expression("1.5+2.5"), 4.0)
        self.assertAlmostEqual(calculate_expression("7.5/2.5"), 3.0)
        self.assertAlmostEqual(calculate_expression(" (1.0 + 2.0) * 3.0 / 3.0 "), 3.0)


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_tokenize_numbers_operators_parentheses(self):
        tokens = self.parser.tokenize("1+2*(3-4)/5.0")
        self.assertEqual([t.type for t in tokens], ['NUMBER', 'OPERATOR', 'NUMBER', 'OPERATOR', 'LPAREN', 'NUMBER', 'OPERATOR', 'NUMBER', 'RPAREN', 'OPERATOR', 'NUMBER'])
        self.assertEqual([t.value for t in tokens if t.type == 'NUMBER'], [1.0, 2.0, 3.0, 4.0, 5.0])

    def test_infix_to_rpn_basic(self):
        rpn = [t.value for t in self.parser.infix_to_rpn("2+3")]
        self.assertEqual(rpn, [2.0, 3.0, '+'])

    def test_infix_to_rpn_precedence(self):
        rpn = [t.value for t in self.parser.infix_to_rpn("2+3*4")]
        self.assertEqual(rpn, [2.0, 3.0, 4.0, '*', '+'])

    def test_infix_to_rpn_parentheses(self):
        rpn = [t.value for t in self.parser.infix_to_rpn("(2+3)*4")]
        self.assertEqual(rpn, [2.0, 3.0, '+', 4.0, '*'])

    def test_infix_to_rpn_complex(self):
        rpn = [t.value for t in self.parser.infix_to_rpn("10 / (5 - 3) + 2")]
        self.assertEqual(rpn, [10.0, 5.0, 3.0, '-', '/', 2.0, '+'])

    def test_infix_to_rpn_mismatched_parentheses(self):
        with self.assertRaisesRegex(InvalidExpressionError, "Mismatched parentheses"):
            self.parser.infix_to_rpn("(2+3")
        with self.assertRaisesRegex(InvalidExpressionError, "Mismatched parentheses"):
            self.parser.infix_to_rpn("2+3)")


class TestEvaluator(unittest.TestCase):

    def setUp(self):
        self.evaluator = Evaluator()
        self.parser = Parser()

    def _evaluate_expression(self, expression: str):
        rpn_tokens = self.parser.infix_to_rpn(expression)
        return self.evaluator.evaluate(rpn_tokens)

    def test_evaluate_rpn_basic(self):
        rpn_tokens = [Token('NUMBER', 2.0), Token('NUMBER', 3.0), Token('OPERATOR', '+')]
        self.assertEqual(self.evaluator.evaluate_rpn(rpn_tokens), 5.0)

    def test_evaluate_rpn_mixed(self):
        rpn_tokens = [Token('NUMBER', 2.0), Token('NUMBER', 3.0), Token('NUMBER', 4.0), Token('OPERATOR', '*'), Token('OPERATOR', '+')]
        self.assertEqual(self.evaluator.evaluate_rpn(rpn_tokens), 14.0)

    def test_evaluate_rpn_division_by_zero(self):
        rpn_tokens = [Token('NUMBER', 5.0), Token('NUMBER', 0.0), Token('OPERATOR', '/')]
        with self.assertRaisesRegex(DivisionByZeroError, "Division by zero"):
            self.evaluator.evaluate_rpn(rpn_tokens)

    def test_evaluate_from_infix_basic(self):
        self.assertEqual(self._evaluate_expression("2+2"), 4.0)

    def test_evaluate_from_infix_complex(self):
        self.assertEqual(self._evaluate_expression("10 / (5 - 3) + 2"), 7.0)

    def test_evaluate_from_infix_division_by_zero(self):
        with self.assertRaisesRegex(DivisionByZeroError, "Division by zero"):
            self._evaluate_expression("10 / (2-2)")

    def test_evaluate_from_infix_invalid_expression(self):
        with self.assertRaisesRegex(InvalidExpressionError, "Mismatched parentheses"):
            self._evaluate_expression("(2+3")
        with self.assertRaisesRegex(InvalidExpressionError, "Invalid expression: not enough operands for operator"):
            self._evaluate_expression("2+")

if __name__ == '__main__':
    unittest.main()
