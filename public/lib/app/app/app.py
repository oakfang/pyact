from pyact import component
from .node_modules import mui
from .home import home

@component
def app():
    +mui.CssBaseline()
    +home()