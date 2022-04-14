# pyright: reportMissingImports=false
from typing import Union, Callable
import pyodide
import react_dom
import js
from .tree import Tree


def render(element_id, component):
    root = react_dom.createRoot(js.document.getElementById(element_id))
    root.render(component.render_root())


def text(t):
    Tree.current.branch_out(str(t))
    Tree.current.branch_in()


def include(children):
    for child in children:
        Tree.current.branch_out(child)
        Tree.current.branch_in()


def to_js_object(dict: dict):
    return js.Object.fromEntries(pyodide.to_js({k: as_js(v) for k, v in dict.items()}))


def to_js_array(lst: list):
    return pyodide.to_js([as_js(x) for x in lst])


def as_js(item):
    if isinstance(item, (list, tuple)):
        return to_js_array(item)
    elif isinstance(item, dict):
        return to_js_object(item)
    elif isinstance(item, Callable):
        return pyodide.create_proxy(item)
    return item
