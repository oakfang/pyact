from pyact import component, use_state, text, html
from .node_modules import mui
from .hooks import use_style, use_image_transformer
from .couter_controller import counter_controller


def to_grayscale(img):
    return img.convert("RGBA").convert("L")


@component
def home():
    counter, set_counter = use_state(0)
    style = use_style(counter)
    grayscale_logo = use_image_transformer("/logo512.png", to_grayscale)

    with mui.AppBar(position="static", sx=dict(padding=2)):
        with mui.Typography(variant="h4", component="div"):
            text("PyAct Demo")

    with mui.Container(sx=dict(display="flex", flexDirection="column")):
        with mui.Typography(variant="h3", component="div", align="center", sx=style):
            text(counter)
        +counter_controller(counter=counter, set_counter=set_counter)
        if grayscale_logo is not None:
            +html.img(src=grayscale_logo)
