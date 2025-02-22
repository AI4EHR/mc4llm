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

def test_guideline_initialization():
    # Test empty initialization
    guideline = BaseGuideline(description="Empty guideline")
    assert len(guideline.rules) == 0
    assert len(guideline.formulas) == 0
    assert guideline.description == "Empty guideline"
    
    # Test type checking
    with pytest.raises(TypeError):
        BaseGuideline(description=123)  # type: ignore

def test_rule_collection():
    guideline = BaseGuideline(description="Test rule collection")
    
    # Test adding single rule
    guideline.rules.add(age_rule)
    assert len(guideline.rules) == 1
    assert "age" in guideline.rules.names()
    
    # Test adding multiple rules as sequence
    guideline.rules.add([height_rule])
    assert len(guideline.rules) == 2
    assert "height" in guideline.rules.names()
    
    # Test getting rule by name
    age_rule_get = guideline.rules.get("age")
    assert age_rule_get.name == "age"
    
    # Test getting non-existent rule
    with pytest.raises(ValueError):
        guideline.rules.get("non_existent")
    
    # Test type checking
    with pytest.raises(TypeError):
        guideline.rules.add("not a rule")  # type: ignore
    
    with pytest.raises(TypeError):
        guideline.rules.add(None)  # type: ignore
    
    # Test duplicate names
    duplicate_rule = RangeRule(
        thresholds={"Test": (0, 1)},
        name="age"
    )
    with pytest.raises(ValueError):
        guideline.rules.add(duplicate_rule)
    
    # Test iteration
    names = [rule.name for rule in guideline.rules]
    assert names == ["age", "height"]
    
    # Test indexing
    assert guideline.rules[0].name == "age"
    assert guideline.rules[1].name == "height"

def test_formula_collection():
    guideline = BaseGuideline(description="Test formula collection")
    
    # Test adding single formula
    guideline.formulas.add(test_formula)
    assert len(guideline.formulas) == 1
    assert "test" in guideline.formulas.names()
    
    # Test adding multiple formulas as sequence
    another_formula = HelperFormula(name="another")
    guideline.formulas.add([another_formula])
    assert len(guideline.formulas) == 2
    assert "another" in guideline.formulas.names()
    
    # Test getting formula by name
    formula = guideline.formulas.get("test")
    assert formula.name == "test"
    
    # Test getting non-existent formula
    with pytest.raises(ValueError):
        guideline.formulas.get("non_existent")
    
    # Test type checking
    with pytest.raises(TypeError):
        guideline.formulas.add("not a formula")  # type: ignore
    
    with pytest.raises(TypeError):
        guideline.formulas.add(None)  # type: ignore
    
    # Test duplicate names
    duplicate_formula = HelperFormula(name="test")
    with pytest.raises(ValueError):
        guideline.formulas.add(duplicate_formula)
    
    # Test iteration
    names = [formula.name for formula in guideline.formulas]
    assert names == ["test", "another"]
    
    # Test indexing
    assert guideline.formulas[0].name == "test"
    assert guideline.formulas[1].name == "another"

def test_rule_categorization():
    guideline = BaseGuideline(description="Test rule categorization")
    guideline.rules.add([age_rule, height_rule])
    
    # Test age rule categorization
    age_rule_get = guideline.rules.get("age")
    assert age_rule_get.categorize(10) == "Child"
    assert age_rule_get.categorize(30) == "Adult"
    assert age_rule_get.categorize(70) == "Senior"
    assert age_rule_get.categorize(200) == "Unknown"  # Outside range
    
    # Test height rule categorization
    height_rule_get = guideline.rules.get("height")
    assert height_rule_get.categorize(150) == "Short"
    assert height_rule_get.categorize(170) == "Medium"
    assert height_rule_get.categorize(190) == "Tall"
    assert height_rule_get.categorize(300) == "Unknown"  # Outside range

def test_collection_sequence_interface():
    guideline = BaseGuideline(description="Test sequence interface")
    
    # Test rule collection sequence operations
    guideline.rules.add([age_rule, height_rule])
    assert len(guideline.rules) == 2
    assert list(guideline.rules) == [age_rule, height_rule]
    
    # Test replacing a rule with a new one (different name)
    new_rule = RangeRule(
        thresholds={"Test": (0, 1)},
        name="test_rule"
    )
    guideline.rules[0] = new_rule
    assert guideline.rules[0].name == "test_rule"
    
    # Test deleting a rule
    del guideline.rules[0]
    assert len(guideline.rules) == 1
    assert guideline.rules[0].name == "height"
    
    # Test formula collection sequence operations
    another_formula = HelperFormula(name="another")
    guideline.formulas.add([test_formula, another_formula])
    assert len(guideline.formulas) == 2
    assert list(guideline.formulas) == [test_formula, another_formula]
    
    # Test replacing a formula with a new one (different name)
    new_formula = HelperFormula(name="new_formula")
    guideline.formulas[0] = new_formula
    assert guideline.formulas[0].name == "new_formula"
    
    # Test deleting a formula
    del guideline.formulas[0]
    assert len(guideline.formulas) == 1
    assert guideline.formulas[0].name == "another"