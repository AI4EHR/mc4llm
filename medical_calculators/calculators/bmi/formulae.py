# medical_calculators/calculators/bmi/formulae.py
from abc import ABC, abstractmethod

class BMIFormula(ABC):
    @abstractmethod
    def calculate(self, weight_kg: float, height_m: float) -> float:
        """Calculate a BMI-like index using weight in kg and height in m."""
        pass

class StandardBMIFormula(BMIFormula):
    def calculate(self, weight_kg: float, height_m: float) -> float:
        return weight_kg / (height_m ** 2)

class PonderalIndex(BMIFormula):
    def calculate(self, weight_kg: float, height_m: float) -> float:
        return weight_kg / (height_m ** 3)

class RevisedBMIFormula(BMIFormula):
    def calculate(self, weight_kg: float, height_m: float) -> float:
        return 1.3 * weight_kg / (height_m ** 2.5)
