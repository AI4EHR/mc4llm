import pytest
from medical_calculators.formula.base import BaseFormula

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

def test_base_formula_interface():
    # Test that BaseFormula cannot be instantiated directly
    with pytest.raises(TypeError):
        BaseFormula()
    
    # Test that calculate method must be implemented
    class IncompleteFormula(BaseFormula):
        pass
    
    with pytest.raises(TypeError):
        IncompleteFormula()

def test_formula_calculation():
    # Test basic calculation with SimpleAdditionFormula
    add_formula = SimpleAdditionFormula()
    result = add_formula.calculate(a=5, b=3)
    assert result == 8.0
    assert isinstance(result, float)
    
    # Test with different number types
    assert add_formula.calculate(a=5.5, b=3.2) == 8.7
    assert add_formula.calculate(a=0, b=0) == 0.0
    assert add_formula.calculate(a=-1, b=1) == 0.0
    
    # Test with a different formula implementation
    mult_formula = SimpleMultiplicationFormula()
    assert mult_formula.calculate(x=4, y=3) == 12.0
    assert mult_formula.calculate(x=2.5, y=2) == 5.0
    assert mult_formula.calculate(x=0, y=5) == 0.0

def test_formula_parameter_validation():
    add_formula = SimpleAdditionFormula()
    mult_formula = SimpleMultiplicationFormula()
    
    # Test missing parameters
    with pytest.raises(ValueError):
        add_formula.calculate(a=5)  # Missing 'b'
    
    with pytest.raises(ValueError):
        add_formula.calculate(b=3)  # Missing 'a'
    
    with pytest.raises(ValueError):
        mult_formula.calculate(x=4)  # Missing 'y'
    
    # Test with wrong parameter names
    with pytest.raises(ValueError):
        add_formula.calculate(x=5, y=3)  # Wrong parameter names
    
    with pytest.raises(ValueError):
        mult_formula.calculate(a=4, b=3)  # Wrong parameter names

def test_formula_type_handling():
    add_formula = SimpleAdditionFormula()
    
    # Test with integers
    assert add_formula.calculate(a=5, b=3) == 8.0
    
    # Test with floats
    assert add_formula.calculate(a=5.5, b=3.5) == 9.0
    
    # Test with mixed types
    assert add_formula.calculate(a=5, b=3.5) == 8.5
    
    # Test with strings that can be converted to numbers
    assert add_formula.calculate(a="5", b="3") == 8.0
    
    # Test with invalid types
    with pytest.raises(TypeError):
        add_formula.calculate(a="abc", b=3)
    
    with pytest.raises(TypeError):
        add_formula.calculate(a=5, b="def") 