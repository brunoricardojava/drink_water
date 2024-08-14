from rest_framework import serializers

from drink_water.models import User, UserDataHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["created_at", "updated_at"]

    def validate_weight(self, weight: float) -> float:
        if weight < 0:
            raise serializers.ValidationError("The field weight must be greater than 0.")
        return weight

    def create(self, validated_data):
        instance = super().create(validated_data)
        UserDataHistory.objects.create(user=instance, weight=instance.weight)
        return instance

    def update(self, instance, validated_data):
        if instance.weight != validated_data.get("weight"):
            UserDataHistory.objects.create(user=instance, weight=validated_data.get("weight"))
        instance = super().update(instance, validated_data)
        return instance
