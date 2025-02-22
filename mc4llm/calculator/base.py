from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from mc4llm.observation import BaseInputModel, BaseOutputModel
from mc4llm.guideline import BaseGuideline

InputT = TypeVar('InputT', bound=BaseInputModel)
OutputT = TypeVar('OutputT', bound=BaseOutputModel)

class Calculator(Generic[InputT, OutputT], ABC):
    """Base class for all medical calculators."""
    
    def __init__(
        self,
        input_model: type[InputT],
        output_model: type[OutputT],
        guideline: BaseGuideline
    ):
        """
        Initialize the calculator with its models and guideline.
        
        Args:
            input_model: The input model class
            output_model: The output model class
            guideline: The guideline to use for calculation and categorization
        """
        self.input_model = input_model
        self.output_model = output_model
        self.guideline = guideline
    
    @abstractmethod
    def calculate(self, data: InputT) -> OutputT:
        """
        Perform the calculation with the given input data.
        
        Args:
            data: The input data
            
        Returns:
            OutputT: The calculation result
            
        Raises:
            ValueError: If input data is invalid
        """
        pass 