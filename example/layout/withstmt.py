# Bind widgets in `with` statement.

from ohmygui import *

app = core.Application()
win = core.Window()

with layout.HorizentalLayout() as lay:
    lay.add_widget(widget.Button("click me!")).add_widget(widget.Text("Wow!")).add_widget(widget.Text("Oh My GUI!"))
win.set_layout(lay).show()
app.run()

