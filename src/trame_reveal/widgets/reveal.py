from trame_client.widgets.core import AbstractElement

from trame_reveal import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


__all__ = [
    "Slides",
]


class Slides(HtmlElement):
    ID = 0

    def __init__(self, content=None, **kwargs):
        Slides.ID += 1
        tpl_name = f"rslides_{Slides.ID}"

        super().__init__(
            "reveal-slides",
            tplName=tpl_name,
            **kwargs,
        )
        self._attr_names += [
            "tplName",
            "config",
        ]

        self.state[f"trame__template_{tpl_name}"] = content
