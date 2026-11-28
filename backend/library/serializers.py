from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from rest_framework import serializers

from .models import Credit, Genre, LibraryEntry, Recommendation, Tag, Work

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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        # The owner is not a request field, so uniqueness is checked in validate_name().
        validators = []

    def validate_name(self, value):
        tags = Tag.objects.filter(owner=self.context["request"].user, name__iexact=value)
        if self.instance:
            tags = tags.exclude(pk=self.instance.pk)
        if tags.exists():
            raise serializers.ValidationError("You already have a tag with this name.")
        return value


class OwnTagField(serializers.PrimaryKeyRelatedField):
    """Accepts only tags owned by the logged-in user."""

    def get_queryset(self):
        request = self.context.get("request")
        return Tag.objects.filter(owner_id=request.user.id if request else None)


class LibraryEntrySerializer(serializers.ModelSerializer):
    work_detail = WorkSummarySerializer(source="work", read_only=True)
    tags = OwnTagField(many=True, required=False)
    tag_names = serializers.StringRelatedField(source="tags", many=True, read_only=True)

    class Meta:
        model = LibraryEntry
        fields = [
            "id", "work", "work_detail", "status", "rating", "progress", "review",
            "added_at", "started_on", "finished_on", "tags", "tag_names",
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


class RecommendationSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field="username", read_only=True)
    recipient = serializers.SlugRelatedField(
        slug_field="username", queryset=get_user_model().objects.filter(is_active=True)
    )
    work_detail = WorkSummarySerializer(source="work", read_only=True)
    message = serializers.CharField(required=False, allow_blank=True, max_length=500)

    class Meta:
        model = Recommendation
        fields = [
            "id", "sender", "recipient", "work", "work_detail", "message",
            "created_at", "read_at",
        ]
        read_only_fields = ["created_at", "read_at"]

    def validate_recipient(self, recipient):
        if recipient == self.context["request"].user:
            raise serializers.ValidationError("You cannot send a recommendation to yourself.")
        return recipient

    def validate_work(self, work):
        if work.created_by_id is not None:
            raise serializers.ValidationError("Only catalogue works can be recommended.")
        return work

    def validate(self, attrs):
        # Stops accidental repeats while the first one is still unread.
        if Recommendation.objects.filter(
            sender=self.context["request"].user,
            recipient=attrs["recipient"],
            work=attrs["work"],
            read_at__isnull=True,
        ).exists():
            raise serializers.ValidationError(
                {"detail": "This user already has this recommendation unread."}
            )
        return attrs


class SentRecommendationSerializer(RecommendationSerializer):
    """The sender does not see whether the recipient has read it."""

    class Meta(RecommendationSerializer.Meta):
        fields = ["id", "recipient", "work", "work_detail", "message", "created_at"]
        read_only_fields = ["created_at"]
