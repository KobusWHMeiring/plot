# Deployment Guide — Plot (plot.org.za)

Target: Ubuntu 24.04 LTS, served at `https://plot.org.za` (and `www.plot.org.za`).
Deploy user: `carbonplanner` (has sudo). App service user: `www-data`.

> **Why SSL is required, not optional:** with `DEBUG=False`, `harvester/settings.py`
> forces `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`,
> `CSRF_COOKIE_SECURE=True`, and HSTS. Over plain HTTP the admin can't log in and
> the inquiry form fails CSRF. So the site **must** be served over HTTPS (step 5).

## 0. Prerequisites

- DNS: add an A record for the apex and `www` pointing at the server:

  ```
  plot.org.za   A   169.239.182.221
  www           A   169.239.182.221
  ```

  (`www` is currently a CNAME to the apex, which works too — an A record is just
  more robust for the bare/`www` pair.)

- The repo is public: `https://github.com/KobusWHMeiring/plot.git`.
- Django 6.0 requires Python 3.12+ — Ubuntu 24.04 ships 3.12, so no extra work.

## 1. System preparation

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx git
```

## 2. Application setup

```bash
# Create a place to clone into
sudo mkdir -p /var/www
sudo chown carbonplanner:carbonplanner /var/www

# Clone and set up the app
git clone https://github.com/KobusWHMeiring/plot.git /var/www/plot
cd /var/www/plot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Generate a real secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

nano .env
```

`.env` should look like:

```
DEBUG=False
SECRET_KEY=<paste the generated key>
ALLOWED_HOSTS=plot.org.za,www.plot.org.za,169.239.182.221
DATABASE_URL=sqlite:///db.sqlite3
```

Then initialise the database and static files:

```bash
python manage.py migrate
python manage.py collectstatic --noinput

# Hand everything to the service user (gunicorn runs as www-data and must be
# able to write the SQLite database and read the code/static files)
sudo chown -R www-data:www-data /var/www/plot
```

## 3. Configure Gunicorn (systemd)

Create `/etc/systemd/system/plot.service`:

```ini
[Unit]
Description=Gunicorn instance to serve Plot
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/plot
Environment="PATH=/var/www/plot/venv/bin"
ExecStart=/var/www/plot/venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/run/plot/plot.sock \
    harvester.wsgi:application

# Creates /run/plot owned by the service user so gunicorn can bind the socket
RuntimeDirectory=plot

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start plot
sudo systemctl enable plot
```

## 4. Configure Nginx

Create `/etc/nginx/sites-available/plot`:

```nginx
server {
    listen 80;
    server_name plot.org.za www.plot.org.za 169.239.182.221;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /var/www/plot/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/plot/plot.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/plot /etc/nginx/sites-enabled/plot
# Remove the default site if it's still there
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

## 5. SSL (required)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d plot.org.za -d www.plot.org.za
```

certbot rewrites the Nginx config to redirect HTTP → HTTPS and adds the cert.
Django's own `SECURE_SSL_REDIRECT` and `SECURE_PROXY_SSL_HEADER` already line up
with Nginx's `X-Forwarded-Proto` header, so everything works end-to-end.

Verify: `curl -I https://plot.org.za` should return `200` (or a redirect to a
known route).

## 6. Deploying updates

On the server, as `carbonplanner`:

```bash
cd /var/www/plot
sudo -u www-data git pull
sudo -u www-data venv/bin/pip install -r requirements.txt
sudo -u www-data venv/bin/python manage.py migrate
sudo -u www-data venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart plot
```

## Notes / gotchas

- **Static files live in `staticfiles/`** (Django's `STATIC_ROOT`), not `static/`.
  The Nginx `alias` above points at `staticfiles/`; the old guide's `root /var/www/plot`
  for `/static/` was wrong and would 404.
- **The socket is `/run/plot/plot.sock`**, created via `RuntimeDirectory=plot`.
  Binding directly to `/run/plot.sock` fails because `www-data` can't write to `/run`.
- **SQLite is a single file.** Keep a backup strategy in mind (e.g. copy
  `/var/www/plot/db.sqlite3` off-box) — the inquiry data lives there.
