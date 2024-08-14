from typing import Optional
from application.entities import UserGoalEntityList
from application.domain_service import CheckUserGoalsService


class UserGoalsUseCase:
    def __init__(self, user_id: int, action: Optional[str] = None, period: Optional[str] = None) -> None:
        self.user_id = user_id
        self.action = action if action else "DRINK WATER"
        self.period = period if period else "day"
        self.check_user_goals = CheckUserGoalsService
        # self.notifier_adapter = TODO Criar o adapter de notificação

    def execute(self) -> UserGoalEntityList:
        self.validate()
        user_goal_entity_list = self.check_user_goals(user_id=self.user_id, action=self.action, period=self.period).execute()
        return user_goal_entity_list

    def validate(self): ...
