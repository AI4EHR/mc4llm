from typing import Dict, Tuple, Optional
from mc4llm.rule.base import BaseClassificationRule

class RangeRule(BaseClassificationRule):
    """Represents a rule that classifies a value into categories based on numeric ranges."""
    def __init__(self, thresholds: Dict[str, Tuple[float, float]], default_category: str = "Unknown", name: Optional[str] = None):
        super().__init__(name)
        self._validate_thresholds(thresholds)
        self.thresholds = thresholds
        self.default_category = default_category

    def _validate_thresholds(self, thresholds: Dict[str, Tuple[float, float]]) -> None:
        """
        Validate the thresholds dictionary.
        
        Args:
            thresholds: Dictionary of category names to (min, max) range tuples
            
        Raises:
            ValueError: If thresholds are invalid
        """
        if not thresholds:
            raise ValueError("Thresholds dictionary cannot be empty")
            
        # Check for invalid ranges (min > max)
        for category, (min_val, max_val) in thresholds.items():
            if min_val >= max_val:
                raise ValueError(f"Invalid range for category '{category}': minimum value must be less than maximum value")
        
        # Check for overlapping ranges
        sorted_ranges = sorted((min_val, max_val, category) for category, (min_val, max_val) in thresholds.items())
        for i in range(len(sorted_ranges) - 1):
            current_max = sorted_ranges[i][1]
            next_min = sorted_ranges[i + 1][0]
            if current_max > next_min:
                raise ValueError(
                    f"Overlapping ranges detected between categories '{sorted_ranges[i][2]}' and '{sorted_ranges[i + 1][2]}'"
                )

    def categorize(self, value: float, **kwargs) -> str:
        """Categorize a value based on the defined thresholds."""
        for category, (min_val, max_val) in self.thresholds.items():
            if min_val <= value < max_val:
                return category
        return self.default_category 