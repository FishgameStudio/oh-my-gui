# Example of horizontal layout

from ohmygui.layout.horizental import HorizentalLayout
from ohmygui.widget.basic import Text
from ohmygui.core.application import App
from ohmygui.core.window import Window

app = App()
window = Window("Horizontal Layout Example", (400, 200))
layout = HorizentalLayout()

layout.add_widget(Text("Hello"))
layout.add_spacing(20)
layout.add_widget(Text("World"))
layout.add_stretch()
layout.add_widget(Text("!"))
window.set_layout(layout)
window.show()
app.run()