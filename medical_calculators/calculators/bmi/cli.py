# medical_calculators/calculators/bmi/cli.py
import sys
from medical_calculators.calculators.bmi.models import BMIInput
from medical_calculators.calculators.bmi.calculation import calculate_bmi
from medical_calculators.calculators.bmi.prompts import BMI_PROMPT
from medical_calculators.calculators.bmi.guidelines import WHO_GUIDELINES

def main():
    print(f"=== {BMI_PROMPT.title} ===")
    print(BMI_PROMPT.description)
    print("Ideal for:", BMI_PROMPT.ideal_for)
    print("Not ideal for:", BMI_PROMPT.not_ideal_for)
    print(BMI_PROMPT.usage_instructions)
    
    try:
        weight_value = float(input("Enter weight value: "))
        weight_unit = input("Enter weight unit (default kg): ").strip() or "kg"
        height_value = float(input("Enter height value: "))
        height_unit = input("Enter height unit (default m): ").strip() or "m"
        output_unit = input("Enter desired output unit for BMI (default kg/m^2): ").strip() or "kg/m^2"
    except Exception as e:
        print("Error in input:", e)
        sys.exit(1)
    
    bmi_input = BMIInput(
        weight={"value": weight_value, "unit": weight_unit},
        height={"value": height_value, "unit": height_unit}
    )
    
    result = calculate_bmi(bmi_input, guideline=WHO_GUIDELINES, output_unit=output_unit)
    print(f"\nYour BMI is: {result.bmi:.2f} ({result.category})")

if __name__ == "__main__":
    main()
