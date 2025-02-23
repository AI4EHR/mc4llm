from pydantic import BaseModel, Field, validator, ConfigDict
from pint import UnitRegistry, Quantity

ureg = UnitRegistry()

# Define your custom base class.
class IOModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    """
    Base class for all medical calculator IO models.
    In the future, common functionality or configuration can be added here.
    """
    pass

# Decorator that performs automatic unit conversion.
def convert_unit(target_unit: str):
    """
    A decorator to convert a field's value to the desired target unit.
    The field can be provided as:
      - a pint.Quantity (which will be converted),
      - a tuple/list (value, unit), or
      - a dict with keys 'value' and 'unit'.
    """
    def decorator(fn):
        @validator(fn.__name__, pre=True, allow_reuse=True)
        def wrapper(cls, v):
            # If the value is already a pint.Quantity, convert directly.
            if isinstance(v, Quantity):
                return v.to(target_unit)
            # If the value is a tuple or list (value, unit)
            elif isinstance(v, (tuple, list)) and len(v) == 2:
                value, unit = v
                return ureg.Quantity(value, unit).to(target_unit)
            # If the value is a dict with keys 'value' and 'unit'
            elif isinstance(v, dict) and 'value' in v and 'unit' in v:
                return ureg.Quantity(v['value'], v['unit']).to(target_unit)
            else:
                raise ValueError(
                    f"Field '{fn.__name__}' must be a pint.Quantity, a tuple/list (value, unit), or a dict with 'value' and 'unit'."
                )
        return wrapper
    return decorator