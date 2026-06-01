from ohmygui.core.application import App
from ohmygui.core.window import Window
from ohmygui.layout.vertical import VerticalLayout
from ohmygui.widget.basic import Text, Button, InputEntry

app = App()
win = Window("Layout Basic", (360, 380))
win.set_bg("#f4f4f8")

layout = VerticalLayout()
layout.add_margin(14)
layout.set_common_spacing(12)

header = Text("Login Form", "#ffffff", "#2257a8")
header.set_size(320, 50)

username = InputEntry("Username")
username.set_size(320, 45)

password = InputEntry("Password")
password.set_size(320, 45)

submit = Button("Submit", "#ffffff", "#2257a8")
submit.set_size(320, 45)

layout.add_widget(header)
layout.add_widget(username)
layout.add_widget(password)
layout.add_widget(submit)

win.set_layout(layout)
win.show()
app.run()
