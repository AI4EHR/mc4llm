# medical_calculators/calculators/bmi/prompts.py
from pydantic import BaseModel

class CalculatorPrompt(BaseModel):
    title: str
    description: str
    ideal_for: str
    not_ideal_for: str
    usage_instructions: str

BMI_PROMPT = CalculatorPrompt(
    title="BMI Calculator",
    description="Calculates Body Mass Index (BMI) using weight and height measurements.",
    ideal_for="General population screening for weight status in adults.",
    not_ideal_for="Athletes with high muscle mass, pregnant individuals, or those with atypical body composition.",
    usage_instructions=(
        "Enter weight and height in any acceptable units (e.g., kg, lbs, m, ft). "
        "Defaults from global configuration will be used if no unit is provided. "
        "You may also specify the desired output unit for BMI (default is 'kg/m^2')."
    )
)
