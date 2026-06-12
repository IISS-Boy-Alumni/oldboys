# How to Serve a Flask App (PythonCMS/Shopyo) with nginx + gunicorn

This guide documents how `iissoldboys.com` (and sibling sites like `linkversity.lol`, `qabar.compileralchemy.com`) are served.

## Architecture

```
Internet → nginx (port 443) → gunicorn (Unix socket) → Flask app
```

- **nginx** terminates SSL, serves `/static/` directly, proxies everything else to gunicorn via a Unix socket.
- **gunicorn** runs the WSGI application with 4 workers.
- **systemd** manages the gunicorn process (auto-restart on failure).

---

## 1. Project Setup

```bash
cd /root/oldboys
uv sync                          # install dependencies from pyproject.toml
uv pip install gunicorn          # install gunicorn
source .venv/bin/activate
shopyo initialise                # create DB, run migrations, seed data
```

Create a `.env` file in the project root:

```ini
SECRET_KEY="<generated-with-python3 -c 'import secrets; print(secrets.token_hex(32))'>"
MAIL_USERNAME=""
MAIL_PASSWORD=""
MAIL_DEFAULT_SENDER=""
SQLALCHEMY_DATABASE_URI="sqlite:///shopyo.db"
```

Create a `wsgi.py` entry point:

```python
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import create_app

application = create_app("production")
```

---

## 2. systemd Service

**`/etc/systemd/system/oldboys.service`**

```ini
[Unit]
Description=Gunicorn instance to serve OldBoys Flask application
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/oldboys
Environment="PATH=/root/oldboys/.venv/bin"

ExecStart=/root/oldboys/.venv/bin/gunicorn \
  -w 4 \
  --bind unix:/root/run/oldboys.sock \
  --access-logfile /root/oldboys/logs/access.log \
  --error-logfile /root/oldboys/logs/error.log \
  wsgi:application

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Commands:

```bash
systemctl daemon-reload
systemctl enable oldboys.service
systemctl start oldboys.service
systemctl status oldboys.service
```

---

## 3. nginx Config

**`/etc/nginx/sites-available/iissoldboys.com`**

```nginx
server {
    listen 80;
    server_name iissoldboys.com www.iissoldboys.com;
    return 301 https://iissoldboys.com$request_uri;
}

server {
    listen 443 ssl http2;
    server_name iissoldboys.com www.iissoldboys.com;

    # --- SSL (managed by Certbot) ---
    ssl_certificate /etc/letsencrypt/live/iissoldboys.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iissoldboys.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # --- Security headers ---
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;

    # --- Static files ---
    location /static/ {
        alias /root/oldboys/static/;
        expires 30d;
        access_log off;
    }

    # --- Flask application ---
    location / {
        proxy_pass http://unix:/root/run/oldboys.sock;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    # --- Block sensitive files ---
    location ~ /\.git {
        deny all;
    }
}
```

Commands:

```bash
ln -sf /etc/nginx/sites-available/iissoldboys.com /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

---

## 4. SSL Certificate (Let's Encrypt)

```bash
certbot --nginx -d iissoldboys.com -d www.iissoldboys.com --agree-tos --email admin@iissoldboys.com
```

Certbot auto-renews via systemd timer. Certificates live in `/etc/letsencrypt/live/iissoldboys.com/`.

---

## 5. Reference: Other Sites on This Server

### linkversity.lol

**nginx** (`/etc/nginx/sites-available/linkversity`):

```nginx
server {
    listen 80;
    server_name linkversity.lol www.linkversity.lol;
    return 301 https://linkversity.lol$request_uri;
}

server {
    listen 443 ssl http2;
    server_name linkversity.lol www.linkversity.lol;

    ssl_certificate /etc/letsencrypt/live/linkversity.lol/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/linkversity.lol/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;

    location /static/ {
        alias /root/linkversity/static/;
        expires 30d;
        access_log off;
    }

    location / {
        proxy_pass http://unix:/root/run/linkversity.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    location ~ /\.git { deny all; }
}
```

**systemd** (`/etc/systemd/system/linkversity.service`):

```ini
[Unit]
Description=Gunicorn instance to serve Linkversity Flask application
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/linkversity
Environment="PATH=/root/linkversity/.venv/bin"

ExecStart=/root/linkversity/.venv/bin/gunicorn \
  -w 4 \
  --bind unix:/root/run/linkversity.sock \
  --access-logfile /root/linkversity/logs/access.log \
  --error-logfile /root/linkversity/logs/error.log \
  app:app

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### qabar.compileralchemy.com

**nginx** (`/etc/nginx/sites-available/qabar.compileralchemy.com`):

```nginx
server {
    listen 80;
    server_name qabar.compileralchemy.com;
    return 301 https://qabar.compileralchemy.com$request_uri;
}

server {
    listen 443 ssl http2;
    server_name qabar.compileralchemy.com;

    ssl_certificate /etc/letsencrypt/live/qabar.compileralchemy.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/qabar.compileralchemy.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;

    location / {
        proxy_pass http://unix:/root/run/qabar.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_read_timeout 300;
    }
}
```

**systemd** (`/etc/systemd/system/qabar.service`):

```ini
[Unit]
Description=Gunicorn instance to serve Qabar Flask application
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/qabaratan
Environment="PATH=/root/qabaratan/.venv/bin"

ExecStart=/root/qabaratan/.venv/bin/gunicorn \
  --chdir /root/qabaratan/qabaratan \
  -w 4 \
  --bind unix:/root/run/qabar.sock \
  --access-logfile /root/qabaratan/logs/access.log \
  --error-logfile /root/qabaratan/logs/error.log \
  app:app

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## 6. Quick-Start Checklist for a New Site

1. Clone project to `/root/<project>/`
2. `cd /root/<project>/ && uv sync && uv pip install gunicorn`
3. Create `.env` with `SECRET_KEY`, database URI, etc.
4. Create `wsgi.py` with `application = create_app("production")`
5. `mkdir -p logs`
6. Create `/etc/systemd/system/<project>.service` (copy pattern above)
7. `systemctl daemon-reload && systemctl enable <project> && systemctl start <project>`
8. Create `/etc/nginx/sites-available/<domain>` (copy pattern above)
9. `ln -sf /etc/nginx/sites-available/<domain> /etc/nginx/sites-enabled/ && systemctl reload nginx`
10. `certbot --nginx -d <domain> -d www.<domain> --agree-tos --email admin@<domain>`

---

## 7. Useful Commands

```bash
# Service management
systemctl status oldboys.service
journalctl -u oldboys.service --no-pager -l
systemctl restart oldboys.service

# Logs
tail -f /root/oldboys/logs/access.log
tail -f /root/oldboys/logs/error.log

# nginx
nginx -t
systemctl reload nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# SSL renewal (automatic via certbot timer, manual:)
certbot renew

# Database re-init (destroys data)
cd /root/oldboys && source .venv/bin/activate && shopyo initialise
```
