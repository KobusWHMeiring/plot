# Deployment Guide for Ubuntu 24.04 LTS

This guide assumes a fresh Ubuntu 24.04 installation.

## 1. System Preparation

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx git
```

## 2. Application Setup

```bash
# Clone the repository
git clone https://github.com/KobusWHMeiring/plot.git /var/www/plot
cd /var/www/plot

# Setup Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Environment
cp .env.example .env
# EDIT .env and set your SECRET_KEY and ALLOWED_HOSTS
nano .env

# Initialize Database and Static Files
python manage.py migrate
python manage.py collectstatic --noinput
```

## 3. Configure Gunicorn (Systemd)

Create a systemd service file: `/etc/systemd/system/plot.service`

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
    --bind unix:/run/plot.sock \
    harvester.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Set permissions
sudo chown -R www-data:www-data /var/www/plot
sudo chmod 755 /var/www/plot

# Start Gunicorn
sudo systemctl start plot
sudo systemctl enable plot
```

## 4. Configure Nginx

Create a new Nginx configuration: `/etc/nginx/sites-available/plot`

```nginx
server {
    listen 80;
    server_name yourdomain.com your_vps_ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/plot;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/plot.sock;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/plot /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 5. SSL (Recommended)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

