from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from drink_water.serializers import UserSerializer as user_serializer

class UserCreateView(APIView):

    def post(self, request: Request) -> Response:
        try:
            serializer = user_serializer(data={**request.data.copy()})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except:
            return Response({}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
