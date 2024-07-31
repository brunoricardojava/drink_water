import pytest
from datetime import datetime
from django.utils import timezone


@pytest.mark.django_db
class TestBaseModel:
    """Test base model"""

    NOW = timezone.now()

    def test_created_at_auto_now_add(self, fixture_user_model):
        user_model = fixture_user_model

        assert isinstance(user_model.created_at, datetime)
        assert user_model.created_at > self.NOW

    def test_update_at_auto_now(self, fixture_user_model):
        user_model = fixture_user_model
        user_model.name = "Updated Name"
        user_model.save()

        assert user_model.name == "Updated Name"
        assert isinstance(user_model.updated_at, datetime)
        assert user_model.updated_at > user_model.created_at
