# calculators/bmi/models.py
from typing import List, Optional, Dict, Tuple
from pydantic import Field, field_validator

from mc4llm.observation import BaseInputModel, BaseOutputModel, BaseObservation
from mc4llm.observation.base import ureg
from mc4llm.config import DEFAULT_UNITS
from mc4llm.guideline import BaseGuideline
from mc4llm.rule import RangeRule
from mc4llm.formula import BaseFormula
from mc4llm.calculator import Calculator


# Define the input and output models for the calculator

class BMIInput(BaseInputModel):
    weight: BaseObservation = Field(
        ..., description="Weight measurement. If provided as a number, the default unit is used."
    )
    height: BaseObservation = Field(
        ..., description="Height measurement. If provided as a number, the default unit is used."
    )

    @field_validator('weight', mode='before')
    @classmethod
    def wrap_weight(cls, v):
        return cls._wrap_observation(v, DEFAULT_UNITS["weight"])

    @field_validator('height', mode='before')
    @classmethod
    def wrap_height(cls, v):
        return cls._wrap_observation(v, DEFAULT_UNITS["height"])
    
    def validate_observations(self) -> None:
        """Validate that weight and height observations have compatible units."""
        if not self.weight.unit:
            raise ValueError("Weight must have a unit")
        if not self.height.unit:
            raise ValueError("Height must have a unit")

class BMIOutput(BaseOutputModel):
    bmi: float
    category: str
    unit: str = Field(default=DEFAULT_UNITS["bmi"])

    def get_value_in_unit(self, unit: Optional[str] = None) -> float:
        """
        Get the BMI value in the specified unit.
        
        Args:
            unit: The unit to convert to. If None, uses the current unit.
            
        Returns:
            float: The BMI value in the specified unit
        """
        if not unit or unit == self.unit:
            return self.bmi
            
        bmi_quantity = self.bmi * ureg(self.unit)
        return bmi_quantity.to(unit).magnitude

    def get_summary(self) -> str:
        """Get a human-readable summary of the BMI calculation."""
        return f"BMI: {self.bmi:.1f} {self.unit} ({self.category})"
    
# Defining the formula for the calculator
class StandardBMIFormula(BaseFormula):
    """Standard BMI formula: weight (kg) / height (m)^2"""
    
    def calculate(self, weight_kg: float, height_m: float) -> float:
        """Calculate standard BMI."""
        return weight_kg / (height_m ** 2) 
    
# Defining the rules for the calculator
who_bmi_range_rule = RangeRule(
    thresholds={
        "Underweight": (0, 18.5),
        "Normal weight": (18.5, 25),
        "Overweight": (25, 30),
        "Obese": (30, float("inf")),
    },
    name="bmi"
)

# Defining the guideline for the calculator
# Create WHO BMI guideline instance
WHO_BMI_GUIDELINE = BaseGuideline(description=(
    "WHO BMI Guideline:\n"
    "Standard BMI classification for general population\n"
    "\nNote: BMI has limitations and may not be suitable for athletes, "
    "pregnant individuals, or those with unusual body compositions."
))

# Add the rule to the guideline
WHO_BMI_GUIDELINE.rules.add(who_bmi_range_rule)

# Add the formula to the guideline
WHO_BMI_GUIDELINE.formulas.add(StandardBMIFormula(name="standard"))

# Defining the BMI calculator   
class BMICalculator(Calculator[BMIInput, BMIOutput]):
    """BMI calculator implementation."""
    
    def calculate(self, data: BMIInput) -> BMIOutput:
        """Calculate BMI using the guideline's formula."""
        # Validate input
        data.validate_observations()
        
        # Convert to calculation units
        values = {
            "weight_kg": data.weight.to("kg"),
            "height_m": data.height.to("m")
        }
        
        # Calculate BMI using guideline's standard formula
        formula = self.guideline.get_formula("standard")
        bmi_value = formula.calculate(**values)
        
        # Get category from guideline's BMI rule
        bmi_rule = self.guideline.get_rule("bmi")
        category = bmi_rule.categorize(bmi_value)
        
        # Create output
        return BMIOutput(bmi=bmi_value, category=category)


WHO_BMI_CALCULATOR = BMICalculator(
    input_model=BMIInput,
    output_model=BMIOutput,
    guideline=WHO_BMI_GUIDELINE
)




# ----------------------------- ASIAN BMI CALCULATOR -----------------------------
# Create Asian BMI guideline instance
ASIAN_BMI_GUIDELINE = BaseGuideline(description=(
    "Asian BMI Guideline:\n"
    "BMI classification with adjusted thresholds for Asian populations\n"
    "\nNote: These thresholds reflect the increased health risks "
    "at lower BMI values in Asian populations."
))
ASIAN_BMI_GUIDELINE.rules.add(RangeRule(
    thresholds={
        "Underweight": (0, 18.5),
        "Normal weight": (18.5, 23),
        "Overweight": (23, 27.5),
        "Obese": (27.5, float("inf")),
    },
    name="bmi"
))
ASIAN_BMI_GUIDELINE.formulas.add(StandardBMIFormula(name="standard"))

ASIAN_BMI_CALCULATOR = BMICalculator(
    input_model=BMIInput,
    output_model=BMIOutput,
    guideline=ASIAN_BMI_GUIDELINE
)