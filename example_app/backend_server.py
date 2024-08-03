import os
import sys

from django.conf import settings
from django.urls import path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


settings.configure(
    DEBUG=True,
    SECRET_KEY="YOUR SECRET KEY",
    ROOT_URLCONF=__name__,
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.staticfiles",
        "django_puepy",
    ],
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
        },
    ],
    STATIC_URL="/static/",
    STATICFILES_DIRS=[os.path.join(BASE_DIR, "static")],
)
from django_puepy import PuePyView


todo_list = ["Buy groceries", "Clean house", "Install PuePy"]


class TodoView(PuePyView):
    frontend_url = "/static/todo.py"
    runtime = "mpy"

    @PuePyView.ajax
    def add_todo(self, item):
        todo_list.append(item)
        return todo_list

    @PuePyView.ajax
    def remove_todo(self, index):
        try:
            del todo_list[index]
        except IndexError:
            pass
        return todo_list

    @PuePyView.ajax
    def get_todos(self):
        return todo_list


urlpatterns = [path("", TodoView.as_view(), name="todo")]

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
