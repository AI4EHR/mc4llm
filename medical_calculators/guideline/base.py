from typing import List, Union, Dict, Optional
from medical_calculators.rule.base import BaseRule
from medical_calculators.formula.base import BaseFormula

class BaseGuideline:
    """Base class for all guidelines that use rules and formulas for classification or calculation."""
    
    def __init__(self, 
                 rules: Union[BaseRule, List[BaseRule]], 
                 formulas: Optional[Union[BaseFormula, List[BaseFormula]]] = None,
                 description: str = ""):
        """
        Initialize the guideline with rules and formulas.
        
        Args:
            rules: Single rule or list of rules
            formulas: Single formula or list of formulas (optional)
            description: A description of what this guideline represents and how it should be used
        """
        self.rules = [rules] if isinstance(rules, BaseRule) else rules
        self.formulas = []
        if formulas:
            self.formulas = [formulas] if isinstance(formulas, BaseFormula) else formulas
            
        self._description = description
        self._validate_rules()
        self._validate_formulas()
    
    def _validate_rules(self):
        """Validate that all rules have unique names."""
        names = [rule.name for rule in self.rules]
        if len(names) != len(set(names)):
            raise ValueError("All rules must have unique names")
    
    def _validate_formulas(self):
        """Validate that all formulas have unique names."""
        names = [formula.name for formula in self.formulas]
        if len(names) != len(set(names)):
            raise ValueError("All formulas must have unique names")
    
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
        name = name.lower()  # Keep case-insensitive lookup for backward compatibility
        for formula in self.formulas:
            if formula.name.lower() == name:
                return formula
        raise ValueError(f"Formula '{name}' not found")
    
    def get_available_rules(self) -> List[str]:
        """Get names of all available rules."""
        return [rule.name for rule in self.rules]
    
    def get_available_formulas(self) -> List[str]:
        """Get names of all available formulas."""
        return [formula.name for formula in self.formulas]
    
    def get_description(self) -> str:
        """Get a description of the guideline and its rules."""
        return self._description