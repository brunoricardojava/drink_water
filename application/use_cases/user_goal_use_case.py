from application.entities import UserGoalEntity
from application.domain_service import CheckUserGoals

from drink_water.models import User


class UserGoalUseCase:
    def __init__(self, user_id: int, action: str = "DRINK WATER") -> None:
        self.user_id = user_id
        self.action = action
        self.check_user_goals = CheckUserGoals(user_id, action)
        # self.notifier_adapter = TODO Criar o adapter de notificação

    def execute(self) -> UserGoalEntity:
        self.validate()
        user_goal_entity = self.check_user_goals.execute()
        return user_goal_entity

    def validate(self):
        self._check_user_exist()

    def _check_user_exist(self):
        if not User.objects.filter(pk=self.user_id).exists():
            raise User.DoesNotExist()
