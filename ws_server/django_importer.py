import django
from django.conf import settings
import settings as ownsettings

import sys
import importlib
from pathlib import Path

# First add django app to the path, so further import can append
rootpath = Path(__file__).parent.parent
sys.path.append( str(rootpath) )

django_path = Path(__file__).parent.parent / "django_app"
sys.path.append( str(django_path) )

# Then load django settings, and modify the database info (like location)
projsettings = importlib.import_module(getattr(ownsettings, "DJANGO_SETTINGS", ""))
dbconf = getattr(ownsettings, "DJANGO_DATABASE", {})
projsettings.DATABASES = dbconf

settings.configure(**projsettings.__dict__)

# Setup django
django.setup()