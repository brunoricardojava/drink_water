import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from drink_water.models import User
from drink_water.serializers import UserSerializer


@pytest.mark.django_db
class TestUserView:
    """Test UserView"""

    api_client = APIClient()

    def test_post_valid_data_user_view(self, fixture_valid_user_data):
        url = reverse(viewname="UserRoute")
        response = self.api_client.post(path=url, data=fixture_valid_user_data, format="json")

        expected_response = {'id': 1, 'name': 'bruno', 'weight': 75.0}

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data == expected_response
        assert User.objects.filter(id=response.data.get("id")).exists()

    def test_post_invalid_user_weight_data_for_user_view(self, fixture_valid_user_data):
        fixture_valid_user_data["weight"] = -10
        url = reverse(viewname="UserRoute")
        response = self.api_client.post(path=url, data=fixture_valid_user_data, format="json")

        expected_error = {'weight': [ErrorDetail(string='The field weight must be greater than 0.', code='invalid')]}

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == expected_error

    @patch.object(UserSerializer, "save")
    def test_internal_error_user_view(self, mock_serializer_save, fixture_valid_user_data):
        mock_serializer_save.side_effect = Exception("Erro serializer save")
        url = reverse(viewname="UserRoute")
        response = self.api_client.post(path=url, data=fixture_valid_user_data, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {}
