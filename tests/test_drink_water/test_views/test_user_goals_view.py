import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from application.use_cases import UserGoalsUseCase


@pytest.mark.django_db
class TestUserGoalsView:
    """Test UserGoalsView."""

    api_client = APIClient()

    @patch.object(UserGoalsUseCase, "execute")
    def test_valid_data_user_goal_view(
        self, mock_use_case_execute, fixture_user_model, fixture_user_goal_entity_not_completed
    ):
        mock_use_case_execute.return_value = fixture_user_goal_entity_not_completed
        user = fixture_user_model
        url = reverse(viewname="UserGoalRoute", kwargs={"user_id": user.id})
        response = self.api_client.get(path=url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == fixture_user_goal_entity_not_completed.model_dump()

    @patch.object(UserGoalsUseCase, "execute")
    def test_valid_data_completed_goal_user_goal_view(
        self, mock_use_case_execute, fixture_user_model, fixture_user_goal_entity_completed
    ):
        mock_use_case_execute.return_value = fixture_user_goal_entity_completed
        user = fixture_user_model
        url = reverse(viewname="UserGoalRoute", kwargs={"user_id": user.id})
        response = self.api_client.get(path=url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == fixture_user_goal_entity_completed.model_dump()

    def test_invalid_action_user_goal_view(self, fixture_user_model):
        fixture_user_model
        url = reverse(viewname="UserGoalRoute", kwargs={"user_id": 100})
        response = self.api_client.get(path=url, format="json")

        expected_response = {"user_id": [ErrorDetail(string="User with id(100) does not exist.", code="invalid")]}

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == expected_response

    @patch.object(UserGoalsUseCase, "execute")
    def test_internal_error_user_goal_view(self, mock_use_case_execute, fixture_user_model):
        mock_use_case_execute.side_effect = Exception("Error in serializer validation.")
        user = fixture_user_model
        url = reverse(viewname="UserGoalRoute", kwargs={"user_id": user.id})
        response = self.api_client.get(path=url, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {}
