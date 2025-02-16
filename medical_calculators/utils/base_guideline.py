from abc import ABC, abstractmethod
from typing import Dict, Tuple, Any, Optional, List, Union

class RangeRule:
    """Represents a rule that classifies a value into categories based on numeric ranges."""
    def __init__(self, thresholds: Dict[str, Tuple[float, float]], default_category: str = "Unknown", name: Optional[str] = None):
        self.thresholds = thresholds
        self.default_category = default_category
        self.name = name or "default"

    def categorize(self, value: float) -> str:
        """Categorize a value based on the defined thresholds."""
        for category, (min_val, max_val) in self.thresholds.items():
            if min_val <= value < max_val:
                return category
        return self.default_category

class Guideline(ABC):
    """Base class for all guidelines that use range-based classification."""
    
    def __init__(self, rules: Union[RangeRule, List[RangeRule]], default_rule: Optional[str] = None):
        """
        Initialize the guideline with one or more RangeRules.
        
        Args:
            rules: Single RangeRule or list of RangeRules for classification
            default_rule: Name of the default rule to use if multiple rules are provided
        """
        self.rules = [rules] if isinstance(rules, RangeRule) else rules
        self._validate_rules()
        self.default_rule = default_rule or (self.rules[0].name if self.rules else None)
    
    def _validate_rules(self):
        """Validate that all rules have unique names."""
        names = [rule.name for rule in self.rules]
        if len(names) != len(set(names)):
            raise ValueError("All rules must have unique names")
    
    def get_rule(self, name: Optional[str] = None) -> RangeRule:
        """
        Get a specific rule by name.
        
        Args:
            name: Name of the rule to retrieve. If None, returns the default rule.
            
        Returns:
            RangeRule: The requested rule
            
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