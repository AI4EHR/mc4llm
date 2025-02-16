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

class MultiParameterRule(ClassificationRule):
    """Rule for classifying based on multiple parameters."""
    def __init__(self, classification_func: Callable[..., str], parameter_names: List[str], name: Optional[str] = None):
        super().__init__(name)
        self.classify = classification_func
        self.parameter_names = parameter_names

    def categorize(self, value: Any, **parameters) -> str:
        """
        Categorize based on multiple parameters.
        
        Args:
            value: The primary value (if applicable)
            **parameters: Additional parameters needed for classification
            
        Returns:
            str: The classification result
        """
        return self.classify(**parameters)

class CorrectionRule(BaseRule):
    """Rule for correcting measurements based on other parameters."""
    def __init__(self, correction_factors: Dict[str, Callable[[float, ...], float]], name: Optional[str] = None):
        super().__init__(name)
        self.correction_factors = correction_factors

    def calculate(self, value: float, correction_type: str, **parameters) -> float:
        """
        Apply corrections to laboratory or clinical values.
        
        Args:
            value: The value to correct
            correction_type: Type of correction to apply
            **parameters: Additional parameters needed for correction
            
        Returns:
            float: The corrected value
            
        Raises:
            ValueError: If correction_type is not found
        """
        if correction_type not in self.correction_factors:
            raise ValueError(f"Unknown correction type: {correction_type}")
        return self.correction_factors[correction_type](value, **parameters)

class Guideline(ABC):
    """Base class for all guidelines that use rules for classification or calculation."""
    
    def __init__(self, rules: Union[BaseRule, List[BaseRule]], default_rule: Optional[str] = None):
        """
        Initialize the guideline with one or more rules.
        
        Args:
            rules: Single rule or list of rules
            default_rule: Name of the default rule to use if multiple rules are provided
        """
        self.rules = [rules] if isinstance(rules, BaseRule) else rules
        self._validate_rules()
        self.default_rule = default_rule or (self.rules[0].name if self.rules else None)
    
    def _validate_rules(self):
        """Validate that all rules have unique names."""
        names = [rule.name for rule in self.rules]
        if len(names) != len(set(names)):
            raise ValueError("All rules must have unique names")
    
    def get_rule(self, name: Optional[str] = None) -> BaseRule:
        """
        Get a specific rule by name.
        
        Args:
            name: Name of the rule to retrieve. If None, returns the default rule.
            
        Returns:
            BaseRule: The requested rule
            
        Raises:
            ValueError: If the rule name doesn't exist
        """
        rule_name = name or self.default_rule
        for rule in self.rules:
            if rule.name == rule_name:
                return rule
        raise ValueError(f"Rule '{rule_name}' not found")
    
    def categorize(self, value: float, rule_name: Optional[str] = None) -> str:
        """
        Categorize a value using a specific rule or the default rule.
        
        Args:
            value: The numeric value to categorize
            rule_name: Name of the rule to use for categorization. If None, uses default rule.
            
        Returns:
            str: The category the value falls into
        """
        rule = self.get_rule(rule_name)
        return rule.categorize(value)
    
    def get_available_rules(self) -> List[str]:
        """Get names of all available rules."""
        return [rule.name for rule in self.rules]
    
    @abstractmethod
    def get_description(self) -> str:
        """Get a description of the guideline and its rules."""
        pass 