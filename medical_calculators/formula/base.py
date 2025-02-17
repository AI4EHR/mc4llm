from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseFormula(ABC):
    """Base class for all calculation formulae in the system."""
    
    @abstractmethod
    def calculate(self, **kwargs: Dict[str, Any]) -> float:
        """
        Calculate a value based on the formula's logic.
        
        Args:
            **kwargs: Input parameters required for the calculation
            
        Returns:
            float: The calculated value
            
        Raises:
            ValueError: If required parameters are missing or invalid
        """
        pass 