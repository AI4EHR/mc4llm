# medical_calculators/calculators/bmi/guidelines.py
from typing import Dict, Tuple

class BMIGuideline:
    def __init__(self, thresholds: Dict[str, Tuple[float, float]]):
        """
        thresholds: A dictionary mapping category names to a tuple (min, max).
        """
        self.thresholds = thresholds

    def categorize(self, bmi: float) -> str:
        for category, (min_val, max_val) in self.thresholds.items():
            if min_val <= bmi < max_val:
                return category
        return "Unknown"

# Define guideline profiles:
WHO_GUIDELINES = BMIGuideline({
    "Underweight": (0, 18.5),
    "Normal weight": (18.5, 25),
    "Overweight": (25, 30),
    "Obese": (30, float("inf")),
})

ASIAN_GUIDELINES = BMIGuideline({
    "Underweight": (0, 18.5),
    "Normal weight": (18.5, 23),
    "Overweight": (23, 27.5),
    "Obese": (27.5, float("inf")),
})
