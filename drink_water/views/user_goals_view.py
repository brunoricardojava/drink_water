from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from application.use_cases import UserGoalUseCase

from drink_water.models import User


class UserGoalsView(APIView):
    def get(self, request: Request, user_id: int) -> Response:
        try:
            try:
                user_goal_entity = UserGoalUseCase(user_id).execute()
            except User.DoesNotExist:
                error_message = f"User with id: {user_id}, does not exist."
                error_response = {"detail": error_message}
                return Response(error_response, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(user_goal_entity.model_dump(), status=status.HTTP_200_OK)
        except Exception:
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
