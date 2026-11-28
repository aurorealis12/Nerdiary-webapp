import io
import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from PIL import Image
from rest_framework.test import APITestCase

from .models import Genre, LibraryEntry, Work

User = get_user_model()


class BaseTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", "alice@example.com", "x")
        self.bob = User.objects.create_user("bob", "bob@example.com", "x")
        self.catalogue = Work.objects.create(title="Dune", media_type="book")
        self.bobs_work = Work.objects.create(title="Bob notes", media_type="book", created_by=self.bob)

    def login(self, user=None):
        self.client.force_authenticate(user or self.alice)

    def titles(self, response):
        return [item["title"] for item in response.data["results"]]


class WorkApiTests(BaseTests):
    def detail(self, work):
        return reverse("work-detail", args=[work.id])

    def test_catalogue_excludes_user_works(self):
        for user in (None, self.alice, self.bob):
            self.client.force_authenticate(user)
            self.assertEqual(self.titles(self.client.get(reverse("work-list"))), ["Dune"])

    def test_guest_cannot_open_user_work(self):
        self.assertEqual(self.client.get(self.detail(self.bobs_work)).status_code, 404)

    def test_logged_in_user_can_open_other_users_work(self):
        self.login()
        response = self.client.get(self.detail(self.bobs_work))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["created_by"], "bob")

    def test_guest_cannot_create_work(self):
        response = self.client.post(reverse("work-list"), {"title": "X", "media_type": "book"})
        self.assertEqual(response.status_code, 403)

    def test_created_work_belongs_to_logged_in_user(self):
        self.login()
        data = {"title": "Mine", "media_type": "movie", "created_by": None}
        response = self.client.post(reverse("work-list"), data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Work.objects.get(title="Mine").created_by, self.alice)
        mine = self.client.get(reverse("work-list"), {"mine": "true"})
        self.assertEqual(self.titles(mine), ["Mine"])

    def test_cannot_change_catalogue_or_other_users_work(self):
        self.login()
        for work in (self.catalogue, self.bobs_work):
            patched = self.client.patch(self.detail(work), {"title": "Hacked"}, format="json")
            self.assertEqual(patched.status_code, 403)
            self.assertEqual(self.client.delete(self.detail(work)).status_code, 403)
        self.assertEqual(Work.objects.filter(title="Hacked").count(), 0)
        self.assertEqual(Work.objects.count(), 2)

    def test_author_can_edit_own_work(self):
        self.login(self.bob)
        response = self.client.patch(self.detail(self.bobs_work), {"description": "New"}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_search_and_filters(self):
        genre = Genre.objects.create(name="Fantasy")
        hobbit = Work.objects.create(title="Hobbit", media_type="movie")
        hobbit.genres.add(genre)
        for params in ({"search": "hob"}, {"media_type": "movie"}, {"genre": genre.id}):
            response = self.client.get(reverse("work-list"), params)
            self.assertEqual(self.titles(response), ["Hobbit"], params)
        invalid = self.client.get(reverse("work-list"), {"genre": "abc"})
        self.assertEqual(invalid.status_code, 400)


class CoverUploadTests(BaseTests):
    def setUp(self):
        super().setUp()
        self.media = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.media, ignore_errors=True)
        override = override_settings(MEDIA_ROOT=self.media)
        override.enable()
        self.addCleanup(override.disable)
        self.login()

    def upload(self, file):
        data = {"title": "With cover", "media_type": "book", "cover": file}
        return self.client.post(reverse("work-list"), data, format="multipart")

    def test_image_is_accepted(self):
        buffer = io.BytesIO()
        Image.new("RGB", (10, 10)).save(buffer, "PNG")
        response = self.upload(SimpleUploadedFile("cover.png", buffer.getvalue(), "image/png"))
        self.assertEqual(response.status_code, 201)
        self.assertIn("/media/covers/", response.data["cover"])

    def test_fake_image_is_rejected(self):
        response = self.upload(SimpleUploadedFile("cover.png", b"not an image", "image/png"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("cover", response.data)


class LibraryApiTests(BaseTests):
    def add(self, work=None, **data):
        payload = {"work": (work or self.catalogue).id, **data}
        return self.client.post(reverse("library-entry-list"), payload, format="json")

    def test_guest_has_no_access(self):
        self.assertEqual(self.client.get(reverse("library-entry-list")).status_code, 403)
        self.assertEqual(self.add().status_code, 403)

    def test_add_entry_with_defaults(self):
        self.login()
        response = self.add(user=self.bob.id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "planned")
        self.assertEqual(response.data["progress"], 0)
        self.assertEqual(LibraryEntry.objects.get().user, self.alice)

    def test_duplicate_is_rejected(self):
        self.login()
        self.add()
        response = self.add()
        self.assertEqual(response.status_code, 400)
        self.assertIn("work", response.data)

    def test_cannot_add_other_users_work(self):
        self.login()
        self.assertEqual(self.add(self.bobs_work).status_code, 400)
        self.assertFalse(LibraryEntry.objects.exists())

    def test_author_can_add_own_work_as_dropped(self):
        self.login(self.bob)
        self.assertEqual(self.add(self.bobs_work, status="dropped").status_code, 201)

    def test_rating_and_progress_limits(self):
        self.login()
        for data in ({"rating": 0}, {"rating": 6}, {"progress": -1}, {"progress": 101}):
            self.assertEqual(self.add(**data).status_code, 400, data)
        self.assertEqual(self.add(rating=5, progress=100).status_code, 201)

    def test_dates_are_checked_on_update(self):
        self.login()
        entry_id = self.add(started_on="2026-05-10").data["id"]
        url = reverse("library-entry-detail", args=[entry_id])
        response = self.client.patch(url, {"finished_on": "2026-05-01"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_work_cannot_be_swapped(self):
        self.login()
        entry_id = self.add().data["id"]
        url = reverse("library-entry-detail", args=[entry_id])
        response = self.client.patch(url, {"work": self.bobs_work.id}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_other_users_entry_cannot_be_changed(self):
        entry = LibraryEntry.objects.create(user=self.bob, work=self.catalogue)
        self.login()
        url = reverse("library-entry-detail", args=[entry.id])
        self.assertEqual(self.client.patch(url, {"rating": 1}, format="json").status_code, 404)
        self.assertEqual(self.client.delete(url).status_code, 404)
        self.assertEqual(self.client.get(reverse("library-entry-list")).data["count"], 0)

    def test_other_users_library_is_read_only_and_hides_email(self):
        LibraryEntry.objects.create(user=self.bob, work=self.bobs_work, review="Great")
        url = reverse("user-library", args=["bob"])
        self.assertEqual(self.client.get(url).status_code, 403)
        self.login()
        response = self.client.get(url)
        self.assertEqual(response.data["results"][0]["review"], "Great")
        self.assertNotIn("bob@example.com", response.content.decode())
        self.assertEqual(self.client.post(url, {}).status_code, 405)

    def test_user_search_hides_email(self):
        self.login()
        response = self.client.get(reverse("user-list"), {"search": "bo"})
        self.assertEqual(response.data["results"], [{"id": self.bob.id, "username": "bob"}])
