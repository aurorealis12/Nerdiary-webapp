from django.contrib import admin

from . import models

admin.site.register([
    models.BookDetails,
    models.Collection,
    models.CollectionEntry,
    models.Credit,
    models.Episode,
    models.Franchise,
    models.GameDetails,
    models.Genre,
    models.LibraryEntry,
    models.MovieDetails,
    models.Person,
    models.Platform,
    models.Recommendation,
    models.Season,
    models.SeriesDetails,
    models.Tag,
    models.Work,
])
