# Catalogue and library API

Log in as described in `AUTH_API.md`. Interactive docs: `/api/docs/`.

| Method | URL | Who | Description |
|---|---|---|---|
| GET | `/api/works/` | everyone | Catalogue. Filters: `search`, `media_type`, `genre` (id), `mine=true` |
| GET | `/api/works/{id}/` | everyone | Guests can open catalogue works only |
| POST | `/api/works/` | logged in | Add your own work |
| PATCH, PUT, DELETE | `/api/works/{id}/` | author | Catalogue works are managed in Django admin |
| GET | `/api/genres/` | everyone | All genres (not paginated) |
| GET, POST | `/api/library/` | logged in | Your library. Filters: `status`, `media_type` |
| GET, PATCH, PUT, DELETE | `/api/library/{id}/` | owner | One of your entries |
| GET | `/api/users/?search=` | logged in | Usernames only |
| GET | `/api/users/{username}/library/` | logged in | Read-only. Filters: `status`, `media_type` |

Lists have 20 items per page: `{"count", "next", "previous", "results"}`. Use `?page=2`.

## Values

- `media_type`: `book`, `movie`, `series`, `music`, `game`, `comic`
- `status`: `planned`, `in_progress`, `completed`, `dropped`
- `rating`: 1-5 or `null`
- `progress`: 0-100, default 0
- `cover`: image URL or `null`. Show a placeholder for `null`.

## Adding things

A work needs `title` and `media_type`. To upload a cover (max 5 MB), send `FormData` and
do not set the `Content-Type` header yourself. Repeat the `genres` key for several genres.

A library entry needs `work` (id). Its work cannot be changed later. Another user's own
work cannot be added, and a work can be in your library only once.

Deleting your own work also deletes your library entry for it.

## Not covered yet

User tags, recommendations, media-specific details (for example page count), editing
credits, average ratings. Replaced or deleted cover files stay on disk.

## Tests

```powershell
python manage.py test accounts library
```
