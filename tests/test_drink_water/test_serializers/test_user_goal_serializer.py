import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError

from drink_water.serializers import UserGoalsSerializer
from drink_water.models import UserAction


@pytest.mark.django_db
class TestUserGoalSerializer:
    """Test UserGoalSerializer."""

    serializer_to_test = UserGoalsSerializer

    def test_valid_user_goal_data(self, fixture_valid_user_goal_data):
        serializer = self.serializer_to_test(data=fixture_valid_user_goal_data)

        assert serializer.is_valid()
        assert serializer.validated_data == fixture_valid_user_goal_data

    def test_invalid_user_id_for_user_goal(self, fixture_valid_user_goal_data):
        fixture_valid_user_goal_data["user_id"] = 2
        serializer = self.serializer_to_test(data=fixture_valid_user_goal_data)

        expected_errors = {"user_id": [ErrorDetail(string="User with id(2) does not exist.", code="invalid")]}

        assert not serializer.is_valid()
        assert serializer.errors == expected_errors
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_action_for_use_goal(self, fixture_valid_user_goal_data):
        fixture_valid_user_goal_data["action"] = "Invalid User action"
        serializer = self.serializer_to_test(data=fixture_valid_user_goal_data)

        expected_errors = expected_errors = {"action": [ErrorDetail(string=f"Invalid action. Allowed actions are: ({', '.join(UserAction.POSSIBLE_ACTIONS)})", code="invalid")]}

        assert not serializer.is_valid()
        assert serializer.errors == expected_errors
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
