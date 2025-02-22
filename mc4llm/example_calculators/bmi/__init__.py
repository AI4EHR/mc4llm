"""BMI Calculator Module

Provides functionality for calculating Body Mass Index (BMI).
"""

from mc4llm.example_calculators.bmi.models import BMIInput, BMIOutput
from mc4llm.example_calculators.bmi.calculation import who_calculator, asian_calculator

__all__ = [
    "who_calculator",
    "asian_calculator",
    "BMIInput",
    "BMIOutput"
]
