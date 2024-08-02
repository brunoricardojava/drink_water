import pytest
from unittest.mock import patch
from django.db.models import QuerySet

from rest_framework.serializers import ValidationError
from rest_framework.exceptions import ErrorDetail

from drink_water.serializers import ListUserActionsSerializer
from drink_water.models import UserAction

from application.use_cases import ListUserActionsUseCase

@pytest.mark.django_db
class TestListUserActionsSerializer:
    """Test ListUserActionsSerializer"""

    serializer_to_test = ListUserActionsSerializer

    def test_validate_user_id_valid(self, fixture_user_model):
        user = fixture_user_model
        data = {"user_id": user.id}
        serializer = self.serializer_to_test(data=data)

        assert serializer.is_valid()

    def test_validate_user_id_not_valid(self):
        data = {"user_id": 100}
        serializer = self.serializer_to_test(data=data)

        expected_errors = {'user_id': [ErrorDetail(string='User with id(100) does not exist.', code='invalid')]}
        
        assert serializer.is_valid() == False
        assert serializer.errors == expected_errors
        with pytest.raises(ValidationError):
            assert serializer.is_valid(raise_exception=True)

    @patch.object(ListUserActionsUseCase, "execute")
    def test_create_mehode(self, mock_use_case_execute, fixture_user_model):
        user = fixture_user_model
        user_action_1 = UserAction.objects.create(user=user, action="DRINK WATER", quantity=100)
        user_action_2 = UserAction.objects.create(user=user, action="DRINK WATER", quantity=200)

        user_actions_query_set = UserAction.objects.filter(user=user)
        mock_use_case_execute.return_value = user_actions_query_set

        data = {"user_id": user.id}
        serializer = self.serializer_to_test(data=data)
        if serializer.is_valid():
            object_created = serializer.save()

        assert isinstance(object_created, QuerySet)
        assert len(object_created) == 2
        assert object_created[0] == user_action_1
        assert object_created[1] == user_action_2
