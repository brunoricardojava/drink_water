import operator
from functools import reduce
from typing import Any
from django.db.models import QuerySet, Q
from django.utils import timezone

from application.entities import ListUserActionsEntity

from drink_water.models import UserAction


class ListUserActionsUseCase:

    def __init__(self, entity: ListUserActionsEntity) -> None:
        self.entity = entity
        self.today = timezone.now().date()

    def execute(self) -> QuerySet:
        return self._process()

    def _process(self) -> QuerySet:
        filter_specification = self._build_filter_specification()
        order_specification = "-created_at"
        return UserAction.objects.filter(filter_specification).order_by(order_specification)

    def _build_filter_specification(self) -> tuple:
        conditions = [self._user_action_condition(), self._data_range_condition()]
        return self._and_concat_specifications(conditions)

    def _user_action_condition(self) -> Q:
        return Q(user=self.entity.user_id)

    def _data_range_condition(self) -> Q:
        start_date = self.entity.start_date
        end_date = self.entity.end_date
        if start_date and end_date:
            return Q(created_at__gte=start_date, created_at__lte=end_date)
        else:
            return Q()

    @staticmethod
    def _and_concat_specifications(conditions=None) -> Any:
        conditions = [] if conditions is None else conditions
        return reduce(operator.and_, (condition for condition in conditions)) if len(conditions) > 0 else None
