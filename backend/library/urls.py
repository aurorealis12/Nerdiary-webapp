from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("works", views.WorkViewSet, basename="work")
router.register("library", views.LibraryEntryViewSet, basename="library-entry")

urlpatterns = [
    path("genres/", views.GenreListView.as_view(), name="genre-list"),
    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/<str:username>/library/", views.UserLibraryView.as_view(), name="user-library"),
    *router.urls,
]
