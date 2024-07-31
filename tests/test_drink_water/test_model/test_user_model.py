import pytest
from datetime import datetime


@pytest.mark.django_db
class TestUserModel:
    """Test User model"""

    def test_fields_user_model(self, fixture_user_model):
        user_model = fixture_user_model

        assert isinstance(user_model.created_at, datetime)
        assert isinstance(user_model.updated_at, datetime)
        assert isinstance(user_model.name, str)
        assert isinstance(user_model.weight, float)

    def test_representer_user_model(self, fixture_user_model):
        user_model = fixture_user_model

        assert user_model.__str__() == f"{user_model.name} - {user_model.id}"
