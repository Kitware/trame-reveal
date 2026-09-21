from pathlib import Path
from trame_revealjs import SlidesApp
from trame_slicer.app.medical_viewer_app import MedicalViewerApp


if __name__ == "__main__":
    app = SlidesApp(
        slides_path=Path(__file__).parent.joinpath("slides.html").resolve().as_posix(),
        server=None,
        iframe_port_start=8081,
        trame_apps={
            "app1": (MedicalViewerApp, []),
            "app2": (MedicalViewerApp, []),
            "app3": (MedicalViewerApp, []),
            "app4": (MedicalViewerApp, []),
        }
    )
    app.start()
