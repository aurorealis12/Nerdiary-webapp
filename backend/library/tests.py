import io
import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from PIL import Image
from rest_framework.test import APITestCase

from .models import Genre, LibraryEntry, Recommendation, Tag, Work

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


class TagApiTests(BaseTests):
    def create_tag(self, name):
        return self.client.post(reverse("tag-list"), {"name": name}, format="json")

    def add_entry(self, tags):
        data = {"work": self.catalogue.id, "tags": tags}
        return self.client.post(reverse("library-entry-list"), data, format="json")

    def test_guest_has_no_access(self):
        self.assertEqual(self.client.get(reverse("tag-list")).status_code, 403)
        self.assertEqual(self.create_tag("x").status_code, 403)

    def test_user_sees_only_own_tags(self):
        Tag.objects.create(owner=self.bob, name="Bob tag")
        self.login()
        self.assertEqual(self.create_tag("Favourite").status_code, 201)
        names = [tag["name"] for tag in self.client.get(reverse("tag-list")).data]
        self.assertEqual(names, ["Favourite"])

    def test_names_are_unique_per_user_ignoring_case(self):
        Tag.objects.create(owner=self.bob, name="Cozy")
        self.login()
        self.assertEqual(self.create_tag("Cozy").status_code, 201)
        self.assertEqual(self.create_tag("cozy").status_code, 400)

    def test_cannot_change_other_users_tag(self):
        tag = Tag.objects.create(owner=self.bob, name="Bob tag")
        self.login()
        url = reverse("tag-detail", args=[tag.id])
        self.assertEqual(self.client.patch(url, {"name": "x"}, format="json").status_code, 404)
        self.assertEqual(self.client.delete(url).status_code, 404)

    def test_own_tag_can_be_attached_and_filtered(self):
        tag = Tag.objects.create(owner=self.alice, name="Cozy")
        self.login()
        response = self.add_entry([tag.id])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["tag_names"], ["Cozy"])
        other = Tag.objects.create(owner=self.alice, name="Unused")
        url = reverse("library-entry-list")
        self.assertEqual(self.client.get(url, {"tag": tag.id}).data["count"], 1)
        self.assertEqual(self.client.get(url, {"tag": other.id}).data["count"], 0)
        self.assertEqual(self.client.get(url, {"tag": "abc"}).status_code, 400)

    def test_other_users_tag_cannot_be_attached(self):
        tag = Tag.objects.create(owner=self.bob, name="Bob tag")
        self.login()
        self.assertEqual(self.add_entry([tag.id]).status_code, 400)
        self.assertFalse(LibraryEntry.objects.exists())
        entry_id = self.add_entry([]).data["id"]
        url = reverse("library-entry-detail", args=[entry_id])
        patched = self.client.patch(url, {"tags": [tag.id]}, format="json")
        self.assertEqual(patched.status_code, 400)


class RecommendationApiTests(BaseTests):
    def send(self, recipient="bob", work=None, **data):
        payload = {"recipient": recipient, "work": (work or self.catalogue).id, **data}
        return self.client.post(reverse("recommendation-list"), payload, format="json")

    def received(self):
        """A recommendation from alice to bob, with bob logged in."""
        recommendation = Recommendation.objects.create(
            sender=self.alice, recipient=self.bob, work=self.catalogue
        )
        self.login(self.bob)
        return recommendation

    def url(self, name, recommendation):
        return reverse(f"recommendation-{name}", args=[recommendation.id])

    def test_guest_has_no_access(self):
        self.assertEqual(self.client.get(reverse("recommendation-list")).status_code, 403)
        self.assertEqual(self.send().status_code, 403)

    def test_send_uses_logged_in_user_as_sender(self):
        self.login()
        response = self.send(message="Read it", sender="bob")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Recommendation.objects.get().sender, self.alice)

    def test_invalid_recommendations_are_rejected(self):
        own = Work.objects.create(title="Mine", media_type="book", created_by=self.alice)
        self.login()
        for response in (self.send("alice"), self.send(work=own), self.send("nobody")):
            self.assertEqual(response.status_code, 400)
        self.assertFalse(Recommendation.objects.exists())

    def test_unread_duplicate_is_rejected(self):
        self.login()
        self.assertEqual(self.send().status_code, 201)
        self.assertEqual(self.send().status_code, 400)
        self.assertEqual(Recommendation.objects.count(), 1)

    def test_inbox_and_sent_list(self):
        self.received()
        inbox = self.client.get(reverse("recommendation-list"))
        self.assertEqual(inbox.data["count"], 1)
        self.login(self.alice)
        self.assertEqual(self.client.get(reverse("recommendation-list")).data["count"], 0)
        sent = self.client.get(reverse("recommendation-sent"))
        self.assertEqual(sent.data["results"][0]["recipient"], "bob")
        self.assertNotIn("read_at", sent.data["results"][0])

    def test_mark_as_read(self):
        recommendation = self.received()
        count_url = reverse("recommendation-unread-count")
        self.assertEqual(self.client.get(count_url).data["count"], 1)
        first = self.client.post(self.url("read", recommendation))
        second = self.client.post(self.url("read", recommendation))
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.data["read_at"], second.data["read_at"])
        self.assertEqual(self.client.get(count_url).data["count"], 0)
        unread = self.client.get(reverse("recommendation-list"), {"unread": "true"})
        self.assertEqual(unread.data["count"], 0)

    def test_add_to_library_does_not_duplicate(self):
        recommendation = self.received()
        url = self.url("add-to-library", recommendation)
        self.assertEqual(self.client.post(url).status_code, 201)
        self.assertEqual(self.client.post(url).status_code, 200)
        self.assertEqual(LibraryEntry.objects.filter(user=self.bob).count(), 1)
        recommendation.refresh_from_db()
        self.assertIsNotNone(recommendation.read_at)

    def test_add_to_library_keeps_existing_entry(self):
        LibraryEntry.objects.create(user=self.bob, work=self.catalogue, status="completed")
        recommendation = self.received()
        response = self.client.post(self.url("add-to-library", recommendation))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "completed")

    def test_only_recipient_can_act_on_recommendation(self):
        recommendation = self.received()
        self.login(self.alice)
        self.assertEqual(self.client.post(self.url("read", recommendation)).status_code, 404)
        self.assertEqual(
            self.client.post(self.url("add-to-library", recommendation)).status_code, 404
        )
        self.assertEqual(self.client.delete(self.url("detail", recommendation)).status_code, 404)
        self.login(self.bob)
        self.assertEqual(self.client.delete(self.url("detail", recommendation)).status_code, 204)
