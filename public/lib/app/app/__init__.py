from pyact import component, html, render, text, as_js, use_state, use_memo, use_effect


@component
def counter_controller(counter, set_counter):
    with html.button(onClick=lambda _e: set_counter(counter - 1)):
        text("-")
    +html.input(
        type="number",
        value=counter,
        onChange=lambda e: set_counter(int(e.target.value)),
    )
    with html.button(onClick=lambda _e: set_counter(counter + 1)):
        text("+")


def use_style(level):
    color = "red" if level < 0 else "darkgoldenrod" if level == 0 else "green"

    @use_memo(color)
    def style():
        return as_js({"color": color})

    return style


@component
def app():
    counter, set_counter = use_state(0)
    style = use_style(counter)

    @use_effect(counter)
    def print_counter():
        print(f"Counter: {counter}")

    with html.div():
        with html.h1(style=style):
            text(counter)
        +counter_controller(counter=counter, set_counter=set_counter)


def main():
    render("root", app())
