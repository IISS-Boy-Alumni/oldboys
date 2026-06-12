# oldboys

## Production Deployment

### Static Assets

Shopyo packages (`shopyo_dashboard`, `shopyo_auth`, etc.) ship their own static files (CSS, JS, images) inside the installed Python package. In production, these must be collected into the project's `static/modules/` directory so your web server can serve them.

#### If using nginx to serve `/static/` directly (recommended)

Run `collectstatic` after every package upgrade:

```bash
cd /root/oldboys
source .venv/bin/activate
shopyo collectstatic
```

This copies all static files from:
- Project modules (`modules/*/static/`)
- Installed `shopyo_*` packages (`shopyo_dashboard`, `shopyo_auth`, etc.)

into `static/modules/`. nginx then serves them directly.

Without this step, `/static/modules/shopyo_dashboard/...` will return 404 in production.

#### If using Flask to serve `/static/` (no nginx override)

The `register_shopyo_static` interceptor serves package statics dynamically even in production — no `collectstatic` needed. But this is slower and not recommended for production.

### Theme Directories

The `front` and `back` theme directories under `static/themes/` are required. They are created during `shopyo initialise`. If missing, copy them from the installed `shopyo` package:

```bash
cp -r /root/oldboys/.venv/lib/python3.12/site-packages/shopyo/static/themes/* /root/oldboys/static/themes/
```

### Full Deployment Checklist

1. `uv sync && uv pip install gunicorn`
2. `source .venv/bin/activate && shopyo initialise`
3. `shopyo collectstatic`
4. `mkdir -p logs`
5. Configure systemd + nginx (see `how-to-serve.md`)
6. `systemctl restart oldboys.service`