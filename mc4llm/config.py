# medical_calculators/config.py

DEFAULT_UNITS = {
    "weight": "kg",      # Default weight unit (SI)
    "height": "m",       # Default height unit (SI)
    "bmi": "kg/m^2",     # Default BMI output unit (SI)
}

def set_default_units(region: str):
    """
    Set the default units based on region.
    If region is "US", default weight becomes pounds (lb) and height inches (in).
    For other regions (or if no config is set), SI units are used.
    """
    global DEFAULT_UNITS
    region = region.upper()
    if region == "US":
        DEFAULT_UNITS = {
            "weight": "lb",
            "height": "in",
            "bmi": "lb/in^2"
        }
    elif region == "UK":
        # Depending on local preference you might choose imperial or SI.
        # Here we assume SI for the UK.
        DEFAULT_UNITS = {
            "weight": "kg",
            "height": "m",
            "bmi": "kg/m^2"
        }
    else:
        DEFAULT_UNITS = {
            "weight": "kg",
            "height": "m",
            "bmi": "kg/m^2"
        }
