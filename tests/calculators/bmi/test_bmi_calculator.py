import pytest
from medical_calculators.example_calculators.bmi.models import BMIInput
from medical_calculators.example_calculators.bmi.calculation import who_calculator, asian_calculator

def test_calculate_bmi_standard():
    # Test using SI units: weight in kg, height in m.
    input_data = BMIInput(weight=70, height=1.75)
    result = who_calculator.calculate(data=input_data)
    
    # Expected BMI ~22.86
    assert pytest.approx(result.bmi, rel=0.01) == 22.86
    assert result.category == "Normal weight"
    assert result.unit == "kg/m^2"

def test_calculate_bmi_with_observation_input():
    # Test using Observation objects for input
    input_data = BMIInput(
        weight={"value": 154, "unit": "lb"},
        height={"value": 68, "unit": "in"}
    )
    result = who_calculator.calculate(data=input_data)
    
    # Expected BMI ~23.4
    assert pytest.approx(result.bmi, rel=0.01) == 23.4
    assert result.category == "Normal weight"

def test_calculate_bmi_unit_conversion():
    input_data = BMIInput(weight=70, height=1.75)
    result = who_calculator.calculate(data=input_data)
    
    # Test converting to lb/ft²
    bmi_lb_ft2 = result.get_value_in_unit("lb/ft^2")
    assert pytest.approx(bmi_lb_ft2, rel=0.01) == 4.68

def test_calculate_bmi_edge_cases():
    # Test very low BMI
    input_data_low = BMIInput(weight=35, height=1.75)
    result_low = who_calculator.calculate(data=input_data_low)
    assert result_low.category == "Underweight"
    
    # Test very high BMI
    input_data_high = BMIInput(weight=150, height=1.75)
    result_high = who_calculator.calculate(data=input_data_high)
    assert result_high.category == "Obese"

def test_calculate_bmi_mixed_units():
    # Test mixing different units in the same calculation
    input_data = BMIInput(
        weight={"value": 70, "unit": "kg"},
        height={"value": 69, "unit": "in"}
    )
    result = who_calculator.calculate(data=input_data)
    assert pytest.approx(result.bmi, rel=0.01) == 22.74

def test_bmi_guidelines_comparison():
    input_data = BMIInput(weight=65, height=1.7)  # BMI ~22.49
    
    # Test with WHO guidelines
    result_who = who_calculator.calculate(data=input_data)
    assert result_who.category == "Normal weight"
    
    # Test with Asian guidelines
    result_asian = asian_calculator.calculate(data=input_data)
    assert result_asian.category == "Normal weight"
    
    # Test borderline case
    input_data_borderline = BMIInput(weight=70, height=1.7)  # BMI ~24.22
    result_borderline_who = who_calculator.calculate(data=input_data_borderline)
    result_borderline_asian = asian_calculator.calculate(data=input_data_borderline)
    assert result_borderline_who.category == "Normal weight"
    assert result_borderline_asian.category == "Overweight"

def test_bmi_input_validation():
    # Test that unitless observations are rejected
    with pytest.raises(ValueError):
        BMIInput(
            weight={"value": 70, "unit": None},
            height={"value": 1.75, "unit": "m"}
        ).validate_observations()
    
    with pytest.raises(ValueError):
        BMIInput(
            weight={"value": 70, "unit": "kg"},
            height={"value": 1.75, "unit": None}
        ).validate_observations()

def test_bmi_output_formatting():
    input_data = BMIInput(weight=70, height=1.75)
    result = who_calculator.calculate(data=input_data)
    
    # Test summary formatting
    summary = result.get_summary()
    assert summary == f"BMI: {result.bmi:.1f} {result.unit} ({result.category})"

