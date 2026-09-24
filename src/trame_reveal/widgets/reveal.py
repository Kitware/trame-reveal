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
    def __init__(self, content=None, **kwargs):
        super().__init__(
            "reveal-slides",
            **kwargs,
        )
        self._attr_names += [
            "theme",
            "config",
        ]

        self.state.trame__template_slides = content
