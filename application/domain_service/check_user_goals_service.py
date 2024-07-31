from django.db.models.functions import TruncDate
from django.utils import timezone
from django.db.models import Sum

from application.entities import UserGoalEntity

from drink_water.models import User, UserAction


class CheckUserGoalsService:
    def __init__(
            self,
            user_id: int,
            action: str,
            goal: float = None,
            total: float = None,
            complete: bool = None
        ) -> None:
        self.user_id = user_id
        self.action = action
        self.goal = goal
        self.total = total
        self.complete = complete
        self.today = timezone.now().date()

    def execute(self) -> UserGoalEntity:
        self._process()
        return UserGoalEntity(
            action=self.action, user_goal=self.goal, total_quantity=self.total, is_complete_goal=self.complete
        )

    def _process(self) -> None:
        self._calculate_goal()
        self._calculate_total()
        self._is_complete()

    def _calculate_goal(self) -> None:
        user_weight = User.objects.get(pk=self.user_id).weight
        self.goal = user_weight * 35

    def _calculate_total(self) -> None:
        total_quantity_today = (
            UserAction.objects.annotate(date=TruncDate("created_at"))
            .filter(user_id=self.user_id, action=self.action, date=self.today)
            .aggregate(total=Sum("quantity"))
        )
        total = total_quantity_today.get("total")
        self.total = total if total else 0

    def _is_complete(self) -> None:
        self.complete = self.total >= self.goal
