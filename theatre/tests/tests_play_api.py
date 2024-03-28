import os
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from theatre.models import Play, Genre, Actor, TheatreHall, Performance
from theatre.serializers import PlayListSerializer, PlayDetailSerializer

PLAY_URL = reverse("theatre:play-list")
PERFORMANCE_URL = reverse("theatre:performance-list")


def sample_play(**params) -> Play:
    default = {
        "title": "Test Play",
        "description": "Test Description",
    }
    default.update(params)
    return Play.objects.create(**default)


def sample_genre(**params):
    defaults = {
        "name": "Drama",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "George", "last_name": "Clooney"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_performance(**params):
    theatre_hall = TheatreHall.objects.create(
        name="Blue", rows=20, seats_in_row=20
    )

    defaults = {
        "play": None,
        "theatre_hall": theatre_hall,
        "show_time": "2022-06-02 14:00:00",
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


def image_upload_url(play_id):
    """Return URL for recipe image upload"""
    return reverse("theatre:play-upload-image", args=[play_id])


def detail_url(play_id):
    return reverse("theatre:play-detail", args=[play_id])


class UnauthenticatedPlayApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLAY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_plays_list(self):
        sample_play()

        play_with_genre_and_actor = sample_play()

        actor1 = Actor.objects.create(first_name="Test_firstname", last_name="Test_lastname")
        genre1 = Genre.objects.create(name="Test_genre")

        play_with_genre_and_actor.genres.add(genre1)
        play_with_genre_and_actor.actors.add(actor1)
        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        res = self.client.get(PLAY_URL)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_filter_plays_by_title(self):
        play1 = sample_play(title="Test_title1")
        play2 = sample_play(title="Test_title2")

        res = self.client.get(PLAY_URL, {"title": f"{ play1.title}"})

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_list_filter_plays_by_genre(self):
        play1 = sample_play(title="Test_title1")
        play2 = sample_play(title="Test_title2")
        play3 = sample_play(title="Movie without filter")

        genre1 = Genre.objects.create(name="Test_genre1")
        genre2 = Genre.objects.create(name="Test_genre2")

        play1.genres.add(genre1)
        play2.genres.add(genre2)

        res = self.client.get(PLAY_URL,
                              {"genres": f"{genre1.id}, {genre2.id}"})
        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)
        serializer3 = PlayListSerializer(play3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_list_filter_plays_by_actor(self):
        play1 = sample_play(title="Test_title1")
        play2 = sample_play(title="Test_title2")
        play3 = sample_play(title="Movie without filter")

        actor1 = sample_actor(first_name="Test_name1", last_name="Test_surname1")
        actor2 = sample_actor(first_name="Test_name2", last_name="Test_surname2")

        play1.actors.add(actor1)
        play2.actors.add(actor2)

        res = self.client.get(PLAY_URL, {"actors": f"{actor1.id},{actor2.id}"})

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)
        serializer3 = PlayListSerializer(play3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_retrieve_play_detail(self):
        play = sample_play(title="Test_title1")
        play.genres.add(Genre.objects.create(name="Drama"))

        url = detail_url(play.id)

        res = self.client.get(url)

        serializer = PlayDetailSerializer(play)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_play_forbidden(self):
        payload = {"title": "Test_title1",
                   "description": "Test_description"}
        res = self.client.post(PLAY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminPlayAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "testpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_play(self):
        payload = {"title": "Test_title1",
                   "description": "Test_description"}
        res = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=res.data["id"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(play, key))

    def test_create_play_with_genre(self):
        genre1 = sample_genre(name="Test_genre1")
        genre2 = sample_genre(name="Test_genre2")
        payload = {"title": "Test_title1",
                   "description": "Test_description",
                   "genres": [genre1.id, genre2.id]}
        res = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=res.data["id"])
        genres = play.genres.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(genres.count(), 2)
        self.assertIn(genre1, genres)
        self.assertIn(genre2, genres)

    def test_create_play_with_actors(self):
        actor1 = sample_actor(first_name="Test name1", last_name="Test surname1")
        actor2 = sample_actor(first_name="Test name2", last_name="Test surname2")
        payload = {
            "title": "Test",
            "description": "Test desc",
            "actors": [actor1.id, actor2.id]
        }

        res = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=res.data["id"])
        actors = play.actors.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(actors.count(), 2)
        self.assertIn(actor1, actors)
        self.assertIn(actor2, actors)

    def test_delete_play_not_allowed(self):
        play = sample_play()
        url = detail_url(play.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PlayImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.play = sample_play()
        self.genre = sample_genre()
        self.actor = sample_actor()
        self.performance = sample_performance(play=self.play)

    def tearDown(self):
        self.play.image.delete()

    def test_upload_image_to_play(self):
        """Test uploading an image to movie"""
        url = image_upload_url(self.play.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"image": ntf}, format="multipart")
        self.play.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.play.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.play.id)
        res = self.client.post(url, {"image": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_image_to_play_list(self):
        url = PLAY_URL
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url,
                {
                    "title": "Title",
                    "description": "Description",
                    "genres": [1],
                    "actors": [1],
                    "image": ntf,
                },
                format="multipart",
            )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        play = Play.objects.get(title="Title")
        self.assertFalse(play.image)

    def test_image_url_is_shown_on_play_detail(self):
        url = image_upload_url(self.play.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(detail_url(self.play.id))

        self.assertIn("image", res.data)

    def test_image_url_is_shown_on_play_list(self):
        url = image_upload_url(self.play.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(PLAY_URL)

        self.assertIn("image", res.data[0].keys())
