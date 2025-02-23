from pydantic import Field
from pint import Quantity

from mc4llm.models.base import IOModel, convert_unit
from mc4llm.guideline import BaseGuideline
from mc4llm.rule import RangeRule
from mc4llm.formula import BaseFormula
from mc4llm.calculator import Calculator


# Define the input and output models for the calculator
class BMIInputWithUnits(IOModel):
    
    
    weight: Quantity = Field(
        ..., 
        description="Weight (supports kg, lbs, g, etc. Will be converted to kilograms)"
    )
    height: Quantity = Field(
        ..., 
        description="Height (supports m, cm, inches, etc. Will be converted to meters)"
    )

    @convert_unit("kilogram")
    def weight(cls, v):
        return v

    @convert_unit("meter")
    def height(cls, v):
        return v


class BMIOutputWithUnits(IOModel):
    bmi: float = Field(..., description="Body Mass Index")
    category: str = Field(..., description="BMI category")


# Create WHO BMI guideline instance
WHO_BMI_GUIDELINE = BaseGuideline()


# Defining the formula
class StandardBMIFormula(BaseFormula):
    """Standard BMI formula: weight (kg) / height (m)^2"""
    
    def calculate(self, weight: Quantity, height: Quantity) -> float:
        """Calculate standard BMI."""
        # The values are already converted to kg and m by the decorators
        return weight.magnitude / (height.magnitude ** 2)


# Add the formula to the guideline
WHO_BMI_GUIDELINE.formulas.add(StandardBMIFormula(name="standard"))

# Define BMI categories
who_bmi_range_rule = RangeRule(
    thresholds={
        "Underweight": (0, 18.5),
        "Normal weight": (18.5, 25),
        "Overweight": (25, 30),
        "Obese": (30, float("inf")),
    },
    name="bmi"
)

# Add the rule to the guideline
WHO_BMI_GUIDELINE.rules.add(who_bmi_range_rule)


# Defining the BMI calculator with unit conversion
class BMICalculatorWithUnits(Calculator[BMIInputWithUnits, BMIOutputWithUnits]):
    """BMI calculator implementation with unit conversion."""
    
    def calculate(self, data: BMIInputWithUnits) -> BMIOutputWithUnits:
        """Calculate BMI using the guideline's formula."""
        # Calculate BMI using guideline's standard formula
        formula = self.guideline.get_formula("standard")
        bmi_value = formula.calculate(**data.model_dump())
        
        # Get category from guideline's BMI rule
        bmi_rule = self.guideline.get_rule("bmi")
        category = bmi_rule.categorize(bmi_value)
        
        # Create output
        return BMIOutputWithUnits(bmi=bmi_value, category=category)


# Creating an instance of the Calculator
BMI_CALCULATOR_WITH_UNITS = BMICalculatorWithUnits(
    input_model=BMIInputWithUnits,
    output_model=BMIOutputWithUnits,
    guideline=WHO_BMI_GUIDELINE
)

# Example usage:
"""
# The calculator accepts various units in multiple formats:

# Using tuples (value, unit):
input_data = BMIInputWithUnits(
    weight=(150, "pound"),
    height=(170, "centimeter")
)

# Using dictionaries:
input_data = BMIInputWithUnits(
    weight={"value": 150, "unit": "pound"},
    height={"value": 170, "unit": "centimeter"}
)

# Using direct Pint Quantity objects (if you have them):
from mc4llm.models.base import ureg
input_data = BMIInputWithUnits(
    weight=ureg.Quantity(150, "pound"),
    height=ureg.Quantity(170, "centimeter")
)

result = BMI_CALCULATOR_WITH_UNITS.calculate(input_data)
print(f"BMI: {result.bmi:.1f}")
print(f"Category: {result.category}")
""" 