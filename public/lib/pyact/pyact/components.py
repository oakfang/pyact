# pyright: reportMissingImports=false
import importlib
import react
from weakref import WeakKeyDictionary
from functools import partial
from types import SimpleNamespace
from pyodide import JsProxy
from js import Object
from .tree import Tree
from .utils import as_js
from .renderer import render_tree

RENDERERS_REGISTRY = WeakKeyDictionary()


class ReactComponentInstance:
    def __init__(self, renderer, **props):
        self.renderer = renderer
        self.props = props
        self.is_native_element = isinstance(renderer, str)
        self.is_js_component = isinstance(renderer, JsProxy)

        if "key" not in self.props:
            self.props["key"] = self.get_default_key()

        if self.is_native_element or self.is_js_component:
            self.renderer_proxy = renderer
        else:
            if not renderer in RENDERERS_REGISTRY:
                RENDERERS_REGISTRY[renderer] = as_js(partial(render_tree, renderer))
            self.renderer_proxy = RENDERERS_REGISTRY[renderer]

    @property
    def name(self):
        if self.is_native_element:
            return self.renderer
        if self.is_js_component:
            return self.renderer.name
        return self.renderer.__name__

    def __pos__(self):
        with self:
            pass

    def __enter__(self):
        Tree.current.branch_out(self)

    def __exit__(self, *_):
        Tree.current.branch_in()

    def __repr__(self) -> str:
        return f"<{self.name} {self.props}>"

    def get_default_key(self):
        return f"{id(self.renderer)}__{len(Tree.current.branches) if Tree.current else '@root'}"

    def render_root(self):
        return react.createElement(
            self.renderer_proxy,
            as_js(self.props),
        )


def component(renderer):
    return partial(ReactComponentInstance, renderer)


class HtmlElementProxy:
    _cache = {}

    def __getattr__(self, element):
        if element not in self._cache:
            self._cache[element] = component(element)
        return self._cache[element]


html = HtmlElementProxy()


def uimport(name: str):
    original = importlib.import_module(name)
    return SimpleNamespace(
        **{key: component(value) for key, value in Object.entries(original)}
    )
