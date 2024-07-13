from django import template
from django.utils.safestring import mark_safe

from django_puepy import config

register = template.Library()


@register.simple_tag
def puepy_headers():
    pyscript_version = config.PUEPY_PYSCRIPT_VERSION
    return mark_safe(
        f"""
        <link rel="stylesheet" href="https://pyscript.net/releases/{pyscript_version}/core.css">
        <script type="module" src="https://pyscript.net/releases/{pyscript_version}/core.js"></script>
        """
    )


@register.inclusion_tag("django_puepy/puepy_script.html")
def puepy_script(runtime, frontend_url, config):
    return {
        "runtime": runtime,
        "frontend_url": frontend_url,
        "config": config,
    }
