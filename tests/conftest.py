from pytest import fixture

from drink_water.models import User, UserAction


@fixture
def fixture_user_model():
    return User.objects.create(name="UserName", weight=75.0)


@fixture
def fixture_user_action_model(fixture_user_model):
    return UserAction.objects.create(user=fixture_user_model, action=UserAction.POSSIBLE_ACTIONS[0], quantity=100.0)
