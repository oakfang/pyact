from pyact import use_memo, use_effect, as_js


def use_style(counter):
    color = "error" if counter < 0 else "warning" if counter == 0 else "success"

    @use_memo(color)
    def style():
        return as_js(dict(color=f"{color}.main"))

    @use_effect(counter)
    def print_counter():
        print(f"Counter: {counter}")

    return style
