from typing import Optional
from application.entities import UserGoalEntity
from application.domain_service import CheckUserGoalsService


class UserGoalsUseCase:
    def __init__(self, user_id: int, action: Optional[str] = None) -> None:
        self.user_id = user_id
        self.action = action if action else "DRINK WATER"
        self.check_user_goals = CheckUserGoalsService
        # self.notifier_adapter = TODO Criar o adapter de notificação

    def execute(self) -> UserGoalEntity:
        self.validate()
        user_goal_entity = self.check_user_goals(user_id=self.user_id, action=self.action).execute()
        return user_goal_entity

    def validate(self): ...
