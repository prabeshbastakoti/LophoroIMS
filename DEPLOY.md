# Deploying LophoroIMS to cPanel

Target setup: cPanel **Setup Python App** (Phusion Passenger) + MySQL, with the
code pulled from git.

---

## 1. Create the database (cPanel → MySQL® Databases)

1. Create a database, e.g. `cpaneluser_lophoroims`.
2. Create a user, e.g. `cpaneluser_lophoro`, with a strong password.
3. Add the user to the database with **ALL PRIVILEGES**.

Note the full prefixed names — they go in `.env`.

## 2. Create the Python app (cPanel → Setup Python App)

| Field | Value |
| --- | --- |
| Python version | 3.11 or newer |
| Application root | `lophoroims` (a folder in your home dir, **not** inside `public_html`) |
| Application URL | the domain/subdomain the app should answer on |
| Application startup file | `passenger_wsgi.py` |
| Application Entry point | `application` |

Click **Create**. cPanel makes the folder and a virtualenv, and shows a
"Enter to the virtual environment" command like:

```
source /home/cpaneluser/virtualenv/lophoroims/3.11/bin/activate && cd /home/cpaneluser/lophoroims
```

Copy that command — you need it for every terminal step below.

## 3. Pull the code (cPanel → Terminal, or SSH)

cPanel creates `passenger_wsgi.py` and `tmp/` in the app root, so the folder is
not empty and `git clone` will refuse it. Clone into it like this:

```bash
cd ~/lophoroims
rm -f passenger_wsgi.py            # ours replaces the cPanel stub
git init
git remote add origin https://github.com/prabeshbastakoti/LophoroIMS.git
git fetch origin main
git checkout -f -t origin/main
```

For later updates, that becomes just `git pull` (see step 8).

## 4. Configure `.env`

```bash
cd ~/lophoroims
cp .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Edit `.env` (cPanel File Manager, or `nano .env`) and set:

```ini
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<paste the generated key>
DJANGO_ALLOWED_HOSTS=ims.example.com,www.ims.example.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://ims.example.com,https://www.ims.example.com

DB_ENGINE=mysql
DB_NAME=cpaneluser_lophoroims
DB_USER=cpaneluser_lophoro
DB_PASSWORD=<db password>
DB_HOST=localhost
DB_PORT=3306
```

`DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` must both list your real
domain, or you get a `DisallowedHost` error and CSRF failures on every form.

If the domain has **no SSL certificate yet**, also add `DJANGO_SSL_REDIRECT=False`
until you run AutoSSL — otherwise the https redirect loops. Remove it afterwards.

## 5. Install dependencies

Run the "Enter to the virtual environment" command from step 2, then:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If `mysqlclient` fails to build on your host, use the pure-python driver instead:

```bash
pip install PyMySQL
```

and add these two lines at the top of `lophoroims/__init__.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

## 6. Migrate, collect static, create the admin user

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

`collectstatic` writes to `staticfiles/`, which is **not** in git — it must be run
on the server after every deploy. Static files are served by WhiteNoise from the
app process, so no Apache alias or `public_html` symlink is needed.

Uploaded images live in `media/`, also not in git. It is created automatically on
first upload; make sure it stays writable.

## 7. Start it

In **Setup Python App**, click **Restart**. Visit your domain — it redirects to
`/accounts/login/`.

Then run **cPanel → SSL/TLS Status → Run AutoSSL** if you have not already.

## 8. Deploying updates later

```bash
source /home/cpaneluser/virtualenv/lophoroims/3.11/bin/activate && cd /home/cpaneluser/lophoroims
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch tmp/restart.txt
```

`touch tmp/restart.txt` tells Passenger to reload the app — same effect as the
Restart button.

---

## Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| 500 with no detail | Check `stderr.log` in the app root, or cPanel → Errors. Never set `DJANGO_DEBUG=True` on a live site to debug. |
| `DisallowedHost` | Domain missing from `DJANGO_ALLOWED_HOSTS`. |
| `CSRF verification failed` | Domain missing from `DJANGO_CSRF_TRUSTED_ORIGINS` (must include the `https://` scheme). |
| Redirect loop | No certificate yet — set `DJANGO_SSL_REDIRECT=False`, run AutoSSL, then remove it. |
| Unstyled pages | `collectstatic` was not run after the last pull. |
| `ImproperlyConfigured: DJANGO_SECRET_KEY ... required` | `.env` missing or the key is blank. |
| Code changes not showing | `touch tmp/restart.txt`. |
