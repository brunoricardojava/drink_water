from rest_framework import serializers

from drink_water.models import User, UserAction


AVAILABLE_GOALS_PERIOD = ["day", "week", "month", "year"]

class UserGoalsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    action = serializers.CharField(required=False)
    period = serializers.CharField(required=False)

    def validate_user_id(self, user_id: int) -> int:
        if not User.objects.filter(pk=user_id).exists():
            raise serializers.ValidationError(f"User with id({user_id}) does not exist.")
        return user_id

    def validate_action(self, action: str) -> str:
        possible_actions_list = UserAction.POSSIBLE_ACTIONS
        if action not in possible_actions_list:
            raise serializers.ValidationError(
                f"Invalid action. Allowed actions are: ({', '.join(possible_actions_list)})"
            )
        return action

    def validate_period(self, period: str) -> str:
        if period not in AVAILABLE_GOALS_PERIOD:
            raise serializers.ValidationError(
                f"Invalid period. Allowed actions are: ({', '.join(AVAILABLE_GOALS_PERIOD)})"
            )
        return period
