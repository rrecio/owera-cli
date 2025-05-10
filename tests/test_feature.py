"""Tests for the Feature model."""

import pytest
from owera.models import Feature

def test_feature_creation():
    """Test creating a new feature."""
    feature = Feature(
        name="test-feature",
        description="A test feature",
        constraints=["secure", "responsive"],
        status="planned",
        priority=1
    )
    
    assert feature.name == "test-feature"
    assert feature.description == "A test feature"
    assert feature.constraints == ["secure", "responsive"]
    assert feature.status == "planned"
    assert feature.priority == 1

def test_feature_validation():
    """Test feature validation."""
    # Test missing name
    with pytest.raises(ValueError, match="Feature must have a name"):
        Feature(name="", description="A test feature")
    
    # Test missing description
    with pytest.raises(ValueError, match="Feature must have a description"):
        Feature(name="test-feature", description="")
    
    # Test invalid constraints
    with pytest.raises(ValueError, match="Constraints must be a list"):
        Feature(
            name="test-feature",
            description="A test feature",
            constraints="not a list"
        )
    
    # Test invalid priority
    with pytest.raises(ValueError, match="Priority must be an integer"):
        Feature(
            name="test-feature",
            description="A test feature",
            priority="not an integer"
        )
    
    # Test priority out of range
    with pytest.raises(ValueError, match="Priority must be between 1 and 5"):
        Feature(
            name="test-feature",
            description="A test feature",
            priority=0
        )
    
    with pytest.raises(ValueError, match="Priority must be between 1 and 5"):
        Feature(
            name="test-feature",
            description="A test feature",
            priority=6
        )
    
    # Test invalid status
    with pytest.raises(ValueError, match="Status must be one of"):
        Feature(
            name="test-feature",
            description="A test feature",
            status="invalid"
        )

def test_feature_serialization():
    """Test feature serialization."""
    feature = Feature(
        name="test-feature",
        description="A test feature",
        constraints=["secure", "responsive"],
        status="planned",
        priority=1
    )
    
    # Convert to dictionary
    feature_dict = feature.to_dict()
    
    assert feature_dict["name"] == feature.name
    assert feature_dict["description"] == feature.description
    assert feature_dict["constraints"] == feature.constraints
    assert feature_dict["status"] == feature.status
    assert feature_dict["priority"] == feature.priority
    
    # Create from dictionary
    new_feature = Feature(**feature_dict)
    
    assert new_feature.name == feature.name
    assert new_feature.description == feature.description
    assert new_feature.constraints == feature.constraints
    assert new_feature.status == feature.status
    assert new_feature.priority == feature.priority 