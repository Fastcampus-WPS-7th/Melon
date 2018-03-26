import random

from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase

from artist.serializers import ArtistSerializer
from .apis import ArtistListCreateView
from .models import Artist


class ArtistListTest(APITestCase):
    MODEL = Artist
    VIEW = ArtistListCreateView
    PATH = '/api/artist/'
    VIEW_NAME = 'apis:artist:artist-list'
    PAGINATION_COUNT = 5

    def test_reverse(self):
        f"""
        Artist List에 해당하는 VIEW_NAME을 reverse한 결과가 기대 PATH와 같은지 검사
            VIEW_NAME: {self.VIEW_NAME}
            PATH:      {self.PATH}
        :return:
        """
        self.assertEqual(reverse(self.VIEW_NAME), self.PATH)

    def test_resolve(self):
        f"""
        Artist List에 해당하는 PATH를 resolve한 결과의 func와 view_name이
        기대하는 View.as_view()와 VIEW_NAME과 같은지 검사
            PATH:       {self.PATH}
            VIEW_NAME:  {self.VIEW_NAME}
        :return:
        """
        resolver_match = resolve(self.PATH)
        self.assertEqual(
            resolver_match.func.__name__,
            self.VIEW.as_view().__name__,
        )
        self.assertEqual(
            resolver_match.view_name,
            self.VIEW_NAME,
        )

    def test_artist_list_count(self):
        num = random.randrange(10, 20)
        for i in range(num):
            Artist.objects.create(name=f'Artist{i}')

        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['count'],
            self.MODEL.objects.count(),
        )
        self.assertEqual(
            response.data['count'],
            num,
        )

    def test_artist_list_pagination(self):
        # math.ceil <- 소수점 올림
        num = 13
        for i in range(num):
            Artist.objects.create(name=f'Artist{i + 1}')
        response = self.client.get(self.PATH, {'page': 1})

        # 응답코드 200 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # for문을 사용해서, 아래의 로직이
        #   페이지네이션 된 모든 page들에 요청 후 results값을 확인하도록 구성

        # 'results'키에 5개의 데이터가 배열로 전달되는지 확인
        self.assertEqual(
            len(response.data['results']),
            self.PAGINATION_COUNT,
        )
        # 'results'키에 들어있는 5개의 Artist가 serialize되어있는 결과가
        # 실제 QuerySet을 serialize한 결과와 같은지 확인
        self.assertEqual(
            response.data['results'],
            ArtistSerializer(Artist.objects.all()[:5], many=True).data,
        )


class ArtistCreateTest(APITestCase):
    def test_create_artist(self):
        # /static/test/pby25.jpg에 있는 파일을 사용해서
        # 나머지 데이터를 채워서 Artist객체를 생성
        # 이진데이터 모드로 연 '파일 객체'를
        # 생성할 Artist의 '파일 필드 명'으로 전달
        # self.client.post(URL, {'img_profile': <파일객체>})
        pass
