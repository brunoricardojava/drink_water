from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from drink_water.models import UserAction
from drink_water.serializers import UserActionSerializer


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
            paginator = LimitOffsetPagination()
            user_actions = UserAction.objects.filter(user_id= user_id).order_by("-created_at")
            paginated_user_actions = paginator.paginate_queryset(user_actions, request)
            serializer = UserActionSerializer(paginated_user_actions, many=True)
            return paginator.get_paginated_response(serializer.data)
        except:
            return Response({}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
