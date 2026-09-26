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


def conf_cone(app):
    with app.server.state as state:
        state.resolution = 12


app = SlideViewer(
    content=Path(__file__).with_name("slides.html"),
    theme="moon",
)
app.register_app(
    name="cone",
    app=Cone,
    initialize=conf_cone,
)
app.server.start()
