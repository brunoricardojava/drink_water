import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError

from drink_water.serializers import UserSerializer


@pytest.mark.django_db
class TestUserSerializer:
    """Test UserSerializer"""

    serializer_to_test = UserSerializer

    def test_valid_user_data(self, fixture_valid_user_data):
        serializer = self.serializer_to_test(data=fixture_valid_user_data)

        assert serializer.is_valid()
        assert serializer.validated_data == fixture_valid_user_data

    def test_invalid_weight_for_user(self, fixture_valid_user_data):
        fixture_valid_user_data["weight"] = -10
        serializer = self.serializer_to_test(data=fixture_valid_user_data)

        expected_erros = {"weight": [ErrorDetail(string="The field weight must be greater than 0.", code="invalid")]}

        assert not serializer.is_valid()
        assert serializer.errors == expected_erros
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
