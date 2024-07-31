from rest_framework import serializers

from application.use_cases import ListUserActionsUseCase
from application.entities import ListUserActionsEntity

from drink_water.models import User


class ListUserActionsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def validate_user_id(self, user_id):
        if not User.objects.filter(pk=user_id).exists():
            raise serializers.ValidationError(f"User with id({user_id}) does not exist.")

        return user_id

    def create(self, validated_data):
        list_user_actions_entity = ListUserActionsEntity(**validated_data)
        return ListUserActionsUseCase(list_user_actions_entity).execute()
