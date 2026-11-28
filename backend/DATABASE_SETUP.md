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
   CREATE DATABASE nerdiary_dev OWNER user1;
   ALTER ROLE user1 SET client_encoding TO 'utf8';
   ALTER ROLE user1 SET default_transaction_isolation TO 'read committed';
   ALTER ROLE user1 SET timezone TO 'UTC';
   \q
   ```

   If you already have `user1`, only create the database. Do not reuse a database
   created from `backup.sql`: the custom user model needs a new, empty one.
4. Copy the `DB_*` variables from `.env.example` to `backend/.env` and set your own values
   (`DB_NAME=nerdiary_dev`).
5. From `backend/`, with the virtual environment activated:

   ```powershell
   uv pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

Django migrations create the tables. Do not import `backup.sql`; it is kept only as a
reference for the old schema and its test data.

## Changing models

After editing a model, run `python manage.py makemigrations` and commit the new migration
files together with the model change.
