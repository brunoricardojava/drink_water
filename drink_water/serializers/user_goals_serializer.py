from rest_framework import serializers

from drink_water.models import User


class UserGoalsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, user_id):
        if not User.objects.filter(pk=user_id).exists():
            raise serializers.ValidationError(f"User with id({user_id}) does not exist.")

        return user_id
