import pytest
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

# Create test guideline instance
test_guideline = BaseGuideline(
    rules=[age_rule, height_rule],
    formulas=test_formula,
    description="A test guideline for testing core guideline functionality"
)

def test_guideline_rule_management():
    # Test getting available rules
    available_rules = test_guideline.get_available_rules()
    assert "age" in available_rules
    assert "height" in available_rules
    assert len(available_rules) == 2
    
    # Test getting specific rules
    age_rule = test_guideline.get_rule("age")
    height_rule = test_guideline.get_rule("height")
    assert age_rule.name == "age"
    assert height_rule.name == "height"
    
    # Test getting non-existent rule
    with pytest.raises(ValueError):
        test_guideline.get_rule("non_existent")

def test_guideline_formula_management():
    # Test getting available formulas
    available_formulas = test_guideline.get_available_formulas()
    assert "test" in available_formulas
    assert len(available_formulas) == 1
    
    # Test getting specific formula
    formula = test_guideline.get_formula("test")
    assert formula.name == "test"
    
    # Test getting non-existent formula
    with pytest.raises(ValueError):
        test_guideline.get_formula("non_existent")

def test_guideline_rule_categorization():
    # Test age rule categorization
    age_rule = test_guideline.get_rule("age")
    assert age_rule.categorize(10) == "Child"
    assert age_rule.categorize(30) == "Adult"
    assert age_rule.categorize(70) == "Senior"
    assert age_rule.categorize(200) == "Unknown"  # Outside range
    
    # Test height rule categorization
    height_rule = test_guideline.get_rule("height")
    assert height_rule.categorize(150) == "Short"
    assert height_rule.categorize(170) == "Medium"
    assert height_rule.categorize(190) == "Tall"
    assert height_rule.categorize(300) == "Unknown"  # Outside range

def test_guideline_description():
    description = test_guideline.get_description()
    assert description == "A test guideline for testing core guideline functionality"

def test_guideline_duplicate_rule_names():
    # Test that guideline creation fails with duplicate rule names
    duplicate_rule1 = RangeRule(
        thresholds={"A": (0, 1)},
        name="same_name"
    )
    duplicate_rule2 = RangeRule(
        thresholds={"B": (1, 2)},
        name="same_name"
    )
    
    with pytest.raises(ValueError):
        BaseGuideline(
            rules=[duplicate_rule1, duplicate_rule2],
            description="Should fail due to duplicate rule names"
        )

def test_guideline_duplicate_formula_names():
    # Test that guideline creation fails with duplicate formula names
    duplicate_formula1 = HelperFormula(name="same_name")
    duplicate_formula2 = HelperFormula(name="same_name")
    
    with pytest.raises(ValueError):
        BaseGuideline(
            rules=age_rule,
            formulas=[duplicate_formula1, duplicate_formula2],
            description="Should fail due to duplicate formula names"
        )

def test_guideline_without_formula():
    # Test creating guideline without formula
    guideline = BaseGuideline(
        rules=age_rule,
        description="Guideline without formula"
    )
    assert len(guideline.get_available_formulas()) == 0
    
    # Test getting formula from guideline without formula
    with pytest.raises(ValueError):
        guideline.get_formula("standard")