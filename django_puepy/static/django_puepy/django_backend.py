from pyscript import fetch
import js

import dtjson


class ServerError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"ServerError({self.code}, {self.message})"


async def call(url, data):
    token = js.document.querySelector("[name=csrfmiddlewaretoken]").value

    response = await fetch(
        js.window.location,
        method="POST",
        body=dtjson.dumps(data),
        headers={"X-CSRFToken": token},
    )
    if response.status > 199 and response.status < 300:
        data = await response.text()
        return dtjson.loads(data)
    elif response.status == 500:
        try:
            data = await response.json()
            error_text = data["message"]
        except:
            error_text = "Server Error"
        raise ServerError(500, error_text)
    else:
        raise ServerError(response.status, f"Server Error: {response.status}")


class Backend:
    def __init__(self, url=None):
        self.url = url or js.window.location

    async def __call__(self, method, *args, **kwargs):
        return await call(self.url, {"method": method, "args": args, "kwargs": kwargs})

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        async def method(*args, **kwargs):
            return await self(name, *args, **kwargs)

        return method


backend = Backend()
__all__ = ["backend", "ServerError", "call"]
