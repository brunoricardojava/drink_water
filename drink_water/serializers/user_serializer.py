from rest_framework import serializers

from drink_water.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate_weight(self, weight: float) -> float:
        if weight <= 0:
            raise serializers.ValidationError("The field weight must be greater than 0.")
        return weight
