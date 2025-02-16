import pytest
from medical_calculators.calculators.bmi.models import BMIInput
from medical_calculators.calculators.bmi.calculation import calculate_bmi
from medical_calculators.calculators.bmi.formulae import StandardBMIFormula, PonderalIndex, RevisedBMIFormula
from medical_calculators.calculators.bmi.guidelines import WHO_BMI_GUIDELINE, ASIAN_BMI_GUIDELINE
from medical_calculators.utils.base_models import Observation

def test_calculate_bmi_standard():
    # Test using SI units: weight in kg, height in m.
    input_data = BMIInput(weight=70, height=1.75)
    result = calculate_bmi(
        input_data, 
        guideline="who",  # Using WHO guidelines explicitly
        formula=StandardBMIFormula(),
        output_unit="kg/m^2"
    )
    # Expected BMI ~22.86
    assert pytest.approx(result.bmi, rel=0.01) == 22.86
    assert result.category == "Normal weight"

def test_calculate_bmi_with_observation_input():
    # Test using Observation objects for input
    input_data = BMIInput(
        weight={"value": 154, "unit": "lb"},
        height={"value": 68, "unit": "in"}
    )
    result = calculate_bmi(input_data)  # Using default WHO guidelines
    # Expected BMI ~23.4
    assert pytest.approx(result.bmi, rel=0.01) == 23.4
    assert result.category == "Normal weight"

def test_calculate_bmi_default_parameters():
    # Test with minimal parameters (using defaults)
    input_data = BMIInput(weight=80, height=1.8)
    result = calculate_bmi(input_data)
    # Expected BMI ~24.69
    assert pytest.approx(result.bmi, rel=0.01) == 24.69
    assert result.category == "Normal weight"

def test_calculate_bmi_different_output_units():
    input_data = BMIInput(weight=70, height=1.75)
    # Test with lb/ft² output
    result = calculate_bmi(input_data, output_unit="lb/ft^2")
    assert pytest.approx(result.bmi, rel=0.01) == 4.68  # Approximate conversion

def test_calculate_bmi_different_formulae():
    input_data = BMIInput(weight=70, height=1.75)
    
    # Test Ponderal Index
    result_ponderal = calculate_bmi(
        input_data,
        formula=PonderalIndex()
    )
    assert pytest.approx(result_ponderal.bmi, rel=0.01) == 13.06

    # Test Revised BMI
    result_revised = calculate_bmi(
        input_data,
        formula=RevisedBMIFormula()
    )
    assert pytest.approx(result_revised.bmi, rel=0.01) == 22.46

def test_calculate_bmi_different_guidelines():
    input_data = BMIInput(weight=65, height=1.7)  # BMI ~22.49
    
    # Test with WHO guidelines
    result_who = calculate_bmi(input_data, guideline="who")
    assert result_who.category == "Normal weight"
    
    # Test with Asian guidelines
    result_asian = calculate_bmi(input_data, guideline="asian")
    assert result_asian.category == "Normal weight"
    
    # Test borderline case
    input_data_borderline = BMIInput(weight=70, height=1.7)  # BMI ~24.22
    result_borderline_who = calculate_bmi(input_data_borderline, guideline="who")
    result_borderline_asian = calculate_bmi(input_data_borderline, guideline="asian")
    assert result_borderline_who.category == "Normal weight"
    assert result_borderline_asian.category == "Overweight"

def test_calculate_bmi_edge_cases():
    # Test very low BMI
    input_data_low = BMIInput(weight=35, height=1.75)
    result_low = calculate_bmi(input_data_low)
    assert result_low.category == "Underweight"
    
    # Test very high BMI
    input_data_high = BMIInput(weight=150, height=1.75)
    result_high = calculate_bmi(input_data_high)
    assert result_high.category == "Obese"

def test_calculate_bmi_mixed_units():
    # Test mixing different units in the same calculation
    input_data = BMIInput(
        weight={"value": 70, "unit": "kg"},
        height={"value": 69, "unit": "in"}
    )
    result = calculate_bmi(input_data)
    assert pytest.approx(result.bmi, rel=0.01) == 22.74

def test_guideline_rules():
    # Test guideline rule management
    assert "bmi" in WHO_BMI_GUIDELINE.get_available_rules()
    assert "bmi" in ASIAN_BMI_GUIDELINE.get_available_rules()
    
    # Test invalid guideline type
    with pytest.raises(ValueError):
        calculate_bmi(BMIInput(weight=70, height=1.75), guideline="invalid_guideline")

def test_guideline_descriptions():
    # Test that guidelines provide meaningful descriptions
    who_description = WHO_BMI_GUIDELINE.get_description()
    asian_description = ASIAN_BMI_GUIDELINE.get_description()
    
    assert "WHO BMI Guideline" in who_description
    assert "general population" in who_description
    assert "Asian BMI Guideline" in asian_description
    assert "Asian populations" in asian_description
