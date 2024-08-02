import pytest
from datetime import datetime, timedelta
from django.db.models import QuerySet
from django.utils.timezone import make_aware, get_current_timezone
from freezegun import freeze_time

from drink_water.models import UserAction

from application.use_cases import ListUserActionsUseCase
from application.entities import ListUserActionsEntity


@pytest.mark.django_db
class TestListUserActionsUseCase:
    """Test ListUserActionsUseCase."""

    use_case_to_test = ListUserActionsUseCase
    tz = get_current_timezone()

    def test_return_type_list_user_actions_use_case(self):
        entity = ListUserActionsEntity(user_id=1)
        instance_use_case = self.use_case_to_test(entity)

        return_queryset_user_action = instance_use_case.execute()

        assert isinstance(return_queryset_user_action, QuerySet)

    def test_execute_use_case_without_date_range(self, fixture_user_model):
        user = fixture_user_model
        UserAction.objects.create(user=user, action="DRINK WATER", quantity=100)
        UserAction.objects.create(user=user, action="DRINK WATER", quantity=200)
        entity = ListUserActionsEntity(user_id=user.id)
        instance_use_case = self.use_case_to_test(entity)

        return_queryset_user_action = instance_use_case.execute()

        assert len(return_queryset_user_action) == 2

    @freeze_time(make_aware(datetime(2024, 7, 31)))
    def test_execute_use_case_with_date_range(self, fixture_user_model):
        user = fixture_user_model
        UserAction.objects.create(user=user, action="DRINK WATER", quantity=100)
        user_action_2 = UserAction.objects.create(user=user, action="DRINK WATER", quantity=200)
        user_action_2.created_at = user_action_2.created_at - timedelta(days=1)
        user_action_2.save()

        start_date_param = make_aware(datetime(2024, 7, 31))
        end_date_param = make_aware(datetime(2024, 8, 1))
        entity = ListUserActionsEntity(user_id=user.id, start_date=start_date_param, end_date=end_date_param)

        instance_use_case = self.use_case_to_test(entity)

        return_queryset_user_action = instance_use_case.execute()

        assert len(return_queryset_user_action) == 1
