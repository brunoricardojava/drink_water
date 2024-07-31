import pytest
from datetime import datetime

from drink_water.models import User, UserAction


@pytest.mark.django_db
class TestUserActionModel:
    """Test UserAction model"""

    def test_fields_user_action_model(self, fixture_user_action_model):
        user_action_model = fixture_user_action_model

        assert isinstance(user_action_model.created_at, datetime)
        assert isinstance(user_action_model.updated_at, datetime)
        assert isinstance(user_action_model.user, User)
        assert isinstance(user_action_model.action, str)
        assert isinstance(user_action_model.quantity, float)

    def test_possibles_actions_of_use_action_model(self):
        possibles = ["DRINK WATER"]
        model_possibles = UserAction.POSSIBLE_ACTIONS

        assert set(possibles) == set(model_possibles)
