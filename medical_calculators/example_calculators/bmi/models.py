# calculators/bmi/models.py
from typing import List, Optional
from pydantic import Field, field_validator

from medical_calculators.observation import BaseInputModel, BaseOutputModel, BaseObservation
from medical_calculators.observation.base import ureg
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
    
