from pathlib import Path

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# ---------------------------------------------------------------------------
# Base de datos: SQLite para desarrollo local
# Nota: psycopg2 en Windows con rutas no-ASCII genera UnicodeDecodeError.
# Cuando se configure PostgreSQL en un entorno limpio, usar prod.py.
# ---------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": Path(__file__).resolve().parent.parent.parent / "db.sqlite3",
    }
}

# Opcional: instalar django-debug-toolbar y agregarlo aquí
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
