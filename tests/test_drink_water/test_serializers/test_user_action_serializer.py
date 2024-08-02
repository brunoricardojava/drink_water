import pytest
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import ErrorDetail

from drink_water.serializers import UserActionSerializer
from drink_water.models import UserAction


@pytest.mark.django_db
class TestUserActionSerializer:
    """Test UserActionSerializer"""

    serializer_to_test = UserActionSerializer

    def test_valid_user_action(self, fixture_valid_user_action_data, fixture_user_model):
        user = fixture_user_model
        serializer = self.serializer_to_test(data=fixture_valid_user_action_data)

        assert serializer.is_valid()
        assert serializer.validated_data.get("user") == user
        assert serializer.validated_data.get("action") == fixture_valid_user_action_data.get("action")
        assert serializer.validated_data.get("quantity") == fixture_valid_user_action_data.get("quantity")

    def test_invalid_user(self, fixture_valid_user_action_data, fixture_user_model):
        user = fixture_user_model
        fixture_valid_user_action_data["user"] = 100
        serializer = self.serializer_to_test(data=fixture_valid_user_action_data)

        expected_errors = {"user": [ErrorDetail(string="Invalid pk \"100\" - object does not exist.", code="does_not_exist")]}

        assert not serializer.is_valid()
        assert serializer.errors == expected_errors
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_action_for_user_action(self, fixture_valid_user_action_data):
        fixture_valid_user_action_data["action"] = "Invalid User action"

        serializer = self.serializer_to_test(data=fixture_valid_user_action_data)
        expected_erros = {"action": [ErrorDetail(string=f"Invalid action. Allowed actions are: ({', '.join(UserAction.POSSIBLE_ACTIONS)})", code="invalid")]}

        assert not serializer.is_valid()
        assert serializer.errors == expected_erros
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_quantity_for_user_action(self, fixture_valid_user_action_data):
        fixture_valid_user_action_data["quantity"] = -10

        serializer = self.serializer_to_test(data=fixture_valid_user_action_data)
        expected_erros = {"quantity": [ErrorDetail(string="The field quantity must be greater than 0.", code="invalid")]}

        assert not serializer.is_valid()
        assert serializer.errors == expected_erros
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
