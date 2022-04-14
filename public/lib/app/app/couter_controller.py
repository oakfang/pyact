from pyact import component, html

from .node_modules import mui, icons


@component
def counter_controller(counter, set_counter):
    with html.div(
        style=dict(
            display="flex",
            justifyContent="center",
        )
    ):
        with mui.Button(
            variant="contained", onClick=lambda _e: set_counter(counter - 1)
        ):
            +icons.Remove()

        +mui.TextField(
            type="number",
            inputProps=dict(inputMode="numeric", pattern="[0-9]*"),
            value=counter,
            onChange=lambda e: set_counter(int(e.target.value)),
        )

        with mui.Button(
            variant="contained", onClick=lambda _e: set_counter(counter + 1)
        ):
            +icons.Add()
