from typing import List, Union, Dict, Optional, Sequence, overload
from medical_calculators.rule.base import BaseRule
from medical_calculators.formula.base import BaseFormula

class BaseGuideline:
    """Base class for all guidelines that use rules and formulas for classification or calculation."""
    
    @overload
    def __init__(self, *, description: str = "") -> None:
        """
        Initialize an empty guideline.
        
        Args:
            description: A description of what this guideline represents and how it should be used
        """
        ...
    
    @overload
    def __init__(self, *, rules: Union[BaseRule, Sequence[BaseRule]], description: str = "") -> None:
        """
        Initialize a guideline with rules.
        
        Args:
            rules: Single rule or sequence of rules
            description: A description of what this guideline represents and how it should be used
        """
        ...
    
    @overload
    def __init__(self, *, formulas: Union[BaseFormula, Sequence[BaseFormula]], description: str = "") -> None:
        """
        Initialize a guideline with formulas.
        
        Args:
            formulas: Single formula or sequence of formulas
            description: A description of what this guideline represents and how it should be used
        """
        ...
    
    @overload
    def __init__(self, *, rules: Union[BaseRule, Sequence[BaseRule]], 
                 formulas: Union[BaseFormula, Sequence[BaseFormula]], description: str = "") -> None:
        """
        Initialize a guideline with both rules and formulas.
        
        Args:
            rules: Single rule or sequence of rules
            formulas: Single formula or sequence of formulas
            description: A description of what this guideline represents and how it should be used
        """
        ...
    
    def __init__(self, *, rules: Optional[Union[BaseRule, Sequence[BaseRule]]] = None,
                 formulas: Optional[Union[BaseFormula, Sequence[BaseFormula]]] = None,
                 description: str = "") -> None:
        """
        Initialize the guideline with optional rules and formulas.
        
        Args:
            rules: Single rule or sequence of rules (optional)
            formulas: Single formula or sequence of formulas (optional)
            description: A description of what this guideline represents and how it should be used
            
        Raises:
            TypeError: If rules or formulas are not of the correct type
        """
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
            
        self.rules: List[BaseRule] = []
        self.formulas: List[BaseFormula] = []
        self._description: str = description
        
        if rules is not None:
            self.add_rules(rules)
        if formulas is not None:
            self.add_formulas(formulas)
    
    def add_rule(self, rule: BaseRule) -> None:
        """
        Add a single rule to the guideline.
        
        Args:
            rule: Rule to add
            
        Raises:
            ValueError: If a rule with the same name already exists
            TypeError: If rule is not a BaseRule instance
        """
        if not isinstance(rule, BaseRule):
            raise TypeError("Rule must be an instance of BaseRule")
            
        if any(r.name == rule.name for r in self.rules):
            raise ValueError(f"Rule with name '{rule.name}' already exists")
        self.rules.append(rule)
    
    def add_rules(self, rules: Union[BaseRule, Sequence[BaseRule]]) -> None:
        """
        Add one or more rules to the guideline.
        
        Args:
            rules: Single rule or sequence of rules to add
            
        Raises:
            ValueError: If any rule has a duplicate name
            TypeError: If rules is not a BaseRule or sequence of BaseRule instances
        """
        if isinstance(rules, BaseRule):
            self.add_rule(rules)
        else:
            if not hasattr(rules, '__iter__'):
                raise TypeError("Rules must be a BaseRule instance or a sequence of BaseRule instances")
            for rule in rules:
                self.add_rule(rule)
    
    def add_formula(self, formula: BaseFormula) -> None:
        """
        Add a single formula to the guideline.
        
        Args:
            formula: Formula to add
            
        Raises:
            ValueError: If a formula with the same name already exists
            TypeError: If formula is not a BaseFormula instance
        """
        if not isinstance(formula, BaseFormula):
            raise TypeError("Formula must be an instance of BaseFormula")
            
        if any(f.name == formula.name for f in self.formulas):
            raise ValueError(f"Formula with name '{formula.name}' already exists")
        self.formulas.append(formula)
    
    def add_formulas(self, formulas: Union[BaseFormula, Sequence[BaseFormula]]) -> None:
        """
        Add one or more formulas to the guideline.
        
        Args:
            formulas: Single formula or sequence of formulas to add
            
        Raises:
            ValueError: If any formula has a duplicate name
            TypeError: If formulas is not a BaseFormula or sequence of BaseFormula instances
        """
        if isinstance(formulas, BaseFormula):
            self.add_formula(formulas)
        else:
            if not hasattr(formulas, '__iter__'):
                raise TypeError("Formulas must be a BaseFormula instance or a sequence of BaseFormula instances")
            for formula in formulas:
                self.add_formula(formula)
    
    def get_rule(self, name: str) -> BaseRule:
        """
        Get a specific rule by name.
        
        Args:
            name: Name of the rule to retrieve
            
        Returns:
            BaseRule: The requested rule
            
        Raises:
            ValueError: If the rule name doesn't exist
            TypeError: If name is not a string
        """
        if not isinstance(name, str):
            raise TypeError("Rule name must be a string")
            
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
            TypeError: If name is not a string
        """
        if not isinstance(name, str):
            raise TypeError("Formula name must be a string")
            
        for formula in self.formulas:
            if formula.name == name:
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