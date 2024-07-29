from rest_framework import serializers

from lib.use_cases import ListUserActionsUseCase
from lib.entities import ListUserActionsEntity


class ListUserActionsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def create(self, validated_data):
        list_user_actions_entity = ListUserActionsEntity(**validated_data)
        return ListUserActionsUseCase(list_user_actions_entity).execute()
