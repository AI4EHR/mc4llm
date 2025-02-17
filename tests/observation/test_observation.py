import pytest
from medical_calculators.observation.base import BaseObservation, TimeSeriesObservation
from pint import UnitRegistry

def test_base_observation_creation():
    # Test basic observation creation
    obs = BaseObservation(value=75.5)
    assert obs.value == 75.5
    assert obs.unit is None
    
    # Test observation with unit
    obs_with_unit = BaseObservation(value=75.5, unit="kg")
    assert obs_with_unit.value == 75.5
    assert obs_with_unit.unit == "kg"

def test_observation_unit_conversion():
    # Test weight conversion
    weight_obs = BaseObservation(value=75.5, unit="kg")
    converted_weight = weight_obs.to("g")
    assert pytest.approx(converted_weight) == 75500.0
    
    # Test length conversion
    height_obs = BaseObservation(value=180, unit="cm")
    converted_height = height_obs.to("m")
    assert pytest.approx(converted_height) == 1.8
    
    # Test conversion with unitless observation
    unitless_obs = BaseObservation(value=100)
    with pytest.raises(ValueError):
        unitless_obs.to("kg")

def test_observation_compatibility():
    # Test compatible units
    weight1 = BaseObservation(value=75.5, unit="kg")
    weight2 = BaseObservation(value=165, unit="lb")
    assert weight1.is_compatible_with(weight2)
    
    # Test incompatible units
    weight = BaseObservation(value=75.5, unit="kg")
    height = BaseObservation(value=180, unit="cm")
    assert not weight.is_compatible_with(height)
    
    # Test unitless observations
    unitless1 = BaseObservation(value=100)
    unitless2 = BaseObservation(value=200)
    assert unitless1.is_compatible_with(unitless2)
    
    # Test mixed unitless and unit observation
    assert not unitless1.is_compatible_with(weight)

def test_time_series_observation():
    # Create a series of weight observations
    weight_series = [
        BaseObservation(value=75.5, unit="kg"),
        BaseObservation(value=75.0, unit="kg"),
        BaseObservation(value=74.8, unit="kg")
    ]
    
    # Test basic time series creation
    ts_obs = TimeSeriesObservation(values=weight_series)
    assert len(ts_obs.values) == 3
    assert ts_obs.timestamp is None
    assert ts_obs.metadata is None
    
    # Test time series with metadata
    metadata = {"frequency": "daily", "start_date": "2024-01-01"}
    ts_obs_with_meta = TimeSeriesObservation(
        values=weight_series,
        metadata=metadata
    )
    assert ts_obs_with_meta.metadata == metadata
    assert all(isinstance(obs, BaseObservation) for obs in ts_obs_with_meta.values) 