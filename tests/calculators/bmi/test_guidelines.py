import pytest
from typing import List, Sequence
from medical_calculators.guideline import BaseGuideline
from medical_calculators.rule import RangeRule
from tests.helpers.formula import HelperFormula

# Create test rules
age_rule = RangeRule(
    thresholds={
        "Child": (0, 18),
        "Adult": (18, 65),
        "Senior": (65, 150)
    },
    default_category="Unknown",
    name="age"
)

height_rule = RangeRule(
    thresholds={
        "Short": (0, 160),
        "Medium": (160, 180),
        "Tall": (180, 250)
    },
    default_category="Unknown",
    name="height"
)

# Create test formula instance
test_formula = HelperFormula(name="test")

def test_guideline_initialization_patterns():
    # Test empty initialization
    empty_guideline = BaseGuideline(description="Empty guideline")
    assert len(empty_guideline.get_available_rules()) == 0
    assert len(empty_guideline.get_available_formulas()) == 0
    assert empty_guideline.get_description() == "Empty guideline"
    
    # Test initialization with single rule
    rule_guideline = BaseGuideline(rules=age_rule, description="Rule guideline")
    assert len(rule_guideline.get_available_rules()) == 1
    assert "age" in rule_guideline.get_available_rules()
    
    # Test initialization with multiple rules
    rules_guideline = BaseGuideline(rules=[age_rule, height_rule], description="Rules guideline")
    assert len(rules_guideline.get_available_rules()) == 2
    assert "age" in rules_guideline.get_available_rules()
    assert "height" in rules_guideline.get_available_rules()
    
    # Test initialization with single formula
    formula_guideline = BaseGuideline(formulas=test_formula, description="Formula guideline")
    assert len(formula_guideline.get_available_formulas()) == 1
    assert "test" in formula_guideline.get_available_formulas()
    
    # Test initialization with multiple formulas
    another_formula = HelperFormula(name="another")
    formulas_guideline = BaseGuideline(
        formulas=[test_formula, another_formula],
        description="Formulas guideline"
    )
    assert len(formulas_guideline.get_available_formulas()) == 2
    assert "test" in formulas_guideline.get_available_formulas()
    assert "another" in formulas_guideline.get_available_formulas()
    
    # Test initialization with both rules and formulas
    full_guideline = BaseGuideline(
        rules=[age_rule, height_rule],
        formulas=[test_formula, another_formula],
        description="Full guideline"
    )
    assert len(full_guideline.get_available_rules()) == 2
    assert len(full_guideline.get_available_formulas()) == 2

def test_guideline_add_rules():
    guideline = BaseGuideline(description="Test adding rules")
    
    # Test adding single rule
    guideline.add_rule(age_rule)
    assert len(guideline.get_available_rules()) == 1
    assert "age" in guideline.get_available_rules()
    
    # Test adding multiple rules as sequence
    guideline.add_rules([height_rule])
    assert len(guideline.get_available_rules()) == 2
    assert "height" in guideline.get_available_rules()
    
    # Test adding single rule via add_rules
    new_rule = RangeRule(
        thresholds={"Test": (0, 1)},
        name="test_rule"
    )
    guideline.add_rules(new_rule)  # type: ignore[arg-type]  # This is actually valid due to Union type
    assert "test_rule" in guideline.get_available_rules()
    
    # Test adding duplicate rule
    with pytest.raises(ValueError):
        guideline.add_rule(age_rule)

def test_guideline_add_formulas():
    guideline = BaseGuideline(description="Test adding formulas")
    
    # Test adding single formula
    guideline.add_formula(test_formula)
    assert len(guideline.get_available_formulas()) == 1
    assert "test" in guideline.get_available_formulas()
    
    # Test adding multiple formulas as sequence
    another_formula = HelperFormula(name="another")
    guideline.add_formulas([another_formula])
    assert len(guideline.get_available_formulas()) == 2
    assert "another" in guideline.get_available_formulas()
    
    # Test adding single formula via add_formulas
    new_formula = HelperFormula(name="new_formula")
    guideline.add_formulas(new_formula)  # type: ignore[arg-type]  # This is actually valid due to Union type
    assert "new_formula" in guideline.get_available_formulas()
    
    # Test adding duplicate formula
    duplicate_formula = HelperFormula(name="test")
    with pytest.raises(ValueError):
        guideline.add_formula(duplicate_formula)

