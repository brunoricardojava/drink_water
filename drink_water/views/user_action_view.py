from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from drink_water.models import User
from drink_water.serializers import UserActionSerializer, ListUserActionsSerializer


class UserActionView(APIView):
    def post(self, request: Request, user_id: int) -> Response:
        try:
            data = {"user": user_id, **request.data.copy()}
            serializer = UserActionSerializer(data= data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except:
            return Response({}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request: Request, user_id: int) -> Response:
        try:
            query_params = {key: request.query_params.get(key) for key in request.query_params}
            data = {"user_id": user_id, **query_params}
            serializer = ListUserActionsSerializer(data= data)
            if serializer.is_valid():
                user_actions = serializer.save()
                paginator = LimitOffsetPagination()
                paginated_user_actions = paginator.paginate_queryset(user_actions, request)
                serializer = UserActionSerializer(paginated_user_actions, many=True)
                return paginator.get_paginated_response(serializer.data)
            else:
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            error_message = f"User with id: {user_id}, does not exist."
            error_response = {"detail": error_message}
            return Response(error_response, status= status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
