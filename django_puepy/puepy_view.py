import json

from django.conf import settings
from django.http import HttpResponse, Http404
from django.templatetags.static import static
from django.views.generic import TemplateView

import dtjson
from django_puepy import config


class PuePyView(TemplateView):
    template_name = "django_puepy/puepy_view.html"
    frontend_url = "/static/app.py"
    runtime = "mpy"
    python_files = []
    python_packages = []
    js_modules = []
    debug = None

    @staticmethod
    def ajax(method):
        method._is_ajax = True

        return method

    def get_context_data(self, **kwargs):
        if self.runtime not in ["mpy", "py"]:
            raise ValueError(f"Invalid runtime: {self.runtime}")

        data = super().get_context_data(**kwargs)
        data["puepy_runtime"] = self.runtime
        data["frontend_url"] = self.frontend_url
        data["pyscript_config"] = json.dumps(self.get_pyscript_config())
        return data

    def get_pyscript_config(self):
        if self.debug is None:
            debug = getattr(settings, "PUEPY_DEBUG", getattr(settings, "DEBUG", False))
        else:
            debug = self.debug

        return {
            "name": "PuePy",
            "debug": debug,
            "files": {
                static("django_puepy/dtjson.py"): "./dtjson.py",
                static("django_puepy/django_backend.py"): "./django_backend.py",
            },
            "packages": [static(config.PUEPY_WHEEL_FILE)],
            "js_modules": {
                "main": {"https://cdn.jsdelivr.net/npm/morphdom@2.7.2/+esm": "morphdom"}
            },
        }

    def post(self, request, *args, **kwargs):
        data = dtjson.loads(request.body)

        try:
            method_name = data["method"]
        except KeyError:
            raise Http404
        args = data["args"]
        kwargs = data["kwargs"]

        method = getattr(self, method_name, None)
        if method and hasattr(method, "_is_ajax"):
            return HttpResponse(content=dtjson.dumps(method(*args, **kwargs)))
        else:
            raise Http404
