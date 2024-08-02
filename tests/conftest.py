from pytest import fixture
from datetime import datetime
from django.utils.timezone import make_aware

from drink_water.models import User, UserAction

from application.entities import UserGoalEntity


@fixture
def fixture_user_model() -> User:
    return User.objects.create(name="UserName", weight=75.0)


@fixture
def fixture_user_action_model(fixture_user_model) -> UserAction:
    return UserAction.objects.create(user=fixture_user_model, action=UserAction.POSSIBLE_ACTIONS[0], quantity=100.0)

@fixture
def fixture_user_goal_entity_completed() -> UserGoalEntity:
    return UserGoalEntity(
        action="DRINK WATER",
        user_goal=100,
        total_quantity=120,
        is_complete_goal=True
    )

@fixture
def fixture_valid_user_action_data(fixture_user_model) -> dict:
    return {
        "user": fixture_user_model.id,
        "action": "DRINK WATER",
        "quantity": 100.0,
        # "created_at": make_aware(datetime(2024, 8, 1)),
        # "updated_at": make_aware(datetime(2024, 8, 1)),
    }
