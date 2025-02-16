from abc import ABC
from typing import Dict, Tuple, Any, Optional

class RangeRule:
    """Represents a rule that classifies a value into categories based on numeric ranges."""
    def __init__(self, thresholds: Dict[str, Tuple[float, float]], default_category: str = "Unknown"):
        self.thresholds = thresholds
        self.default_category = default_category

    def categorize(self, value: float) -> str:
        """Categorize a value based on the defined thresholds."""
        for category, (min_val, max_val) in self.thresholds.items():
            if min_val <= value < max_val:
                return category
        return self.default_category

class Guideline(ABC):
    """Base class for all guidelines that use range-based classification."""
    
    def __init__(self, rule: RangeRule):
        """
        Initialize the guideline with a RangeRule.
        
        Args:
            rule: The RangeRule that defines the classification thresholds
        """
        self.rule = rule
    
    def categorize(self, value: float) -> str:
        """
        Categorize a value using the guideline's rule.
        
        Args:
            value: The numeric value to categorize
            
        Returns:
            str: The category the value falls into
        """
        return self.rule.categorize(value) 