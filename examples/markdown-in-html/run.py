#!/usr/bin/env -S uv run --script
# /// script
#
# requires-python = ">=3.10"
#
# dependencies = [
#   "trame>=3.13",
#   "trame-vuetify",
#   "trame-vtk",
#   "trame-revealjs",
# ]
#
# ///

from pathlib import Path

from app import Cone

from trame.tools.reveal import SlideViewer


def main():
    app = SlideViewer(
        content=Path(__file__).with_name("slides.html"),
        theme="black-contrast",
    )
    app.register_app(
        name="cone",
        app=Cone,
    )
    app.server.start()


if __name__ == "__main__":
    main()
