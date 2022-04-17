from pyact import component, as_js
from mui import createTheme
from .node_modules import mui
from .home import home

theme = createTheme(as_js({"palette": {"mode": "dark"}}))


@component
def app():
    with mui.ThemeProvider(theme=theme):
        +mui.CssBaseline()
        +home()
