from typing import List, Union, Dict, Optional, Sequence, overload, Iterator
from collections.abc import MutableSequence
from medical_calculators.rule.base import BaseRule
from medical_calculators.formula.base import BaseFormula

class RuleCollection(MutableSequence[BaseRule]):
    """Collection class for managing rules in a guideline."""
    
    def __init__(self, parent: 'BaseGuideline'):
        self._rules: List[BaseRule] = []
        self._parent = parent
    
    def __getitem__(self, i: int) -> BaseRule:
        return self._rules[i]
    
    def __len__(self) -> int:
        return len(self._rules)
    
    def __iter__(self) -> Iterator[BaseRule]:
        return iter(self._rules)
    
    def __setitem__(self, i: int, rule: BaseRule) -> None:
        if not isinstance(rule, BaseRule):
            raise TypeError("Rule must be an instance of BaseRule")
        if any(r.name == rule.name for j, r in enumerate(self._rules) if j != i):
            raise ValueError(f"Rule with name '{rule.name}' already exists")
        self._rules[i] = rule
    
    def __delitem__(self, i: int) -> None:
        del self._rules[i]
    
    def insert(self, index: int, rule: BaseRule) -> None:
        if not isinstance(rule, BaseRule):
            raise TypeError("Rule must be an instance of BaseRule")
        if any(r.name == rule.name for r in self._rules):
            raise ValueError(f"Rule with name '{rule.name}' already exists")
        self._rules.insert(index, rule)
    
    @overload
    def add(self, rule: BaseRule) -> None: ...
    
    @overload
    def add(self, rules: Sequence[BaseRule]) -> None: ...
    
    def add(self, rule_or_rules: Union[BaseRule, Sequence[BaseRule]]) -> None:
        """
        Add a single rule or sequence of rules.
        
        Args:
            rule_or_rules: Single rule or sequence of rules to add
            
        Raises:
            TypeError: If any rule is not a BaseRule instance
            ValueError: If any rule has a duplicate name
        """
        if isinstance(rule_or_rules, BaseRule):
            self.insert(len(self), rule_or_rules)
        else:
            if not hasattr(rule_or_rules, '__iter__'):
                raise TypeError("Rules must be a BaseRule instance or a sequence of BaseRule instances")
            for rule in rule_or_rules:
                self.insert(len(self), rule)
    
    def get(self, name: str) -> BaseRule:
        """
        Get a rule by name.
        
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
        for rule in self._rules:
            if rule.name == name:
                return rule
        raise ValueError(f"Rule '{name}' not found")
    
    def names(self) -> List[str]:
        """Get names of all rules in the collection."""
        return [rule.name for rule in self._rules]

class FormulaCollection(MutableSequence[BaseFormula]):
    """Collection class for managing formulas in a guideline."""
    
    def __init__(self, parent: 'BaseGuideline'):
        self._formulas: List[BaseFormula] = []
        self._parent = parent
    
    def __getitem__(self, i: int) -> BaseFormula:
        return self._formulas[i]
    
    def __len__(self) -> int:
        return len(self._formulas)
    
    def __iter__(self) -> Iterator[BaseFormula]:
        return iter(self._formulas)
    
    def __setitem__(self, i: int, formula: BaseFormula) -> None:
        if not isinstance(formula, BaseFormula):
            raise TypeError("Formula must be an instance of BaseFormula")
        if any(f.name == formula.name for j, f in enumerate(self._formulas) if j != i):
            raise ValueError(f"Formula with name '{formula.name}' already exists")
        self._formulas[i] = formula
    
    def __delitem__(self, i: int) -> None:
        del self._formulas[i]
    
    def insert(self, index: int, formula: BaseFormula) -> None:
        if not isinstance(formula, BaseFormula):
            raise TypeError("Formula must be an instance of BaseFormula")
        if any(f.name == formula.name for f in self._formulas):
            raise ValueError(f"Formula with name '{formula.name}' already exists")
        self._formulas.insert(index, formula)
    
    @overload
    def add(self, formula: BaseFormula) -> None: ...
    
    @overload
    def add(self, formulas: Sequence[BaseFormula]) -> None: ...
    
    def add(self, formula_or_formulas: Union[BaseFormula, Sequence[BaseFormula]]) -> None:
        """
        Add a single formula or sequence of formulas.
        
        Args:
            formula_or_formulas: Single formula or sequence of formulas to add
            
        Raises:
            TypeError: If any formula is not a BaseFormula instance
            ValueError: If any formula has a duplicate name
        """
        if isinstance(formula_or_formulas, BaseFormula):
            self.insert(len(self), formula_or_formulas)
        else:
            if not hasattr(formula_or_formulas, '__iter__'):
                raise TypeError("Formulas must be a BaseFormula instance or a sequence of BaseFormula instances")
            for formula in formula_or_formulas:
                self.insert(len(self), formula)
    
    def get(self, name: str) -> BaseFormula:
        """
        Get a formula by name.
        
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
        for formula in self._formulas:
            if formula.name == name:
                return formula
        raise ValueError(f"Formula '{name}' not found")
    
    def names(self) -> List[str]:
        """Get names of all formulas in the collection."""
        return [formula.name for formula in self._formulas]

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
            
        self._rules = RuleCollection(self)
        self._formulas = FormulaCollection(self)
        self._description = description
        
        if rules is not None:
            self._rules.add(rules)
        if formulas is not None:
            self._formulas.add(formulas)
    
    @property
    def rules(self) -> RuleCollection:
        """Access the rule collection."""
        return self._rules
    
    @property
    def formulas(self) -> FormulaCollection:
        """Access the formula collection."""
        return self._formulas
    
    @property
    def description(self) -> str:
        """Get the guideline description."""
        return self._description
    
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
        return self.rules.names()
    
    def get_available_formulas(self) -> List[str]:
        """Get names of all available formulas."""
        return self.formulas.names()