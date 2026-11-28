from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from rest_framework import serializers

from .models import Credit, Genre, LibraryEntry, Work

MAX_COVER_SIZE = 5 * 1024 * 1024


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class PublicUserSerializer(serializers.ModelSerializer):
    """What other users may see. Never add the email here."""

    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class CreditSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source="person")

    class Meta:
        model = Credit
        fields = ["name", "role"]


class WorkSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field="username", read_only=True)
    genres = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Genre.objects.all())
    genre_names = serializers.StringRelatedField(source="genres", many=True, read_only=True)
    credits = CreditSerializer(many=True, read_only=True)

    class Meta:
        model = Work
        fields = [
            "id", "title", "original_title", "media_type", "release_date", "description",
            "tagline", "cover", "genres", "genre_names", "credits", "created_by",
        ]

    def validate_cover(self, value):
        if value and value.size > MAX_COVER_SIZE:
            raise serializers.ValidationError("The cover cannot be larger than 5 MB.")
        return value


class WorkSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ["id", "title", "media_type", "cover"]


class LibraryEntrySerializer(serializers.ModelSerializer):
    work_detail = WorkSummarySerializer(source="work", read_only=True)

    class Meta:
        model = LibraryEntry
        fields = [
            "id", "work", "work_detail", "status", "rating", "progress", "review",
            "added_at", "started_on", "finished_on",
        ]
        # The user is not a request field, so uniqueness is checked in validate_work().
        validators = []

    def validate_work(self, work):
        if self.instance:
            if work != self.instance.work:
                raise serializers.ValidationError("The work of an entry cannot be changed.")
            return work
        user = self.context["request"].user
        if work.created_by_id not in (None, user.id):
            raise serializers.ValidationError("You cannot add another user's own work to your library.")
        if LibraryEntry.objects.filter(user=user, work=work).exists():
            raise serializers.ValidationError("This work is already in your library.")
        return work

    def validate(self, attrs):
        started = attrs.get("started_on", getattr(self.instance, "started_on", None))
        finished = attrs.get("finished_on", getattr(self.instance, "finished_on", None))
        if started and finished and finished < started:
            raise serializers.ValidationError(
                {"finished_on": "The finish date cannot be before the start date."}
            )
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            # Another request added the same work after validation.
            raise serializers.ValidationError({"work": "This work is already in your library."})
