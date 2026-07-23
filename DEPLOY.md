# Deploying LophoroIMS to cPanel

Target setup: cPanel **Setup Python App** (Phusion Passenger) + MySQL, with the
code pulled from git.

---

**Do steps 1 and 2 in this order.** Cloning must happen into an empty folder, but
creating the Python app first puts `passenger_wsgi.py` and `tmp/` in it. Clone
first, then point the app at the folder you cloned into.

## 1. Clone the code (cPanel → Git™ Version Control)

Click **Create**, then:

| Field | Value |
| --- | --- |
| Clone a Repository | toggle **on** |
| Clone URL | `https://github.com/prabeshbastakoti/LophoroIMS.git` |
| Repository Path | `lophoroims` — must **not** already exist, and must be outside `public_html` |

The repo is public, so no deploy key or token is needed.

<details>
<summary>If you already created the Python app first</summary>

The folder is not empty, so `git clone` refuses it. From Terminal:

```bash
cd ~/lophoroims
rm -f passenger_wsgi.py            # ours replaces the cPanel stub
git init
git remote add origin https://github.com/prabeshbastakoti/LophoroIMS.git
git fetch origin main
git checkout -f -t origin/main
```
</details>

## 2. Create the Python app (cPanel → Setup Python App)

| Field | Value |
| --- | --- |
| Python version | 3.11 or newer |
| Application root | `lophoroims` — the folder you just cloned into |
| Application URL | the domain/subdomain the app should answer on |
| Application startup file | `passenger_wsgi.py` |
| Application Entry point | `application` |

Click **Create**. cPanel builds a virtualenv and shows an "Enter to the virtual
environment" command like:

```
source /home/cpaneluser/virtualenv/lophoroims/3.11/bin/activate && cd /home/cpaneluser/lophoroims
```

Copy that command — you need it for every terminal step below.

## 3. Create the database (cPanel → MySQL® Databases)

1. Create a database, e.g. `cpaneluser_lophoroims`.
2. Create a user, e.g. `cpaneluser_lophoro`, with a strong password.
3. Add the user to the database with **ALL PRIVILEGES**.

Note the full prefixed names — they go in `.env`. Leave the database empty;
`migrate` builds the tables in step 6. You can inspect them afterwards in
phpMyAdmin.

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

You can also press **Update from Remote** in Git™ Version Control instead of
`git pull`, but that button *only* fetches code — it does not install packages,
migrate, collect static, or restart. The remaining four commands still have to be
run in Terminal. Note also that it refuses to pull if tracked files were edited
on the server, so make config changes in `.env` (which is gitignored) rather than
by editing tracked files directly.

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
| `Database returned an invalid datetime value` | MySQL has no timezone tables loaded (needs root, so shared hosts often lack them). Handled by `DB_TIME_ZONE` defaulting to `TIME_ZONE`; if you overrode it to `UTC`, remove that. |

To read a 500's traceback, use `tail -60 stderr.log`, or reproduce it directly:

```bash
python manage.py shell -c "
from django.test import Client
from accounts.models import User
c = Client()
c.force_login(User.objects.first())
print(c.get('/analytics/', HTTP_HOST='your.domain', secure=True).status_code)
"
```
