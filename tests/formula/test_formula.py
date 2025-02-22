import pytest
from mc4llm.formula.base import BaseFormula
from tests.helpers.formula import SimpleAdditionFormula, SimpleMultiplicationFormula

def test_formula_name():
    # Test default name
    formula = SimpleAdditionFormula()
    assert formula.name == "default"
    
    # Test custom name
    named_formula = SimpleAdditionFormula(name="custom")
    assert named_formula.name == "custom"

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
    formula = SimpleAdditionFormula()
    
    # Test valid calculation
    assert formula.calculate(a=1, b=2) == 3
    assert formula.calculate(a="1", b="2") == 3  # String inputs should work
    
    # Test missing parameters
    with pytest.raises(ValueError):
        formula.calculate(a=1)  # Missing b
    with pytest.raises(ValueError):
        formula.calculate(b=2)  # Missing a
    
    # Test invalid parameters
    with pytest.raises(TypeError):
        formula.calculate(a="invalid", b=2)
    with pytest.raises(TypeError):
        formula.calculate(a=1, b="invalid")

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