from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import generics, mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Genre, LibraryEntry, Recommendation, Tag, Work
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    GenreSerializer,
    LibraryEntrySerializer,
    PublicUserSerializer,
    RecommendationSerializer,
    SentRecommendationSerializer,
    TagSerializer,
    WorkSerializer,
)


class DefaultPagination(PageNumberPagination):
    page_size = 20


def filter_entries(queryset, params):
    if entry_status := params.get("status"):
        queryset = queryset.filter(status=entry_status)
    if tag := params.get("tag"):
        if not tag.isdecimal():
            raise ValidationError({"tag": "Expected a tag id."})
        queryset = queryset.filter(tags__id=tag)
    if media_type := params.get("media_type"):
        queryset = queryset.filter(work__media_type=media_type)
    return queryset.select_related("work").prefetch_related("tags").order_by("-added_at", "-id")


ENTRY_FILTERS = [
    OpenApiParameter("status", str),
    OpenApiParameter("media_type", str),
    OpenApiParameter("tag", int),
]


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("search", str),
            OpenApiParameter("media_type", str),
            OpenApiParameter("genre", int),
            OpenApiParameter("mine", bool, description="Only works added by you."),
        ]
    )
)
class WorkViewSet(viewsets.ModelViewSet):
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Work.objects.select_related("created_by")
            .prefetch_related("genres", "credits__person")
            .order_by("title", "id")
        )
        # Guests only see the catalogue.
        if not user.is_authenticated:
            queryset = queryset.filter(created_by__isnull=True)
        if self.action != "list":
            return queryset

        params = self.request.query_params
        # The list is the shared catalogue, unless the user asks for their own works.
        if params.get("mine") == "true":
            queryset = queryset.filter(created_by_id=user.id) if user.is_authenticated else queryset.none()
        else:
            queryset = queryset.filter(created_by__isnull=True)
        if search := params.get("search"):
            queryset = queryset.filter(Q(title__icontains=search) | Q(original_title__icontains=search))
        if media_type := params.get("media_type"):
            queryset = queryset.filter(media_type=media_type)
        if genre := params.get("genre"):
            if not genre.isdecimal():
                raise ValidationError({"genre": "Expected a genre id."})
            queryset = queryset.filter(genres__id=genre)
        return queryset

    def perform_create(self, serializer):
        # Taken from the session, so API users cannot add works to the catalogue.
        serializer.save(created_by=self.request.user)


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.order_by("name")
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]


@extend_schema_view(list=extend_schema(parameters=ENTRY_FILTERS))
class LibraryEntryViewSet(viewsets.ModelViewSet):
    """The logged-in user's own library."""

    serializer_class = LibraryEntrySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return LibraryEntry.objects.none()
        # Other users' entries are not found here, so they cannot be edited.
        queryset = LibraryEntry.objects.filter(user=self.request.user)
        return filter_entries(queryset, self.request.query_params)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(parameters=[OpenApiParameter("search", str)])
class UserListView(generics.ListAPIView):
    serializer_class = PublicUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = get_user_model().objects.filter(is_active=True).order_by("username")
        if search := self.request.query_params.get("search"):
            queryset = queryset.filter(username__icontains=search)
        return queryset


@extend_schema(parameters=ENTRY_FILTERS)
class UserLibraryView(generics.ListAPIView):
    """Read-only view of any user's library."""

    serializer_class = LibraryEntrySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return LibraryEntry.objects.none()
        owner = get_object_or_404(
            get_user_model(), username=self.kwargs["username"], is_active=True
        )
        queryset = LibraryEntry.objects.filter(user=owner)
        return filter_entries(queryset, self.request.query_params)


class TagViewSet(viewsets.ModelViewSet):
    """The logged-in user's own tags."""

    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Tag.objects.none()
        return Tag.objects.filter(owner=self.request.user).order_by("name", "id")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema_view(list=extend_schema(parameters=[OpenApiParameter("unread", bool)]))
class RecommendationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """The list is the inbox. Only the recipient can read or delete a recommendation."""

    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Recommendation.objects.none()
        queryset = (
            Recommendation.objects.filter(recipient=self.request.user)
            .select_related("sender", "recipient", "work")
            .order_by("-created_at", "-id")
        )
        if self.action == "list" and self.request.query_params.get("unread") == "true":
            queryset = queryset.filter(read_at__isnull=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def _mark_as_read(self, recommendation):
        if recommendation.read_at is None:
            recommendation.read_at = timezone.now()
            recommendation.save(update_fields=["read_at"])

    @extend_schema(responses=SentRecommendationSerializer(many=True))
    @action(detail=False, serializer_class=SentRecommendationSerializer)
    def sent(self, request):
        queryset = (
            Recommendation.objects.filter(sender=request.user)
            .select_related("recipient", "work")
            .order_by("-created_at", "-id")
        )
        page = self.paginate_queryset(queryset)
        return self.get_paginated_response(self.get_serializer(page, many=True).data)

    @extend_schema(responses=inline_serializer("UnreadCount", {"count": serializers.IntegerField()}))
    @action(detail=False, url_path="unread-count", url_name="unread-count", pagination_class=None)
    def unread_count(self, request):
        return Response({"count": self.get_queryset().filter(read_at__isnull=True).count()})

    @extend_schema(request=None, responses=RecommendationSerializer)
    @action(detail=True, methods=["post"], url_path="read", url_name="read")
    def mark_read(self, request, pk=None):
        recommendation = self.get_object()
        self._mark_as_read(recommendation)
        return Response(self.get_serializer(recommendation).data)

    @extend_schema(request=None, responses={200: LibraryEntrySerializer, 201: LibraryEntrySerializer})
    @action(detail=True, methods=["post"], url_path="add-to-library", url_name="add-to-library")
    def add_to_library(self, request, pk=None):
        recommendation = self.get_object()
        work = recommendation.work
        if work.created_by_id not in (None, request.user.id):
            raise ValidationError({"work": "This work cannot be added to your library."})
        # An existing entry is returned unchanged, so no duplicate is created.
        entry, created = LibraryEntry.objects.get_or_create(user=request.user, work=work)
        self._mark_as_read(recommendation)
        data = LibraryEntrySerializer(entry, context=self.get_serializer_context()).data
        return Response(data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
