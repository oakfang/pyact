# pyright: reportMissingImports=false
import inspect
import react
import js
from .tree import Tree
from .utils import as_js


def run_render(renderer, props, children):
    params = inspect.signature(renderer).parameters
    has_kwargs = any(param.kind == param.VAR_KEYWORD for param in params.values())
    has_children_prop = "children" in params
    render_props = {
        key: item
        for key, item in js.Object.entries(props)
        if has_kwargs or key in params
    }

    if has_children_prop or has_kwargs:
        render_props["children"] = children

    return renderer(**render_props)


def render_subtree(subtree):
    if isinstance(subtree.data, str):
        return subtree.data

    return react.createElement(
        subtree.data.renderer_proxy,
        as_js(subtree.data.props),
        as_js([render_subtree(branch) for branch in subtree.branches])
        if subtree.branches
        else None,
    )


def render_tree(renderer, props=None, children=None):
    root = Tree(None)
    run_render(renderer, props, children)

    if not root.branches:
        return None

    if len(root.branches) == 1:
        subtree = root.branches[0]
        return render_subtree(subtree)

    return react.createElement(
        react.Fragment,
        None,
        as_js([render_subtree(subtree) for subtree in root.branches]),
    )
