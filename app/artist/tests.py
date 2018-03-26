import random

from django.urls import reverse, resolve
from rest_framework.test import APITestCase

from .apis import ArtistListCreateView
from .models import Artist


class ArtistListTest(APITestCase):
    MODEL = Artist
    VIEW = ArtistListCreateView
    PATH = '/api/artist/'
    VIEW_NAME = 'apis:artist:artist-list'

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
        num = random.randrange(1, 10)
        for i in range(num):
            Artist.objects.create(name=f'Artist{i}')

        response = self.client.get(self.PATH)
        self.assertEqual(
            response.data['count'],
            self.MODEL.objects.count(),
        )
        self.assertEqual(
            response.data['count'],
            num,
        )

    def test_artist_list_pagination(self):
        # artist-list요청시 pagination이 잘 적용되어있는지 테스트
        pass
