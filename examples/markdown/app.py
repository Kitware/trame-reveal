from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3, vtk as vtkw
from trame_server import Server


class Cone(TrameApp):
    def __init__(self, server: Server = None, initial_resolution: int = 6):
        super().__init__(server)
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("Trame demo")
            with self.ui.toolbar as toolbar:
                toolbar.density = "compact"
                v3.VSpacer()
                v3.VSlider(
                    v_model=("resolution", initial_resolution),
                    min=3,
                    max=60,
                    step=1,
                    hide_details=True,
                    style="max-width: 300px;",
                )
                v3.VBtn(icon="mdi-lock-reset", click="resolution=6")
                v3.VBtn(icon="mdi-crop-free", click=self.ctrl.view_reset_camera)

            with self.ui.content:
                with v3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    with vtkw.VtkView() as view:
                        self.ctrl.view_reset_camera = view.reset_camera
                        with vtkw.VtkGeometryRepresentation():
                            vtkw.VtkAlgorithm(
                                vtk_class="vtkConeSource",
                                state=("{ resolution }",),
                            )
