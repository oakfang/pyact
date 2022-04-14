from pyact import use_memo, use_effect


def use_style(counter):
    color = "error" if counter < 0 else "warning" if counter == 0 else "success"

    @use_memo(color)
    def style():
        return dict(color=f"{color}.main")

    @use_effect(counter)
    def print_counter():
        print(f"Counter: {counter}")

    return style
