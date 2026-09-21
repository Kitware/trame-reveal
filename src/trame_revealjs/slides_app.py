import asyncio
import sys
from pathlib import Path

from trame.app import TrameApp, get_server
from trame.ui.html import DivLayout
from trame.widgets import html, client
from trame_server.utils.browser import open_browser


class SlidesApp(TrameApp):
    def __init__(
        self,
        slides_path: str,
        server=None,
        port: int=8080,
        iframe_port_start: int=8081,
        trame_apps: dict[str, tuple[TrameApp, list]]={},
    ):
        super().__init__(server)
        self.slides_path = Path(slides_path).resolve()
        if not Path(self.slides_path).exists():
            error = f"{self.slides_path} does not exist"
            raise ValueError(error)
        self.port = port
        self.server.enable_module({
            "serve" : {
                "serve": Path(__file__).with_name("serve"),
                "$": Path(sys.argv[0]).resolve().parent.joinpath("www").resolve().as_posix(),
            },
            "scripts": [
                "serve/TrameEmbeddedApp.js",
                "serve/revealjs/js/reveal.js",
                "serve/revealjs/js/notes.js",
                "serve/revealjs/js/markdown.js",
                "serve/revealjs/js/highlight.js",
            ],
            "styles": [
                "serve/revealjs/css/reset.css",
                "serve/revealjs/css/reveal.css",
                "serve/revealjs/css/black.css",
                "serve/revealjs/css/monokai.css",
            ],
        })

        self.state.setdefault("app_urls", {})

        # Instantiate a trame apps per slide
        self.apps = {}
        self.sub_servers = []
        port = iframe_port_start
        for app_name, (app_constructor, args) in trame_apps.items():
            sub_server = get_server(app_name)
            app = app_constructor(sub_server, *args)
            self.apps[app_name] = app
            self.sub_servers.append((sub_server, port))
            self.state.app_urls = {
                **self.state.app_urls,
                app_name: f"http://localhost:{port}/index.html",
            }
            port += 1

        self.ctrl.on_server_ready.add(self.on_server_ready)
        self._build_ui()

    def _build_ui(self):
        with DivLayout(self.server) as self.ui:
            self.ui.root.style="height:100vh;"
            div = html.Div(classes="reveal")
            div.add_child(self.slides_path.read_text())

            client.Script("""
                setTimeout(() => {
                   Reveal.initialize({
                    hash: true,
                    plugins: [RevealMarkdown, RevealHighlight, RevealNotes],
                   });
                }, 100);
            """)

    def on_server_ready(self, *args, **kwargs):
        print(f"Slides available at: {self.ui.url.split("?")[0]}")
        open_browser(self.server)

    def start(self):
        # Main application server
        tasks = [self.server.start(exec_mode="task", port=self.port, open_browser=True)]

        # trame embedded app servers
        for sub_server, port in self.sub_servers:
            tasks.append(sub_server.start(exec_mode="task", port=port, open_browser=True))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*tasks))
