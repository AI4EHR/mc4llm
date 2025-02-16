# medical_calculators/calculators/bmi/guidelines.py
from typing import Dict, Tuple
from medical_calculators.utils.base_guideline import Guideline, RangeRule

class BMIGuideline(Guideline):
    """BMI classification guidelines following different standards."""
    
    def __init__(self):
        who_rule = RangeRule(
            thresholds={
                "Underweight": (0, 18.5),
                "Normal weight": (18.5, 25),
                "Overweight": (25, 30),
                "Obese": (30, float("inf")),
            },
            name="who"
        )
        
        asian_rule = RangeRule(
            thresholds={
                "Underweight": (0, 18.5),
                "Normal weight": (18.5, 23),
                "Overweight": (23, 27.5),
                "Obese": (27.5, float("inf")),
            },
            name="asian"
        )
        
        super().__init__([who_rule, asian_rule], default_rule="who")
    
    def get_description(self) -> str:
        return (
            "BMI Guidelines:\n"
            "1. WHO Standard (default): General population BMI classification\n"
            "2. Asian Standard: Adjusted thresholds for Asian populations\n"
            "\nNote: BMI has limitations and may not be suitable for athletes, "
            "pregnant individuals, or those with unusual body compositions."
        )

# Create a singleton instance for global use
DEFAULT_BMI_GUIDELINE = BMIGuideline()

# For backward compatibility
WHO_GUIDELINES = DEFAULT_BMI_GUIDELINE
ASIAN_GUIDELINES = DEFAULT_BMI_GUIDELINE
