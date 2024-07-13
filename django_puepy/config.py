from django.conf import settings
from django_puepy import paths

DEBUG = getattr(settings, "PUEPY_DEBUG", getattr(settings, "DEBUG", False))
PUEPY_PYSCRIPT_VERSION = getattr(settings, "PUEPY_PYSCRIPT_VERSION", "2024.7.1")
PUEPY_WHEEL_FILE = getattr(
    settings,
    "PUEPY_WHEEL_FILE",
    f'{paths.static_path.name}/{sorted(paths.static_path.glob("puepy*.whl"))[-1].relative_to(paths.static_path)}',
)
