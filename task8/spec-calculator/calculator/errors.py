"""Custom exception classes for the calculator."""

class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass

class InvalidExpressionError(CalculatorError):
    """Raised when an expression is syntactically invalid."""
    pass

class DivisionByZeroError(CalculatorError):
    """Raised when a division by zero occurs."""
    pass

class UnsupportedOperationError(CalculatorError):
    """Raised when an unsupported operation is encountered."""
    pass