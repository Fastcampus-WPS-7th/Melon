from rest_framework import generics

from utils.pagination import SmallPagination
from ...models import Artist
from ...serializers import ArtistSerializer

__all__ = (
    'ArtistListCreateView',
    'ArtistRetrieveUpdateDestroyView',
)


class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    pagination_class = SmallPagination


class ArtistRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

# 1. 특정 유저의 Token을 생성
# 2. TokenAuthentication을 사용하도록 REST_FRAMEWORK설정
# 3. Postman의 HTTP Header 'Authorization'에
#       Token <value> <- 지정
# 4. 요청 후 request.user가 정상적으로 출력되는지 확인
