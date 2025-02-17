from typing import Dict, Tuple, Optional
from medical_calculators.rule.base import BaseClassificationRule

class RangeRule(BaseClassificationRule):
    """Represents a rule that classifies a value into categories based on numeric ranges."""
    def __init__(self, thresholds: Dict[str, Tuple[float, float]], default_category: str = "Unknown", name: Optional[str] = None):
        super().__init__(name)
        self.thresholds = thresholds
        self.default_category = default_category

    def categorize(self, value: float, **kwargs) -> str:
        """Categorize a value based on the defined thresholds."""
        for category, (min_val, max_val) in self.thresholds.items():
            if min_val <= value < max_val:
                return category
        return self.default_category 