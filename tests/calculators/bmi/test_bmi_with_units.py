import pytest
from pint.errors import UndefinedUnitError
from mc4llm.example_calculators.bmi.bmi_with_units import BMIInputWithUnits, BMI_CALCULATOR_WITH_UNITS
from mc4llm.models.base import ureg

def test_bmi_calculator_pounds_feet():
    """Test BMI calculation with imperial units (pounds and feet)."""
    input_data = BMIInputWithUnits(
        weight=(154, "pound"),  # ~70 kg
        height=(5.74, "feet")   # ~1.75 m
    )
    result = BMI_CALCULATOR_WITH_UNITS.calculate(data=input_data)
    assert result.bmi == pytest.approx(22.86, rel=1e-2)
    assert result.category == "Normal weight"

def test_bmi_calculator_grams_cm():
    """Test BMI calculation with alternative metric units (grams and cm)."""
    input_data = BMIInputWithUnits(
        weight=(70000, "gram"),  # 70 kg
        height=(175, "centimeter")  # 1.75 m
    )
    result = BMI_CALCULATOR_WITH_UNITS.calculate(data=input_data)
    assert result.bmi == pytest.approx(22.86, rel=1e-2)
    assert result.category == "Normal weight"

def test_bmi_calculator_mixed_units():
    """Test BMI calculation with mixed unit systems (pounds and cm)."""
    input_data = BMIInputWithUnits(
        weight=(198, "pound"),  # ~90 kg
        height=(180, "centimeter")  # 1.8 m
    )
    result = BMI_CALCULATOR_WITH_UNITS.calculate(data=input_data)
    assert result.bmi == pytest.approx(27.78, rel=1e-2)
    assert result.category == "Overweight"

def test_bmi_calculator_with_quantity():
    """Test BMI calculation using Pint Quantity objects with non-standard units."""
    input_data = BMIInputWithUnits(
        weight=ureg.Quantity(220, "pound"),  # ~100 kg
        height=ureg.Quantity(67, "inch")  # ~1.7 m
    )
    result = BMI_CALCULATOR_WITH_UNITS.calculate(data=input_data)
    assert result.bmi == pytest.approx(34.60, rel=1e-2)
    assert result.category == "Obese"

