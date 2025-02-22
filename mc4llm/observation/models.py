from typing import Union, Optional, Dict, Any, List
from pydantic import BaseModel
from abc import ABC, abstractmethod

from mc4llm.observation.base import BaseObservation

class BaseInputModel(BaseModel, ABC):
    """Abstract base class for all calculator input models."""
    
    @classmethod
    def _wrap_observation(
        cls, 
        value: Union[int, float, dict, BaseObservation], 
        default_unit: Optional[str] = None
    ) -> BaseObservation:
        """
        Wrap a value into an Observation with appropriate unit handling.
        
        Args:
            value: The value to wrap
            default_unit: The default unit to use if value is a number
            
        Returns:
            BaseObservation: The wrapped observation
            
        Raises:
            ValueError: If value cannot be wrapped into an observation
        """
        if isinstance(value, (int, float)):
            return BaseObservation(value=float(value), unit=default_unit)
        elif isinstance(value, dict):
            return BaseObservation(**value)
        elif isinstance(value, BaseObservation):
            return value
        raise ValueError(f"Cannot wrap value of type {type(value)}")
    
    @abstractmethod
    def validate_observations(self) -> None:
        """
        Validate that all observations in this input are compatible and valid.
        Should be implemented by each specific input model.
        
        Raises:
            ValueError: If observations are incompatible or invalid
        """
        pass

class BaseOutputModel(BaseModel, ABC):
    """Abstract base class for all calculator output models."""
    
    @abstractmethod
    def get_summary(self) -> str:
        """Get a human-readable summary of the output."""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the output to a dictionary format."""
        return self.model_dump()
    
