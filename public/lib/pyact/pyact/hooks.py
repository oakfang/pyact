# pyright: reportMissingImports=false
from react import useState, useMemo, useEffect
from .utils import as_js


def js_producer(func):
    def wrapper(*args, **kwargs):
        return as_js(func(*args, **kwargs))

    return wrapper


def use_memo(*dependencies):
    def wrapper(memorizer):
        return useMemo(as_js(js_producer(memorizer)), as_js(dependencies))

    return wrapper


def use_effect(*dependencies):
    def wrapper(effect):
        return useEffect(as_js(js_producer(effect)), as_js(dependencies))

    return wrapper


use_state = useState
