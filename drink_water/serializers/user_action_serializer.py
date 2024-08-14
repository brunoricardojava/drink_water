from rest_framework import serializers

from drink_water.models import UserAction


class UserActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAction
        exclude = ["updated_at"]

    def validate_action(self, action: str) -> str:
        possible_actions_list = UserAction.POSSIBLE_ACTIONS
        if action not in possible_actions_list:
            raise serializers.ValidationError(
                f"Invalid action. Allowed actions are: ({', '.join(possible_actions_list)})"
            )
        return action

    def validate_quantity(self, quantity: float) -> float:
        if quantity <= 0:
            raise serializers.ValidationError("The field quantity must be greater than 0.")
        return quantity
