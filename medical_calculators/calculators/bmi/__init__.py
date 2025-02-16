"""BMI Calculator Module

Provides functionality for calculating Body Mass Index (BMI).
"""

from medical_calculators.calculators.bmi.calculation import calculate_bmi
from medical_calculators.calculators.bmi.models import BMIInput, BMIOutput
from medical_calculators.calculators.bmi.formulae import BMIFormula, StandardBMIFormula
from medical_calculators.calculators.bmi.guidelines import WHO_BMI_GUIDELINE, ASIAN_BMI_GUIDELINE

__all__ = [
    "calculate_bmi",
    "BMIInput",
    "BMIOutput",
    "BMIFormula",
    "StandardBMIFormula",
    "WHO_BMI_GUIDELINE",
    "ASIAN_BMI_GUIDELINE",
]
