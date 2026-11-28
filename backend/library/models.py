from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class Work(models.Model):
    class MediaType(models.TextChoices):
        BOOK = "book", "Book"
        MOVIE = "movie", "Movie"
        SERIES = "series", "TV series"
        MUSIC = "music", "Music"
        GAME = "game", "Game"
        COMIC = "comic", "Comic"

    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    media_type = models.CharField(max_length=10, choices=MediaType)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    tagline = models.CharField(max_length=255, blank=True)
    # Optional: the frontend must show a placeholder when there is no cover.
    cover = models.ImageField(upload_to="covers/", blank=True)
    # Empty for catalogue works, set for works added by a user.
    # User works are visible to everyone, but only the author can add them to a library.
    # CASCADE: SET_NULL would turn them into catalogue works when the author is deleted.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.CASCADE, related_name="created_works",
    )
    genres = models.ManyToManyField(Genre, blank=True, related_name="works")
    people = models.ManyToManyField(Person, through="Credit", related_name="works")

    def __str__(self):
        return self.title


class Credit(models.Model):
    class Role(models.TextChoices):
        AUTHOR = "author", "Author"
        DIRECTOR = "director", "Director"
        ACTOR = "actor", "Actor"
        ARTIST = "artist", "Artist"
        COMPOSER = "composer", "Composer"
        DEVELOPER = "developer", "Developer"
        OTHER = "other", "Other"

    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="credits")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="credits")
    role = models.CharField(max_length=10, choices=Role)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["work", "person", "role"], name="unique_credit"),
        ]


class MovieDetails(models.Model):
    work = models.OneToOneField(Work, on_delete=models.CASCADE, primary_key=True, related_name="movie")
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)


class BookDetails(models.Model):
    work = models.OneToOneField(Work, on_delete=models.CASCADE, primary_key=True, related_name="book")
    page_count = models.PositiveIntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=255, blank=True)
    volume_number = models.PositiveIntegerField(null=True, blank=True)


class GameDetails(models.Model):
    work = models.OneToOneField(Work, on_delete=models.CASCADE, primary_key=True, related_name="game")
    platforms = models.ManyToManyField(Platform, blank=True, related_name="games")


class SeriesDetails(models.Model):
    work = models.OneToOneField(Work, on_delete=models.CASCADE, primary_key=True, related_name="series")
    season_count = models.PositiveIntegerField(null=True, blank=True)


class Season(models.Model):
    series = models.ForeignKey(SeriesDetails, on_delete=models.CASCADE, related_name="seasons")
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(fields=["series", "number"], name="unique_season_number"),
        ]


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(fields=["season", "number"], name="unique_episode_number"),
        ]


class Franchise(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Collection(models.Model):
    """The `seria` table. Named to avoid confusion with TV series."""

    name = models.CharField(max_length=255)
    kind = models.CharField(max_length=255, blank=True)
    franchises = models.ManyToManyField(Franchise, blank=True, related_name="collections")
    works = models.ManyToManyField(Work, through="CollectionEntry", related_name="collections")

    def __str__(self):
        return self.name


class CollectionEntry(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="entries")
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="collection_entries")
    position = models.CharField(max_length=255, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["collection", "work"], name="unique_collection_work"),
        ]


class Tag(models.Model):
    """A user's own tag. Predefined catalogue tags are stored as genres."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="unique_tag_per_owner"),
        ]

    def __str__(self):
        return self.name


class LibraryEntry(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
        DROPPED = "dropped", "Dropped"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="library_entries")
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="library_entries")
    status = models.CharField(max_length=15, choices=Status, default=Status.PLANNED)
    rating = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    # Percentage, 0 means not started.
    progress = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    review = models.TextField(blank=True)
    # The API must only allow tags owned by the entry's user.
    tags = models.ManyToManyField(Tag, blank=True, related_name="library_entries")
    added_at = models.DateTimeField(auto_now_add=True)
    started_on = models.DateField(null=True, blank=True)
    finished_on = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "work"], name="unique_user_work"),
            models.CheckConstraint(
                condition=Q(rating__isnull=True) | Q(rating__gte=1, rating__lte=5),
                name="rating_between_1_and_5",
            ),
            models.CheckConstraint(condition=Q(progress__lte=100), name="progress_max_100"),
        ]

    def clean(self):
        # Runs in forms and the admin, not on save(). The API must enforce it too.
        super().clean()
        if self.user_id is None or self.work_id is None:
            return
        if self.work.created_by_id not in (None, self.user_id):
            raise ValidationError("You cannot add another user's own work to your library.")


class Recommendation(models.Model):
    """Stays in the recipient's inbox until explicitly deleted."""

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_recommendations")
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_recommendations"
    )
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="recommendations")
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(condition=~Q(sender=models.F("recipient")), name="no_self_recommendation"),
        ]

    def clean(self):
        # Runs in forms and the admin, not on save(). The API must enforce it too.
        super().clean()
        if self.work_id and self.work.created_by_id is not None:
            raise ValidationError({"work": "Only catalogue works can be recommended."})
