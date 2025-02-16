from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any, Optional, List, Union, Callable

class BaseRule(ABC):
    """Root class for all types of rules in the system."""
    def __init__(self, name: Optional[str] = None):
        self.name = name or "default"

class ClassificationRule(BaseRule, ABC):
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

class RangeRule(ClassificationRule):
    """Represents a rule that classifies a value into categories based on numeric ranges."""
    def __init__(self, thresholds: Dict[str, Tuple[float, float]], default_category: str = "Unknown", name: Optional[str] = None):
        super().__init__(name)
        self.thresholds = thresholds
        self.default_category = default_category

    def categorize(self, value: float, **kwargs) -> str:
        """Categorize a value based on the defined thresholds."""
        for category, (min_val, max_val) in self.thresholds.items():
            if min_val <= value < max_val:
                return category
        return self.default_category

class Guideline(ABC):
    """Base class for all guidelines that use rules for classification or calculation."""
    
    def __init__(self, rules: Union[BaseRule, List[BaseRule]], description: str):
        """
        Initialize the guideline with one or more rules.
        
        Args:
            rules: Single rule or list of rules
            description: A description of what this guideline represents and how it should be used
        """
        self.rules = [rules] if isinstance(rules, BaseRule) else rules
        self._description = description
        self._validate_rules()
    
    def _validate_rules(self):
        """Validate that all rules have unique names."""
        names = [rule.name for rule in self.rules]
        if len(names) != len(set(names)):
            raise ValueError("All rules must have unique names")
    
    def get_rule(self, name: str) -> BaseRule:
        """
        Get a specific rule by name.
        
        Args:
            name: Name of the rule to retrieve
            
        Returns:
            BaseRule: The requested rule
            
        Raises:
            ValueError: If the rule name doesn't exist
        """
        for rule in self.rules:
            if rule.name == name:
                return rule
        raise ValueError(f"Rule '{name}' not found")
    
    def get_available_rules(self) -> List[str]:
        """Get names of all available rules."""
        return [rule.name for rule in self.rules]
    
    def get_description(self) -> str:
        """Get a description of the guideline and its rules."""
        return self._description 