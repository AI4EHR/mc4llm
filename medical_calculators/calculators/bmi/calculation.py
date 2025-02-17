# calculators/bmi/calculation.py
from medical_calculators.calculators.bmi.models import BMIInput, BMIOutput
from medical_calculators.formula import BaseFormula
from medical_calculators.calculators.bmi.formulae import StandardBMIFormula
from medical_calculators.calculators.bmi.guidelines import WHO_BMI_GUIDELINE, ASIAN_BMI_GUIDELINE
from medical_calculators.observation.base import ureg
from medical_calculators.config import DEFAULT_UNITS
from typing import Optional, Union

def calculate_bmi(
    data: BMIInput,
    guideline: Union[str, None] = "who",
    formula: BaseFormula = StandardBMIFormula(),
    output_unit: str = DEFAULT_UNITS["bmi"]
) -> BMIOutput:
    # Convert input weight and height to SI units.
    weight_kg = data.weight.to("kg")
    height_m = data.height.to("m")
    
    # Calculate index using the chosen formula.
    bmi_value = formula.calculate(weight_kg=weight_kg, height_m=height_m)
    
    # Convert the BMI value to the user-specified output unit.
    if output_unit != "kg/m^2":
        bmi_quantity = bmi_value * ureg("kg/m^2")
        bmi_converted = bmi_quantity.to(output_unit).magnitude
    else:
        bmi_converted = bmi_value

    # Categorize using the appropriate guideline and rule
    if guideline == "asian":
        category = ASIAN_BMI_GUIDELINE.get_rule("bmi").categorize(bmi_value)
    elif guideline == "who" or guideline is None:
        category = WHO_BMI_GUIDELINE.get_rule("bmi").categorize(bmi_value)
    else:
        raise ValueError(f"Unknown guideline type: {guideline}. Use 'who' or 'asian'.")
    
    return BMIOutput(bmi=bmi_converted, category=category)