def test_guideline_rule_management():
    guideline = BaseGuideline(description="Test rule management")
    guideline.add_rules([age_rule, height_rule])
    
    # Test getting available rules
    available_rules = guideline.get_available_rules()
    assert "age" in available_rules
    assert "height" in available_rules
    assert len(available_rules) == 2
    
    # Test getting specific rules
    age_rule_get = guideline.get_rule("age")
    height_rule_get = guideline.get_rule("height")
    assert age_rule_get.name == "age"
    assert height_rule_get.name == "height"
    
    # Test getting non-existent rule
    with pytest.raises(ValueError):
        guideline.get_rule("non_existent")

def test_guideline_formula_management():
    guideline = BaseGuideline(description="Test formula management")
    guideline.add_formula(test_formula)
    
    # Test getting available formulas
    available_formulas = guideline.get_available_formulas()
    assert "test" in available_formulas
    assert len(available_formulas) == 1
    
    # Test getting specific formula
    formula = guideline.get_formula("test")
    assert formula.name == "test"
    
    # Test getting non-existent formula
    with pytest.raises(ValueError):
        guideline.get_formula("non_existent")

def test_guideline_rule_categorization():
    guideline = BaseGuideline(description="Test rule categorization")
    guideline.add_rules([age_rule, height_rule])
    
    # Test age rule categorization
    age_rule_get = guideline.get_rule("age")
    assert age_rule_get.categorize(10) == "Child"
    assert age_rule_get.categorize(30) == "Adult"
    assert age_rule_get.categorize(70) == "Senior"
    assert age_rule_get.categorize(200) == "Unknown"  # Outside range
    
    # Test height rule categorization
    height_rule_get = guideline.get_rule("height")
    assert height_rule_get.categorize(150) == "Short"
    assert height_rule_get.categorize(170) == "Medium"
    assert height_rule_get.categorize(190) == "Tall"
    assert height_rule_get.categorize(300) == "Unknown"  # Outside range

def test_guideline_description():
    guideline = BaseGuideline(description="Test description")
    assert guideline.get_description() == "Test description"

def test_guideline_duplicate_rule_names():
    # Test that adding rules with duplicate names fails
    guideline = BaseGuideline(description="Test duplicate rule names")
    duplicate_rule1 = RangeRule(
        thresholds={"A": (0, 1)},
        name="same_name"
    )
    duplicate_rule2 = RangeRule(
        thresholds={"B": (1, 2)},
        name="same_name"
    )
    
    guideline.add_rule(duplicate_rule1)
    with pytest.raises(ValueError):
        guideline.add_rule(duplicate_rule2)

def test_guideline_duplicate_formula_names():
    # Test that adding formulas with duplicate names fails
    guideline = BaseGuideline(description="Test duplicate formula names")
    duplicate_formula1 = HelperFormula(name="same_name")
    duplicate_formula2 = HelperFormula(name="same_name")
    
    guideline.add_formula(duplicate_formula1)
    with pytest.raises(ValueError):
        guideline.add_formula(duplicate_formula2)

def test_guideline_without_formula():
    # Test creating guideline without formula
    guideline = BaseGuideline(description="Guideline without formula")
    guideline.add_rule(age_rule)
    
    assert len(guideline.get_available_formulas()) == 0
    
    # Test getting formula from guideline without formula
    with pytest.raises(ValueError):
        guideline.get_formula("standard")

def test_guideline_type_safety():
    # Test type annotations
    guideline: BaseGuideline = BaseGuideline(description="Type test")
    rules: List[str] = guideline.get_available_rules()
    formulas: List[str] = guideline.get_available_formulas()
    description: str = guideline.get_description()
    
    # Test type checking with incorrect types
    with pytest.raises(TypeError):
        guideline.add_rule("not a rule")  # type: ignore
    
    with pytest.raises(TypeError):
        guideline.add_formula("not a formula")  # type: ignore
    
    # Test sequence types
    tuple_rules: Sequence[BaseRule] = (age_rule, height_rule)
    guideline.add_rules(tuple_rules)
    assert len(guideline.get_available_rules()) == 2
    
    # Test type safety with None
    with pytest.raises(TypeError):
        guideline.add_rule(None)  # type: ignore
    
    with pytest.raises(TypeError):
        guideline.add_formula(None)  # type: ignore