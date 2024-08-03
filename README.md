# Django PuePy Integration

Provides [PuePy](https://puepy.dev) integration for Django.

## Installation

1. Install the package using pip:

```
pip install django_puepy
```

2. Add `django_puepy` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "django_puepy",
]
```

## Usage

Take a look at the `example_app` directory for a very simple Django app that makes use of django_puepy. There are just two files:

- `example_app/backend_server.py`: Simple one-file Django app that shows a server-side Django controller
- `example_app/static/todo.py`: The frontend PuePy code that interacts with the Django controller

### Backend Usage

Our example backend app, `example_app/backend_server.py`, specifies a frontend file, a runtime, and three ajax methods that are called by the frontend.

```python
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
```

The frontend file, `static/todo.py`, is a regular PuePy app+page, but makes calls to the django_backend to interact with the ajax methods specified above:

```python
from puepy import Application, Page, t

app = Application()
from django_backend import backend


@app.page()
class TodoPage(Page):
    def initial(self):
        return {"todos": [], "todo_add": "", "loading": True}

    def populate(self):
        t.h1("Todo List")
        if self.state["loading"]:
            t.p("Loading...")
        with t.ul(ref="todos"):
            for i, todo_item in enumerate(self.state["todos"]):
                t.li(
                    todo_item,
                    t.button(
                        "X", on_click=self.on_remove_todo_click, data_index=str(i)
                    ),
                )
        t.hr()
        with t.form(on_submit=self.on_add_form_submit, ref="form"):
            t.input(type="text", bind="todo_add")
            t.button("Add Todo")

    def on_ready(self):
        self.add_event_listener("load-data", self.on_load_data)
        self.trigger_event("load-data")

    async def on_load_data(self, event):
        with self.state.mutate():
            self.state["loading"] = True
            try:
                self.state["todos"] = await backend.get_todos()
            finally:
                self.state["loading"] = False

    async def on_add_form_submit(self, event):
        event.preventDefault()
        with self.state.mutate():
            self.state["loading"] = True
            try:
                self.state["todos"] = await backend.add_todo(self.state["todo_add"])
            finally:
                self.state["loading"] = False

    async def on_remove_todo_click(self, event):
        index = int(event.target.getAttribute("data-index"))
        with self.state.mutate():
            self.state["loading"] = True
            try:
                self.state["todos"] = await backend.remove_todo(index)
            finally:
                self.state["loading"] = False


app.mount("#app")
```

The result? A demo todo app.

## Project status

While PuePy is approach relative stability, this Django integration is currently only an experiment. It is not recommended for production use *at all* and will hopefully evolve over time.


