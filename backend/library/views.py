from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Genre, LibraryEntry, Work
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    GenreSerializer,
    LibraryEntrySerializer,
    PublicUserSerializer,
    WorkSerializer,
)


class DefaultPagination(PageNumberPagination):
    page_size = 20


def filter_entries(queryset, params):
    if status := params.get("status"):
        queryset = queryset.filter(status=status)
    if media_type := params.get("media_type"):
        queryset = queryset.filter(work__media_type=media_type)
    return queryset.select_related("work").order_by("-added_at", "-id")


ENTRY_FILTERS = [OpenApiParameter("status", str), OpenApiParameter("media_type", str)]


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
