from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from application.use_cases import UserGoalUseCase

from drink_water.serializers import UserGoalsSerializer
from drink_water.models import User


class UserGoalsView(APIView):
    def get(self, request: Request, user_id: int) -> Response:
        try:
            data = {"user_id": user_id}
            serializer = UserGoalsSerializer(data=data)
            if serializer.is_valid():
                user_goal_entity = UserGoalUseCase(serializer.validated_data.get("user_id")).execute()
                return Response(user_goal_entity.model_dump(), status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
