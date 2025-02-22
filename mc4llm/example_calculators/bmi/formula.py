from mc4llm.formula import BaseFormula

class StandardBMIFormula(BaseFormula):
    """Standard BMI formula: weight (kg) / height (m)^2"""
    
    def calculate(self, weight_kg: float, height_m: float) -> float:
        """Calculate standard BMI."""
        return weight_kg / (height_m ** 2) 