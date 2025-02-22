"""Formula test helper classes."""
from mc4llm.formula.base import BaseFormula

class HelperFormula(BaseFormula):
    """A simple formula that multiplies a value by 2 for testing."""
    def calculate(self, value: float) -> float:
        return value * 2

class SimpleAdditionFormula(BaseFormula):
    """A simple formula that adds two numbers for testing."""
    def calculate(self, **kwargs) -> float:
        if 'a' not in kwargs or 'b' not in kwargs:
            raise ValueError("Both 'a' and 'b' parameters are required")
        try:
            a = float(kwargs['a'])
            b = float(kwargs['b'])
            return a + b
        except (ValueError, TypeError):
            raise TypeError("Parameters must be numeric or convertible to numeric")

class SimpleMultiplicationFormula(BaseFormula):
    """A simple formula that multiplies two numbers for testing."""
    def calculate(self, **kwargs) -> float:
        if 'x' not in kwargs or 'y' not in kwargs:
            raise ValueError("Both 'x' and 'y' parameters are required")
        try:
            x = float(kwargs['x'])
            y = float(kwargs['y'])
            return x * y
        except (ValueError, TypeError):
            raise TypeError("Parameters must be numeric or convertible to numeric")