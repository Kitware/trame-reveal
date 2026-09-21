from pathlib import Path
from trame_revealjs import SlidesApp

from app import Cone


if __name__ == "__main__":
    app = SlidesApp(
        slides_path=Path(__file__).parent.joinpath("index.html").resolve().as_posix(),
        server=None,
        trame_apps={
            "app1": (Cone, [12]),
        }
    )
    app.start()
