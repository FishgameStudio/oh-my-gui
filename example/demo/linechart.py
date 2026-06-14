# Line chart demo.
# Only 28 lines

from ohmygui import *
from random import randint

app = core.App()
win = core.Window("Line chart demo")    
win.set_size((800, 400))

DATA: list[int] = []
for _ in range(0, 100):
    DATA.append(randint(0, 50))

PADDING = 20
data_len = len(DATA)

with layout.VerticalLayout() as lay:
    cvs = widget.Canvas(utils.WHITE, utils.BLACK)
    cvs.set_size((win.w, win.h))

    canvas_w = cvs.width - PADDING * 2
    canvas_h = cvs.height - PADDING * 2
    step_x = canvas_w / (data_len - 1)

    def map_value(val: int) -> int:
        return int(PADDING + canvas_h - (val / 100 * canvas_h))

    current_x = PADDING
    current_y = map_value(DATA[0])

    for val in DATA[1:]:
        next_x = current_x + step_x
        next_y = map_value(val)
        cvs.make_line(current_x, current_y, next_x, next_y)
        current_x, current_y = next_x, next_y

    lay.add_widget(cvs)

win.set_layout(lay).set_bg("#000000").show()
app.run()