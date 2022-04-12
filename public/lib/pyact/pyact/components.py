# pyright: reportMissingImports=false
import react
from weakref import WeakKeyDictionary
from functools import partial
from .tree import Tree
from .utils import as_js
from .renderer import render_tree

RENDERERS_REGISTRY = WeakKeyDictionary()


class ReactComponentInstance:
    def __init__(self, renderer, **props):
        self.renderer = renderer
        self.props = props
        if "key" not in self.props:
            self.props["key"] = self.get_default_key()
        if not renderer in RENDERERS_REGISTRY and not isinstance(renderer, str):
            RENDERERS_REGISTRY[renderer] = as_js(partial(render_tree, renderer))
        self.renderer_proxy = (
            RENDERERS_REGISTRY[renderer] if not isinstance(renderer, str) else renderer
        )

    @property
    def name(self):
        return (
            self.renderer.__name__
            if not isinstance(self.renderer, str)
            else self.renderer
        )

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
