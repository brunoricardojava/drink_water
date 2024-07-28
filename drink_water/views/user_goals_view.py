from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

class UserGoalsView(APIView):
    def get(self, request: Request, user_id: int) -> Response:
        ...
