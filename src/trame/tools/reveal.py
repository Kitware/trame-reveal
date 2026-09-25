import inspect
from asyncio.tasks import Task
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from trame.app import TrameApp, asynchronous, get_server
from trame.decorators import life_cycle
from trame.ui.html import DivLayout
from trame.widgets import client, reveal
from trame_reveal import module


@dataclass
class Entry:
    app: TrameApp
    task: Task
    initialize: Callable[[TrameApp], None]
    port: int = 0
    url: str = ""


class SlideViewer(TrameApp):
    def __init__(self, server=None, content=None, theme="white", styles=None):
        super().__init__(server)

        reveal.initialize(self.server)
        if styles is None:
            styles = []

        if theme:
            styles.append(f"{module.serve_directory}/theme/{theme}.css")

        self._slide_file = Path(content)
        www = self._slide_file.with_name("$")
        if www.exists():
            self.server.enable_module(
                {
                    "serve": {"$": str(www.resolve())},
                }
            )
            for css in www.glob("*.css"):
                styles.append(f"$/{css.name}")

        if styles:
            self.server.enable_module(
                {
                    "styles": styles,
                }
            )
        self._apps = {}
        with DivLayout(self.server) as self.ui:
            self.ui.root.style = "height:100vh;"
            client.Style("html,body{margin:0;padding:0;}")
            reveal.Slides(
                content=self._slide_file.read_text(),
                theme=theme,
            )

    @life_cycle.server_ready_task
    async def _on_ready(self, **_):
        urls = {}
        for name, entry in self._apps.items():
            await entry.app.server.ready
            entry.port = entry.app.server.port
            entry.url = f"http://localhost:{entry.port}/"
            urls[name] = entry.url
            if entry.initialize:
                result = entry.initialize(entry.app)
                if inspect.isawaitable(result):
                    asynchronous.create_task(result)

        with self.state as state:
            state.app_urls = urls

    def register_app(self, name, app, initialize=None):
        server = get_server(name)
        app = app(server)
        task = app.server.start(exec_mode="task", port=0)
        self._apps[name] = Entry(app=app, task=task, initialize=initialize)
