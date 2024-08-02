import pytest
from django.urls import reverse
from unittest.mock import patch
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
from rest_framework import status

from drink_water.views import UserActionView
from drink_water.models import UserAction
from drink_water.serializers import UserActionSerializer, ListUserActionsSerializer


@pytest.mark.django_db
class TestUserActionView:
    """Test UserActionView."""

    view_to_test = UserActionView
    api_client = APIClient()

    def test_post_valid_data(self, fixture_user_model, fixture_valid_user_action_data_for_post_view):
        user = fixture_user_model
        url = reverse("UserActionRoute", kwargs={"user_id": user.id})
        response = self.api_client.post(path=url, data=fixture_valid_user_action_data_for_post_view, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["action"] == fixture_valid_user_action_data_for_post_view["action"]
        assert response.data["quantity"] == fixture_valid_user_action_data_for_post_view["quantity"]

    def test_post_invalid_user(self, fixture_user_model, fixture_valid_user_action_data_for_post_view):
        fixture_user_model
        url = reverse("UserActionRoute", kwargs={"user_id": "100"})
        response = self.api_client.post(path=url, data=fixture_valid_user_action_data_for_post_view, format="json")
        expected_error_response = {
            "user": [ErrorDetail(string='Invalid pk "100" - object does not exist.', code="does_not_exist")]
        }

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == expected_error_response

    def test_post_invalid_user_action_data(self, fixture_user_model, fixture_valid_user_action_data_for_post_view):
        user = fixture_user_model
        fixture_valid_user_action_data_for_post_view["action"] = "Invalid action"
        url = reverse("UserActionRoute", kwargs={"user_id": user.id})
        response = self.api_client.post(path=url, data=fixture_valid_user_action_data_for_post_view, format="json")
        expected_error_response = {
            "action": [
                ErrorDetail(
                    string=f"Invalid action. Allowed actions are: ({', '.join(UserAction.POSSIBLE_ACTIONS)})",
                    code="invalid",
                )
            ]
        }

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == expected_error_response

    def test_post_invalid_quantity_data(self, fixture_user_model, fixture_valid_user_action_data_for_post_view):
        user = fixture_user_model
        fixture_valid_user_action_data_for_post_view["quantity"] = -10
        url = reverse("UserActionRoute", kwargs={"user_id": user.id})
        response = self.api_client.post(path=url, data=fixture_valid_user_action_data_for_post_view, format="json")
        expected_error_response = {
            "quantity": [ErrorDetail(string="The field quantity must be greater than 0.", code="invalid")]
        }

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == expected_error_response

    @patch.object(UserActionSerializer, "save")
    def test_post_internal_server_error(
        self, mock_serializer_save, fixture_user_model, fixture_valid_user_action_data_for_post_view
    ):
        mock_serializer_save.side_effect = Exception("Error serializer save")
        user = fixture_user_model
        url = reverse("UserActionRoute", kwargs={"user_id": user.id})
        response = self.api_client.post(path=url, data=fixture_valid_user_action_data_for_post_view, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {}

    def test_get_valid_data_without_user_actions(self, fixture_user_model):
        user = fixture_user_model
        url = reverse("UserActionRoute", kwargs={"user_id": user.id})
        response = self.api_client.get(path=url, format="json")

        expected_response = {"count": 0, "next": None, "previous": None, "results": []}

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_response

    def test_get_valid_data_with_user_actions(self, fixture_user_model):
        user = fixture_user_model
        user_actio_1 = UserAction.objects.create(user=user, action="DRINK WATER", quantity=100)
        user_actio_2 = UserAction.objects.create(user=user, action="DRINK WATER", quantity=200)
        url = reverse("UserActionRoute", kwargs={"user_id": user.id})
        response = self.api_client.get(path=url, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("count") == 2
        assert response.data.get("next") is None
        assert response.data.get("previus") is None
        assert len(response.data.get("results")) == 2
        assert response.data.get("results")[0].get("id") == user_actio_2.id
        assert response.data.get("results")[0].get("user") == user_actio_2.user_id
        assert response.data.get("results")[0].get("quantity") == user_actio_2.quantity
        assert response.data.get("results")[1].get("id") == user_actio_1.id
        assert response.data.get("results")[1].get("user") == user_actio_1.user_id
        assert response.data.get("results")[1].get("quantity") == user_actio_1.quantity

    def test_get_invalid_user(self, fixture_user_model):
        fixture_user_model
        url = reverse("UserActionRoute", kwargs={"user_id": "100"})
        response = self.api_client.get(path=url, format="json")
        expected_error_response = {"user_id": [ErrorDetail(string="User with id(100) does not exist.", code="invalid")]}

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == expected_error_response

    @patch.object(ListUserActionsSerializer, "save")
    def test_get_internal_server_error(self, mock_serializer_save, fixture_user_model):
        mock_serializer_save.side_effect = Exception("Error serializer")
        user = fixture_user_model
        url = reverse("UserActionRoute", kwargs={"user_id": user.id})
        response = self.api_client.get(path=url, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {}
