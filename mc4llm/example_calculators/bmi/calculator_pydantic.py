from pydantic import Field, BaseModel

from mc4llm.guideline import BaseGuideline
from mc4llm.rule import RangeRule
from mc4llm.formula import BaseFormula
from mc4llm.calculator import Calculator


# Define the input and output models for the calculator
class BMIInput(BaseModel):
    weight: float = Field(..., description="Weight in kilograms")
    height: float = Field(..., description="Height in meters")

class BMIOutput(BaseModel):
    bmi: float = Field(..., description="Body Mass Index")
    category: str = Field(..., description="BMI category")
    
# Defining the guideline for the calculator
# Create WHO BMI guideline instance
WHO_BMI_GUIDELINE = BaseGuideline()

# Defining the formula to add to the guideline
class StandardBMIFormula(BaseFormula):
    """Standard BMI formula: weight (kg) / height (m)^2"""
    
    def calculate(self, weight: float, height: float) -> float:
        """Calculate standard BMI."""
        return weight / (height ** 2) 

# Add the formula to the guideline
WHO_BMI_GUIDELINE.formulas.add(StandardBMIFormula(name="standard"))
    
# Defining the rules for the guideline
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


# Defining the BMI calculator   
class BMICalculator(Calculator[BMIInput, BMIOutput]):
    """BMI calculator implementation."""
    
    def calculate(self, data: BMIInput) -> BMIOutput:
        """Calculate BMI using the guideline's formula."""

        # Calculate BMI using guideline's standard formula
        formula = self.guideline.get_formula("standard")
        bmi_value = formula.calculate(**data.model_dump())
        
        # Get category from guideline's BMI rule
        bmi_rule = self.guideline.get_rule("bmi")
        category = bmi_rule.categorize(bmi_value)
        
        # Create output
        return BMIOutput(bmi=bmi_value, category=category)

#Creating a instance of the Calculator
SIMPLE_WHO_BMI_CALCULATOR = BMICalculator(
    input_model=BMIInput,
    output_model=BMIOutput,
    guideline=WHO_BMI_GUIDELINE
)




