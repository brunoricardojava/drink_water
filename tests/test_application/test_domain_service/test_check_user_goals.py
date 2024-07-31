import pytest
from unittest.mock import patch, MagicMock

from drink_water.models import User, UserAction

from application.entities import UserGoalEntity
from application.domain_service import CheckUserGoalsService


@pytest.mark.django_db
class TestCheckUserGoalsService:

    service_to_test = CheckUserGoalsService

    @patch.object(CheckUserGoalsService, "_process")
    def test_user_goals_service_return_correct_entity(self, mock_process):
        mock_process.return_value = None
        return_service = self.service_to_test(1, "DRINK WATER", 100, 80, False).execute()

        assert isinstance(return_service, UserGoalEntity)
        assert return_service.action == "DRINK WATER"
        assert return_service.user_goal == 100
        assert return_service.total_quantity == 80
        assert return_service.is_complete_goal == False

    @patch.object(User.objects, "get")
    def test_user_goals_service_correct_calculate_goal(self, mock_user_get):
        mock_user = MagicMock()
        mock_user.weight = 70
        mock_user_get.return_value = mock_user

        instance_service = self.service_to_test(1, "DRINK WATER")
        instance_service._calculate_goal()
        calculated_user_goal = instance_service.goal

        assert calculated_user_goal == 70 * 35

    def test_user_goals_service_correct_get_total_quantity(self, fixture_user_model):
        user = fixture_user_model
        user_action_1 = UserAction.objects.create(user=user, action="DRINK WATER", quantity=100)
        user_action_2 = UserAction.objects.create(user=user, action="DRINK WATER", quantity=200)

        instance_service = self.service_to_test(1, "DRINK WATER")
        instance_service._calculate_total()
        total_user_action_quantity = instance_service.total

        assert total_user_action_quantity == user_action_1.quantity + user_action_2.quantity

    def test_user_complete_goals(self):
        instance_service = self.service_to_test(1, "DRINK WATER")
        instance_service.goal = 100
        instance_service.total = 100

        instance_service._is_complete()

        assert instance_service.complete == True

    def test_user_over_completed_goals(self):
        instance_service = self.service_to_test(1, "DRINK WATER")
        instance_service.goal = 100
        instance_service.total = 1000

        instance_service._is_complete()

        assert instance_service.complete == True

    def test_user_not_completed_goals(self):
        instance_service = self.service_to_test(1, "DRINK WATER")
        instance_service.goal = 100
        instance_service.total = 10

        instance_service._is_complete()

        assert instance_service.complete == False

    def test_user_goals_service_process(self, fixture_user_model):
        user = fixture_user_model
        user_action_1 = UserAction.objects.create(user=user, action="DRINK WATER", quantity=100)
        user_action_2 = UserAction.objects.create(user=user, action="DRINK WATER", quantity=200)
        instance_service = self.service_to_test(user.id, "DRINK WATER")

        instance_service._process()

        assert instance_service.user_id == user.id
        assert instance_service.action == "DRINK WATER"
        assert instance_service.goal == user.weight * 35
        assert instance_service.total == user_action_1.quantity + user_action_2.quantity
        assert instance_service.complete == False
