import pytest
from unittest.mock import patch

from application.use_cases import UserGoalsUseCase
from application.entities import UserGoalEntity
from application.domain_service import CheckUserGoalsService


@pytest.mark.django_db
class TestUserGoalsUseCase:
    """Test UserGoalsUseCase"""

    use_case_to_test = UserGoalsUseCase

    @patch.object(CheckUserGoalsService, "execute")
    def test_return_type_use_case(self, mock_service_execute, fixture_user_goal_entity_completed):
        mock_service_execute.return_value = fixture_user_goal_entity_completed

        instance_use_case = self.use_case_to_test(user_id=1)
        return_entity_response = instance_use_case.execute()

        assert isinstance(return_entity_response, UserGoalEntity)
