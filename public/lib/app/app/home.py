from functools import cache
from pyact import component, use_state, text, html
from rooks import useDebouncedValue
from .node_modules import mui
from .hooks import use_style, use_image_transformer
from .couter_controller import counter_controller


@cache
def shift_hue(hue_delta):
    def shift(img):
        img = img.convert("RGBA")
        alpha = img.getchannel("A")
        img = img.convert("HSV")
        data = img.getdata()
        img.putdata(tuple((abs(h + hue_delta) % 255, s, v) for h, s, v in data))
        img = img.convert("RGBA")
        img.putalpha(alpha)
        return img
    return shift


@component
def home():
    counter, set_counter = use_state(0)
    style = use_style(counter)
    debounced_counter,_ = useDebouncedValue(counter, 300)
    logo = use_image_transformer("/logo512.png", shift_hue(debounced_counter))

    with mui.AppBar(position="static", sx=dict(padding=2)):
        with mui.Typography(variant="h4", component="div"):
            text("PyAct Demo")

    with mui.Container(sx=dict(display="flex", flexDirection="column")):
        with mui.Typography(variant="h3", component="div", align="center", sx=style):
            text(counter)
        +counter_controller(counter=counter, set_counter=set_counter)
        if logo is not None:
            +html.img(src=logo)
