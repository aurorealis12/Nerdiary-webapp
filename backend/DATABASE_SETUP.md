# Local database setup (Windows, PowerShell)

1. Install PostgreSQL (server and command line tools): https://www.postgresql.org/download/windows/
2. Set the path to `psql` (replace `VERSION` with your version number):

   ```powershell
   $psql = "C:\Program Files\PostgreSQL\VERSION\bin\psql.exe"
   ```

3. Open the shell with `& $psql -U postgres`, then run:

   ```
   CREATE USER user1;
   \password user1
   CREATE DATABASE myprojectdb OWNER user1;
   ALTER ROLE user1 SET client_encoding TO 'utf8';
   ALTER ROLE user1 SET default_transaction_isolation TO 'read committed';
   ALTER ROLE user1 SET timezone TO 'UTC';
   \q
   ```

   If you already have the user and database, skip this step and step 5.
4. Copy the `DB_*` variables from `.env.example` to `backend/.env` and set your own values.
5. From `backend/`, import the data into the **empty** database:

   ```powershell
   & $psql -U postgres -d myprojectdb -v ON_ERROR_STOP=1 --single-transaction -f backup.sql
   ```

6. From `backend/`, with the virtual environment activated:

   ```powershell
   uv pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

The backup contains no admin account. Create one with `python manage.py createsuperuser`.

## Updating the backup

Use `-f` instead of `>`, so PowerShell does not change the file encoding:

```powershell
$pgDump = "C:\Program Files\PostgreSQL\VERSION\bin\pg_dump.exe"
& $pgDump -U user1 -h localhost -p 5432 --exclude-table-data=public.auth_user --exclude-table-data=public.auth_user_groups --exclude-table-data=public.auth_user_user_permissions --exclude-table-data=public.django_session --exclude-table-data=public.django_admin_log -f backup.sql myprojectdb
```

Before committing, check that the file has no real passwords or personal data (see the `uzytkownik` table).
