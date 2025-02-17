from medical_calculators.formula.base import BaseFormula

class StandardBMIFormula(BaseFormula):
    """Standard BMI formula: weight (kg) / height (m)²"""
    
    def calculate(self, weight_kg: float, height_m: float, **kwargs) -> float:
        """
        Calculate BMI using the standard formula.
        
        Args:
            weight_kg: Weight in kilograms
            height_m: Height in meters
            **kwargs: Additional parameters (not used)
            
        Returns:
            float: BMI value in kg/m²
            
        Raises:
            ValueError: If height is zero
        """
        if height_m <= 0:
            raise ValueError("Height must be greater than zero")
        if weight_kg < 0:
            raise ValueError("Weight cannot be negative")
            
        return weight_kg / (height_m ** 2) 