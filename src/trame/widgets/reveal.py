from trame_reveal import module
from trame_reveal.widgets.reveal import *  # noqa: F403


def initialize(server, **_):
    server.enable_module(module)
