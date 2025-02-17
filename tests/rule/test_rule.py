import pytest
from medical_calculators.rule.base import BaseRule, BaseClassificationRule
from medical_calculators.rule.range import RangeRule

def test_base_rule_creation():
    # Test basic rule creation
    class SimpleRule(BaseRule):
        pass
    
    rule = SimpleRule()
    assert rule.name == "default"
    
    named_rule = SimpleRule(name="test_rule")
    assert named_rule.name == "test_rule"

def test_range_rule_creation():
    # Test basic range rule creation
    thresholds = {
        "Low": (0, 18.5),
        "Normal": (18.5, 25),
        "High": (25, 30),
        "Very High": (30, 100)
    }
    
    rule = RangeRule(
        thresholds=thresholds,
        default_category="Unknown",
        name="test_range"
    )
    
    assert rule.name == "test_range"
    assert rule.default_category == "Unknown"
    assert rule.thresholds == thresholds

def test_range_rule_categorization():
    # Create a BMI-like range rule
    rule = RangeRule(
        thresholds={
            "Underweight": (0, 18.5),
            "Normal": (18.5, 25),
            "Overweight": (25, 30),
            "Obese": (30, 100)
        },
        default_category="Unknown"
    )
    
    # Test various categorizations
    assert rule.categorize(17.5) == "Underweight"
    assert rule.categorize(22.0) == "Normal"
    assert rule.categorize(27.5) == "Overweight"
    assert rule.categorize(35.0) == "Obese"
    
    # Test edge cases
    assert rule.categorize(-1) == "Unknown"  # Below minimum
    assert rule.categorize(150) == "Unknown"  # Above maximum

def test_range_rule_edge_cases():
    # Test empty thresholds
    with pytest.raises(ValueError):
        RangeRule(thresholds={})
    
    # Test overlapping ranges
    overlapping_thresholds = {
        "Range1": (0, 10),
        "Range2": (5, 15)  # Overlaps with Range1
    }
    with pytest.raises(ValueError):
        RangeRule(thresholds=overlapping_thresholds)
    
    # Test invalid range (min > max)
    invalid_thresholds = {
        "Invalid": (10, 5)  # min > max
    }
    with pytest.raises(ValueError):
        RangeRule(thresholds=invalid_thresholds)

def test_classification_rule_interface():
    # Test that BaseClassificationRule cannot be instantiated directly
    with pytest.raises(TypeError):
        BaseClassificationRule()
    
    # Test that categorize method must be implemented
    class IncompleteRule(BaseClassificationRule):
        pass
    
    with pytest.raises(TypeError):
        IncompleteRule() 