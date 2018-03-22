from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, AccessTokenSerializer


class AuthTokenForFacebookAccessTokenView(APIView):
    def post(self, request):
        # access_token이라는 이름으로 1개의 데이터가 전달됨
        # 해당 데이터를 가지고 AccessTokenSerializer에서 validation
        #   이 과정에서 authenticate가 이루어지며
        #       authenticate에서 페이스북과 통신해서 유저정보를 받아옴
        #   받아온 유저정보와 일치하는 유저가 있으면 해당 유저를, 없으면 생성해서 반환
        # 리턴된 유저는 serializer의 validated_data의 'user'라는 키에 할당
        serializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data)


class AuthTokenView(APIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data)


class MyUserDetail(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
