# calculators/bmi/calculation.py
from medical_calculators.calculators.bmi.models import BMIInput, BMIOutput
from medical_calculators.calculators.bmi.formulae import BMIFormula, StandardBMIFormula
from medical_calculators.calculators.bmi.guidelines import BMIGuideline, WHO_GUIDELINES
from medical_calculators.utils.base_models import ureg
from medical_calculators.config import DEFAULT_UNITS

def calculate_bmi(
    data: BMIInput,
    guideline: BMIGuideline = WHO_GUIDELINES,
    formula: BMIFormula = StandardBMIFormula(),
    output_unit: str = DEFAULT_UNITS["bmi"]
) -> BMIOutput:
    # Convert input weight and height to SI units.
    weight_kg = data.weight.to("kg")
    height_m = data.height.to("m")
    
    # Calculate index using the chosen formula.
    bmi_value = formula.calculate(weight_kg, height_m)
    
    # Convert the BMI value to the user-specified output unit.
    if output_unit != "kg/m^2":
        bmi_quantity = bmi_value * ureg("kg/m^2")
        bmi_converted = bmi_quantity.to(output_unit).magnitude
    else:
        bmi_converted = bmi_value

    # Categorize using the guideline (e.g. WHO_GUIDELINES).
    category = guideline.categorize(bmi_value)
    
    return BMIOutput(bmi=bmi_converted, category=category)
