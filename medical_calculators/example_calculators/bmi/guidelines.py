# medical_calculators/calculators/bmi/guidelines.py
from typing import Dict, Tuple
from medical_calculators.guideline import BaseGuideline
from medical_calculators.rule import RangeRule
from medical_calculators.example_calculators.bmi.formula import StandardBMIFormula

# Create WHO BMI guideline instance
WHO_BMI_GUIDELINE = BaseGuideline(description=(
    "WHO BMI Guideline:\n"
    "Standard BMI classification for general population\n"
    "\nNote: BMI has limitations and may not be suitable for athletes, "
    "pregnant individuals, or those with unusual body compositions."
))
WHO_BMI_GUIDELINE.add_rule(RangeRule(
    thresholds={
        "Underweight": (0, 18.5),
        "Normal weight": (18.5, 25),
        "Overweight": (25, 30),
        "Obese": (30, float("inf")),
    },
    name="bmi"
))
WHO_BMI_GUIDELINE.add_formula(StandardBMIFormula(name="standard"))

# Create Asian BMI guideline instance
ASIAN_BMI_GUIDELINE = BaseGuideline(description=(
    "Asian BMI Guideline:\n"
    "BMI classification with adjusted thresholds for Asian populations\n"
    "\nNote: These thresholds reflect the increased health risks "
    "at lower BMI values in Asian populations."
))
ASIAN_BMI_GUIDELINE.add_rule(RangeRule(
    thresholds={
        "Underweight": (0, 18.5),
        "Normal weight": (18.5, 23),
        "Overweight": (23, 27.5),
        "Obese": (27.5, float("inf")),
    },
    name="bmi"
))
ASIAN_BMI_GUIDELINE.add_formula(StandardBMIFormula(name="standard"))
