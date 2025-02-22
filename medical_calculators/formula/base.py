from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic

# Define generic type variables for input and output
InputType = TypeVar('InputType')
OutputType = TypeVar('OutputType')

class BaseFormula(Generic[InputType, OutputType], ABC):
    """Base class for all calculation formulae in the system.
    
    Type Parameters:
        InputType: The type of input parameters the formula accepts
        OutputType: The type of output the formula produces
    """
    def __init__(self, name: Optional[str] = None):
        self.name = name or "default"
    
    @abstractmethod
    def calculate(self, params: InputType) -> OutputType:
        """
        Calculate a value based on the formula's logic.
        
        Args:
            params: Input parameters required for the calculation
            
        Returns:
            The calculated value of type OutputType
            
        Raises:
            ValueError: If required parameters are missing or invalid
        """
        pass 