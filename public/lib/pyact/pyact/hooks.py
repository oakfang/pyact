# pyright: reportMissingImports=false
from react import useState, useMemo, useEffect
from .utils import as_js


def use_memo(*dependencies):
    def wrapper(memorizer):
        return useMemo(as_js(memorizer), as_js(dependencies))

    return wrapper


def use_effect(*dependencies):
    def wrapper(effect):
        return useEffect(as_js(effect), as_js(dependencies))

    return wrapper


use_state = useState
