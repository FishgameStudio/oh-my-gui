# Bind widgets in `with` statement.

from ohmygui import *

app = Application()
win = Window()

with HorizontalLayout() as lay:
    lay.add_widget(Button("click me!")).add_widget(Text("Wow!")).add_widget(Text("Oh My GUI!"))
win.set_layout(lay).show()
app.run()

