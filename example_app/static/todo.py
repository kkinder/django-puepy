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
