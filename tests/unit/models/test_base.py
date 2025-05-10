import pytest
from owera.models.base import BaseModel

def test_base_model_creation(base_model):
    """Test base model creation."""
    assert base_model.id is None
    assert base_model.created_at is None

def test_base_model_validation(base_model):
    """Test base model validation."""
    base_model.id = 1
    assert base_model.validate() is True

def test_base_model_serialization(base_model):
    """Test base model serialization."""
    base_model.id = 1
    data = base_model.to_dict()
    assert isinstance(data, dict)
    assert "id" in data
    assert data["id"] == 1 