from typing import List, Union
from medical_calculators.rule.base import BaseRule

class BaseGuideline:
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