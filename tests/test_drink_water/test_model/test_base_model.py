import pytest
from django.utils import timezone

from drink_water.models import User


class TestModelUser:
    """Test model User"""

    @pytest.mark.django_db()
    def test_base_model_created_at(self):
        instance = User.objects.create(name="Test", weight=75)
        assert instance.created_at is not None
        assert instance.updated_at is not None
        assert instance.created_at <= timezone.now()
