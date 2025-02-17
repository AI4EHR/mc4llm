from typing import List, Union, Dict, Optional
from medical_calculators.rule.base import BaseRule
from medical_calculators.formula.base import BaseFormula

class BaseGuideline:
    """Base class for all guidelines that use rules and formulas for classification or calculation."""
    
    def __init__(self, 
                 rules: Union[BaseRule, List[BaseRule]], 
                 formulas: Optional[Dict[str, BaseFormula]] = None,
                 description: str = ""):
        """
        Initialize the guideline with rules and formulas.
        
        Args:
            rules: Single rule or list of rules
            formulas: Dictionary mapping formula names to formula instances (optional)
            description: A description of what this guideline represents and how it should be used
        """
        self.rules = [rules] if isinstance(rules, BaseRule) else rules
        self.formulas = {}
        if formulas:
            # Convert all formula names to lowercase for case-insensitive lookup
            self.formulas = {name.lower(): formula for name, formula in formulas.items()}
            
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
    
    def get_formula(self, name: str) -> BaseFormula:
        """
        Get a specific formula by name.
        
        Args:
            name: Name of the formula to retrieve
            
        Returns:
            BaseFormula: The requested formula
            
        Raises:
            ValueError: If the formula name doesn't exist
        """
        name = name.lower()  # Convert to lowercase for case-insensitive lookup
        if name not in self.formulas:
            raise ValueError(f"Formula '{name}' not found")
        return self.formulas[name]
    
    def get_available_rules(self) -> List[str]:
        """Get names of all available rules."""
        return [rule.name for rule in self.rules]
    
    def get_available_formulas(self) -> List[str]:
        """Get names of all available formulas."""
        return list(self.formulas.keys())
    
    def get_description(self) -> str:
        """Get a description of the guideline and its rules."""
        return self._description 