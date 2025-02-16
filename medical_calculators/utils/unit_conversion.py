# medical_calculators/utils/unit_conversion.py
from pint import UnitRegistry

ureg = UnitRegistry()

def convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert a given value from one unit to another.
    """
    return (value * ureg(from_unit)).to(to_unit).magnitude
