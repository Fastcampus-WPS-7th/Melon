from rest_framework.views import APIView


class AuthTokenView(APIView):
    def post(self, request):
        # URL: /api/members/auth-token/
        #   members.urls
        #   config.urls에서 include

        # username, password를 받음
        # 유저 인증에 성공했을 경우
        #   authenticate

        # 토큰을 생성하거나 있으면 존재하는걸 가져와서
        #   get_or_create

        # Response로 돌려줌
        pass
