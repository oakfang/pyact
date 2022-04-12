from pyact import component, use_state, as_js, text
from .node_modules import mui
from .hooks import use_style
from .couter_controller import counter_controller


@component
def home():
    counter, set_counter = use_state(0)
    style = use_style(counter)

    with mui.AppBar(position="static", sx=as_js(dict(padding=2))):
        with mui.Typography(variant="h4", component="div"):
            text("PyAct Demo")

    with mui.Container():
        with mui.Typography(variant="h3", component="div", align="center", sx=style):
            text(counter)
        +counter_controller(counter=counter, set_counter=set_counter)
