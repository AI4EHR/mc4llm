# calculators/bmi/calculation.py
from mc4llm.calculator import Calculator
from mc4llm.example_calculators.bmi.models import BMIInput, BMIOutput
from mc4llm.example_calculators.bmi.guidelines import WHO_BMI_GUIDELINE, ASIAN_BMI_GUIDELINE
from mc4llm.observation.base import ureg

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

# Create calculator instances with different guidelines
who_calculator = BMICalculator(
    input_model=BMIInput,
    output_model=BMIOutput,
    guideline=WHO_BMI_GUIDELINE
)

asian_calculator = BMICalculator(
    input_model=BMIInput,
    output_model=BMIOutput,
    guideline=ASIAN_BMI_GUIDELINE
)
