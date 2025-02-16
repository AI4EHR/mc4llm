# medical_calculators/utils/base_models.py
from pydantic import BaseModel
from pint import UnitRegistry

# Create a global UnitRegistry instance.
ureg = UnitRegistry()

class Observation(BaseModel):
    value: float
    unit: str

    def to(self, target_unit: str) -> float:
        """
        Convert this observation to the specified target unit.
        """
        quantity = self.value * ureg(self.unit)
        return quantity.to(target_unit).magnitude
