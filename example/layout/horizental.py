# Example of horizontal layout

from ohmygui import *

app = App()
window = Window("Horizontal Layout Example", (400, 200))
lay = HorizontalLayout()

lay.add_widget(Text("Hello"))
lay.add_spacing(20)
lay.add_widget(Text("World"))
lay.add_stretch()
lay.add_widget(Text("!"))
window.set_layout(lay)
window.show()
app.run()