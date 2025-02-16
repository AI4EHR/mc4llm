# medical_calculators/calculators/bmi/guidelines.py
from typing import Dict, Tuple
from medical_calculators.utils.base_guideline import (
    Guideline, 
    RangeRule
)

class BMIGuideline(Guideline):
    """BMI classification guideline."""
    
    def __init__(self, thresholds: Dict[str, Tuple[float, float]], description: str):
        bmi_rule = RangeRule(
            thresholds=thresholds,
            name="bmi"
        )
        super().__init__([bmi_rule])
        self._description = description
    
    def get_description(self) -> str:
        return self._description

# Create instances for global use
WHO_BMI_GUIDELINE = BMIGuideline(
    thresholds={
        "Underweight": (0, 18.5),
        "Normal weight": (18.5, 25),
        "Overweight": (25, 30),
        "Obese": (30, float("inf")),
    },
    description=(
        "WHO BMI Guideline:\n"
        "Standard BMI classification for general population\n"
        "\nNote: BMI has limitations and may not be suitable for athletes, "
        "pregnant individuals, or those with unusual body compositions."
    )
)

ASIAN_BMI_GUIDELINE = BMIGuideline(
    thresholds={
        "Underweight": (0, 18.5),
        "Normal weight": (18.5, 23),
        "Overweight": (23, 27.5),
        "Obese": (27.5, float("inf")),
    },
    description=(
        "Asian BMI Guideline:\n"
        "BMI classification with adjusted thresholds for Asian populations\n"
        "\nNote: These thresholds reflect the increased health risks "
        "at lower BMI values in Asian populations."
    )
)
