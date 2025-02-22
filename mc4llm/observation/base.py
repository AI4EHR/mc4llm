from typing import List, Optional, Any
from pydantic import BaseModel
from pint import UnitRegistry

# Create a global UnitRegistry instance
ureg = UnitRegistry()

class BaseObservation(BaseModel):
    """Base class for all observations in the system."""
    value: float
    unit: Optional[str] = None

    def to(self, target_unit: str) -> float:
        """
        Convert this observation to the specified target unit.
        
        Args:
            target_unit: The unit to convert to
            
        Returns:
            float: The converted value
            
        Raises:
            ValueError: If conversion is requested but no unit is set
        """
        if self.unit is None:
            if target_unit is not None:
                raise ValueError("Cannot convert unitless observation to a unit")
            return self.value
            
        quantity = self.value * ureg(self.unit)
        return quantity.to(target_unit).magnitude

    def is_compatible_with(self, other: 'BaseObservation') -> bool:
        """
        Check if this observation is unit-compatible with another observation.
        
        Args:
            other: Another observation to check compatibility with
            
        Returns:
            bool: True if observations are unit-compatible or both unitless
        """
        if self.unit is None and other.unit is None:
            return True
        if self.unit is None or other.unit is None:
            return False
        return ureg(self.unit).dimensionality == ureg(other.unit).dimensionality

class TimeSeriesObservation(BaseModel):
    """Container for time-series observations."""
    values: List[BaseObservation]
    timestamp: Optional[Any] = None
    metadata: Optional[dict] = None  # For additional time-series specific data 