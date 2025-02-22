from abc import ABC, abstractmethod
from typing import Any, Optional

class BaseRule(ABC):
    """Root class for all types of rules in the system."""
    def __init__(self, name: Optional[str] = None):
        self.name = name or "default"

class BaseClassificationRule(BaseRule, ABC):
    """Abstract base class for rules that classify values into categories."""
    @abstractmethod
    def categorize(self, value: Any, **kwargs) -> str:
        """
        Categorize a value based on the rule's logic.
        
        Args:
            value: The primary value to categorize
            **kwargs: Additional parameters that might be needed for classification
            
        Returns:
            str: The category the value falls into
        """
        pass 