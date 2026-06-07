# Example of horizontal layout

import ohmygui.core as core
import ohmygui.widget as widget
import ohmygui.layout as layout

app = core.App()
window = core.Window("Horizontal Layout Example", (400, 200))
layout = layout.HorizentalLayout()

layout.add_widget(widget.Text("Hello"))
layout.add_spacing(20)
layout.add_widget(widget.Text("World"))
layout.add_stretch()
layout.add_widget(widget.Text("!"))
window.set_layout(layout)
window.show()
app.run()