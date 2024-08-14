from datetime import date, timedelta

from django.db.models.functions import TruncDate
from django.utils import timezone
from django.db.models import Sum

from application.entities import UserGoalEntity, UserGoalEntityList

from drink_water.models import User, UserAction, UserDataHistory


class CheckUserGoalsService:
    def __init__(
        self, user_id: int, action: str, period: str = None
    ) -> None:
        self.user_id = user_id
        self.action = action
        self.period = period
        self.today = timezone.now().date()

    def execute(self) -> UserGoalEntity:
        return self._process()

    def _process(self) -> None:
        days_number = self._get_days_for_period()
        goals_list = []

        for day in range(days_number):
            date = self.today - timedelta(days=day)
            goal = self._calculate_goal(date)
            total = self._calculate_total(date)
            completed = self._is_complete(total, goal)
            user_goal_entity = UserGoalEntity(date=date, action=self.action, user_goal=goal, total_quantity=total, is_complete_goal=completed)
            goals_list.append(user_goal_entity)

        return UserGoalEntityList(items=goals_list)

    def _get_days_for_period(self) -> int:
        definition = {"day": 1, "week": 7, "month": 30}
        return definition.get(self.period)

    def _calculate_goal(self, date) -> float:
        user_weight = self._get_user_weight(date)
        return user_weight * 35

    def _get_user_weight(self, date) -> float:
        # date = date + timedelta(days=1)
        user_history = (
            UserDataHistory.objects.annotate(date=TruncDate("created_at"))
            .filter(user_id=self.user_id, date=date)
            .order_by("-created_at").first()
        )
        if not user_history:
            weight = User.objects.get(pk=self.user_id).weight
        else:
            weight = user_history.weight
        return weight

    def _calculate_total(self, date: date) -> float:
        total_quantity_today = (
            UserAction.objects.annotate(date=TruncDate("created_at"))
            .filter(user_id=self.user_id, action=self.action, date=date)
            .aggregate(total=Sum("quantity"))
        )
        total = total_quantity_today.get("total")
        return  total if total else 0

    def _is_complete(self, total, goal) -> bool:
        return total >= goal
