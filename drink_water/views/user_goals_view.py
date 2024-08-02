from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from application.use_cases import UserGoalUseCase

from drink_water.serializers import UserGoalsSerializer


class UserGoalsView(APIView):
    def get(self, request: Request, user_id: int) -> Response:
        try:
            query_params = {key: request.query_params.get(key) for key in request.query_params}
            data = {"user_id": user_id, **query_params}
            serializer = UserGoalsSerializer(data=data)
            if serializer.is_valid():
                user_id = serializer.validated_data.get("user_id")
                action = serializer.validated_data.get("action")
                user_goal_entity = UserGoalUseCase(user_id, action).execute()
                return Response(user_goal_entity.model_dump(), status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
