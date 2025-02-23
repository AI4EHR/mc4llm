import pytest
from mc4llm.example_calculators.bmi.calculator_pydantic import BMIInput, SIMPLE_WHO_BMI_CALCULATOR

def test_bmi_calculator_standard():
    input_data = BMIInput(weight=70, height=1.75)
    result = SIMPLE_WHO_BMI_CALCULATOR.calculate(data=input_data)
    assert result.bmi == pytest.approx(22.86, rel=1e-2)
    assert result.category == "Normal weight"

def test_bmi_calculator_underweight():
    input_data = BMIInput(weight=45, height=1.70)
    result = SIMPLE_WHO_BMI_CALCULATOR.calculate(data=input_data)
    assert result.bmi == pytest.approx(15.57, rel=1e-2)
    assert result.category == "Underweight"

def test_bmi_calculator_overweight():
    input_data = BMIInput(weight=85, height=1.75)
    result = SIMPLE_WHO_BMI_CALCULATOR.calculate(data=input_data)
    assert result.bmi == pytest.approx(27.76, rel=1e-2)
    assert result.category == "Overweight"

def test_bmi_calculator_obese():
    input_data = BMIInput(weight=100, height=1.70)
    result = SIMPLE_WHO_BMI_CALCULATOR.calculate(data=input_data)
    assert result.bmi == pytest.approx(34.60, rel=1e-2)
    assert result.category == "Obese"

def test_bmi_calculator_boundary_cases():
    # Test at the boundary of underweight/normal (18.5)
    input_data = BMIInput(weight=56.6, height=1.75)
    result = SIMPLE_WHO_BMI_CALCULATOR.calculate(data=input_data)
    assert result.bmi == pytest.approx(18.48, rel=0.02)
    assert result.category == "Underweight"

    # Test at the boundary of normal/overweight (25.0)
    input_data = BMIInput(weight=76.5, height=1.75)
    result = SIMPLE_WHO_BMI_CALCULATOR.calculate(data=input_data)
    assert result.bmi == pytest.approx(24.97, rel=0.02)
    assert result.category == "Normal weight"

    # Test at the boundary of overweight/obese (30.0)
    input_data = BMIInput(weight=91.8, height=1.75)
    result = SIMPLE_WHO_BMI_CALCULATOR.calculate(data=input_data)
    assert result.bmi == pytest.approx(29.97, rel=1e-2)
    assert result.category == "Overweight"

