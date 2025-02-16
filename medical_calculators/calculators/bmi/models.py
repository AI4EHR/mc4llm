# calculators/bmi/models.py
from pydantic import BaseModel, Field, field_validator
from medical_calculators.utils.base_models import Observation
from medical_calculators.config import DEFAULT_UNITS

class BMIInput(BaseModel):
    weight: Observation = Field(
        ..., description="Weight measurement. If provided as a number, the default unit is used."
    )
    height: Observation = Field(
        ..., description="Height measurement. If provided as a number, the default unit is used."
    )

    @field_validator('weight', mode='before')
    @classmethod
    def wrap_weight(cls, v):
        # If a plain number is provided, wrap it into an Observation using the default weight unit.
        if isinstance(v, (int, float)):
            from medical_calculators.config import DEFAULT_UNITS
            return {"value": v, "unit": DEFAULT_UNITS["weight"]}
        return v

    @field_validator('height', mode='before')
    @classmethod
    def wrap_height(cls, v):
        # If a plain number is provided, wrap it into an Observation using the default height unit.
        if isinstance(v, (int, float)):
            from medical_calculators.config import DEFAULT_UNITS
            return {"value": v, "unit": DEFAULT_UNITS["height"]}
        return v

class BMIOutput(BaseModel):
    bmi: float
    category: str
