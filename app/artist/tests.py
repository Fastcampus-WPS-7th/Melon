import filecmp
import os
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.temp import NamedTemporaryFile
from django.urls import reverse, resolve
from django.utils.module_loading import import_string
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.test import APITestCase

from artist.serializers import ArtistSerializer
from .apis import ArtistListCreateView
from .models import Artist

User = get_user_model()


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
    PATH = '/api/artist/'
    TEST_ARTIST_NAME = 'Test Artist'

    def test_create_artist(self):
        # /static/test/pby25.jpg에 있는 파일을 사용해서
        # 나머지 데이터를 채워서 Artist객체를 생성

        # 이진데이터 모드로 연 '파일 객체'를
        # 생성할 Artist의 '파일 필드 명'으로 전달
        # self.client.post(URL, {'img_profile': <파일객체>})

        # 테스트용 정적파일을 불러옴
        file_path = os.path.join(settings.STATIC_DIR, 'test', 'pby25.jpg')

        # 유저 토큰인증을 self.client에 추가
        user = User.objects.create_user(username='test_user')
        token = Token.objects.create(user=user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + token.key,
        )

        # with 블록으로 Create(POST)요청
        with open(file_path, 'rb') as f:
            response = self.client.post(self.PATH, {
                'name': self.TEST_ARTIST_NAME,
                'img_profile': f,
            })

        # 생성완료 코드(201)인지 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 1명만 생성되었는지 확인
        self.assertEqual(
            Artist.objects.count(),
            1,
        )
        # 지정한 username으로 생성되었는지 확인
        self.assertEqual(
            Artist.objects.first().name,
            self.TEST_ARTIST_NAME,
        )

        artist = Artist.objects.first()
        # Artist인스턴스에 지정되어있는 파일과
        #   -> DEFAULT_FILE_STORAGE를 사용해 저장된 파일

        # FieldFile
        # uploaded_file = default_storage.open(
        #     artist.img_profile.name
        # )
        # 파일을 읽어서 파일시스템상의 임시파일을 생성
        with NamedTemporaryFile() as temp_file:
            temp_file.write(artist.img_profile.read())
            # temp_file.write(uploaded_file.read())
            # 생성한 임시파일의 경로 (temp_file.name)와
            # 테스트용 정적파일의 경로 (file_path)를 이용해서
            # 같은 파일인지 비교
            print('file_path:', file_path)
            print('temp_file.name:', temp_file.name)
            self.assertTrue(filecmp.cmp(file_path, temp_file.name))
