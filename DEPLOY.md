# Deployment Guide — Plot (plot.org.za)

Serves `https://plot.org.za` (and `www.plot.org.za`) from `vm670ifvm`, alongside
the existing apps in `~/apps` (`garden`, `market`, `river`, `elands`, `homtini`).

This guide mirrors the proven `garden` pattern exactly:
- code in `~/apps/plot`, gunicorn runs as `carbonplanner` (group `www-data`)
- unix socket in the app dir, served by nginx behind certbot SSL

> **SSL is required, not optional:** with `DEBUG=False`, `harvester/settings.py`
> forces `SECURE_SSL_REDIRECT=True`, secure session/CSRF cookies, and HSTS. Plain
> HTTP would break admin login and the inquiry form, so run step 5 (certbot).

## 0. Prerequisites

- DNS is already done: `plot.org.za` and `www` → `169.239.182.221`.
- Repo is public: `https://github.com/KobusWHMeiring/plot.git`.
- Django 6.0 needs Python 3.12+ (Ubuntu 24.04 default — satisfied).
- nginx + python3-venv are already installed (other apps run on this box).

## 1. Application setup

```bash
mkdir -p ~/apps/plot
git clone https://github.com/KobusWHMeiring/plot.git ~/apps/plot
cd ~/apps/plot

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env

# Generate a real secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

nano .env
```

`.env`:

```
DEBUG=False
SECRET_KEY=<paste the generated key>
ALLOWED_HOSTS=plot.org.za,www.plot.org.za,169.239.182.221
DATABASE_URL=sqlite:///db.sqlite3
```

Initialise DB and static files:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

No `chown` needed — everything runs as `carbonplanner`.

## 2. Configure Gunicorn (systemd)

Create `/etc/systemd/system/plot.service`:

```ini
[Unit]
Description=Gunicorn daemon for Plot
After=network.target

[Service]
User=carbonplanner
Group=www-data
WorkingDirectory=/home/carbonplanner/apps/plot
ExecStart=/home/carbonplanner/apps/plot/venv/bin/gunicorn --workers 3 --bind unix:/home/carbonplanner/apps/plot/plot.sock harvester.wsgi:application
[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start plot
sudo systemctl enable plot
```

## 3. Configure Nginx

Create `/etc/nginx/sites-available/plot` (HTTP-only; certbot adds SSL next step):

```nginx
server {
    server_name plot.org.za www.plot.org.za;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /home/carbonplanner/apps/plot/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/carbonplanner/apps/plot/plot.sock;
    }

    listen 80;
}
```

```bash
sudo ln -s /etc/nginx/sites-available/plot /etc/nginx/sites-enabled/plot
sudo nginx -t
sudo systemctl reload nginx
```

Do **not** remove `sites-enabled/default` — it isn't enabled anyway, and the other
sites each have their own `server_name` block.

## 4. SSL (required)

```bash
sudo certbot --nginx -d plot.org.za -d www.plot.org.za
```

certbot rewrites `plot` into the standard 443 + `listen 80` → 301 redirect pair,
exactly like `garden`. There is no wildcard cert on this box, so this adds a
dedicated `plot.org.za` cert without touching the others.

Verify: `curl -I https://plot.org.za`.

## 5. Deploying updates

```bash
cd ~/apps/plot
git pull
venv/bin/pip install -r requirements.txt
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart plot
```

## Notes / gotchas

- **Static files live in `staticfiles/`** (Django's `STATIC_ROOT`), not `static/`.
- **Socket is `/home/carbonplanner/apps/plot/plot.sock`**, created by gunicorn
  (default umask → world-connectable), so nginx (`www-data`) can reach it — same
  mechanism as `garden.sock`.
- **Don't name the unit `gunicorn.service`** — a failed unit with that name
  already exists on the box. Use `plot.service`.
- **SQLite is a single file** at `~/apps/plot/db.sqlite3`; back it up if inquiry
  data matters (there's a `market_worker` Celery pattern on this box if you ever
  want to move off SQLite, but that's out of scope here).
