# calculators/bmi/models.py
from typing import List
from pydantic import Field, field_validator

from medical_calculators.observation import BaseInputModel, BaseOutputModel, BaseObservation
from medical_calculators.config import DEFAULT_UNITS

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

    def get_summary(self) -> str:
        """Get a human-readable summary of the BMI calculation."""
        return f"BMI: {self.bmi:.1f} ({self.category})"
    
