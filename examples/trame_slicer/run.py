#!/usr/bin/env -S uv run --script
# /// script
#
# requires-python = ">=3.10"
#
# dependencies = [
#   "requests",
#   "trame>=3.13",
#   "trame-vuetify",
#   "trame-revealjs",
#   "trame-slicer",
# ]
#
# [[tool.uv.index]]
# url = "https://wheels.vtk.org"
#
# ///

import os
import json
import requests
from pathlib import Path

from trame.tools.reveal import SlideViewer

from trame_slicer.app.medical_viewer_app import MedicalViewerApp


def load_scene(application: MedicalViewerApp, file_path: str) -> None:
    application._logic._load_files_logic._on_load_scene(file_path)


def load_state(application: MedicalViewerApp, state_path: str) -> None:
    with open(state_path, "r") as f:
        state = json.load(f)

    for k, v in state.items():
        if k.startswith("trame"):
            continue
        application.state[k] = v
        application.state.flush()



def download(url: str, target_path: str) -> bool:
    r = requests.get(url, stream=True)
    if r.ok:
        with open(target_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
        return True
    else:
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
        return False


def main():
    app = SlideViewer(
        content=Path(__file__).with_name("slides.html"),
        theme="white",
    )
    app.register_app(
        name="app1",
        app=MedicalViewerApp,
    )
    app.register_app(
        name="app2",
        app=MedicalViewerApp,
    )
    app.register_app(
        name="app3",
        app=MedicalViewerApp,
    )
    app.register_app(
        name="app4",
        app=MedicalViewerApp,
    )

    scene_urls = {
        "app1": "https://github.com/Slicer/SlicerDataStore/releases/download/SHA256/1af630ebec079a34061c43d79afb786ae55a91230e82abad130097d60088ba4d",
        "app2": "https://github.com/Slicer/SlicerDataStore/releases/download/SHA256/47dd7b98fa9a0b2e15c3e755ea9cd7ec6047aa5c3a7e239c805fb27e9ad933d9",
        "app3": "https://github.com/Slicer/SlicerDataStore/releases/download/SHA256/3c71ed8d9d56fba66920ff532312efed29326e18fbc77352ceaced854ca12d93",
        "app4": "https://github.com/Slicer/SlicerDataStore/releases/download/SHA256/84644d9c8742023d1d27def26cd293905ed25e4fc17561dd0b1af6b9724ef13d",
    }

    for app_name, entry in app._apps.items():
        scene_file = Path(__file__).parent.joinpath("data_files", f"{app_name}.mrb")
        if not scene_file.exists():
            url = scene_urls[app_name]
            print(f"Fetching scene file for {app_name}: {url}")
            if not download(url, scene_file.resolve().as_posix()):
                error = f"Could not download scene file for {app_name} at : {url}"
                raise Exception(error)
            print("Fetch successful")

        load_scene(entry.app, scene_file)

    def load_states():
        for app_name, entry in app._apps.items():
            load_state(entry.app, Path(__file__).parent.joinpath("data_files", f"{app_name}_state.json"))

    app.ctrl.on_client_connected.add(load_states)
    app.server.start()


if __name__ == "__main__":
    main()
