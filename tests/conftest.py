from pytest import fixture

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
    return UserGoalEntity(action="DRINK WATER", user_goal=100, total_quantity=120, is_complete_goal=True)


@fixture
def fixture_valid_user_action_data(fixture_user_model) -> dict:
    return {
        "user": fixture_user_model.id,
        "action": "DRINK WATER",
        "quantity": 100.0,
    }


@fixture
def fixture_valid_user_action_data_for_post_view() -> dict:
    return {
        "action": "DRINK WATER",
        "quantity": 100.0,
    }


@fixture
def fixture_valid_user_actio_data_for_get_view() -> dict:
    return {
        "start_date": ["2024-07-31"],
        "end_date": ["2024-08-01"],
    }


@fixture
def fixture_valid_user_goal_data(fixture_user_model) -> dict:
    return {
        "user_id": fixture_user_model.id,
        "action": "DRINK WATER",
    }


@fixture
def fixture_valid_user_data() -> dict:
    return {
        "name": "bruno",
        "weight": 75.0,
    }
