import ohmygui.core as core
import ohmygui.widget as widget
import ohmygui.layout as layout

app = core.App()
win = core.Window("Layout Basic", (360, 380))
win.set_bg("#f4f4f8")

lay = layout.VerticalLayout()
lay.add_margin(14)
lay.set_common_spacing(12)

header = widget.Text("Login Form", "#ffffff", "#2257a8")
header.set_size((320, 50))

username = widget.InputEntry("Username")
username.set_size((320, 45))

password = widget.InputEntry("Password")
password.set_size((320, 45))

submit = widget.Button("Submit", "#ffffff", "#2257a8")
submit.set_size((320, 45))

lay.add_widget(header)
lay.add_widget(username)
lay.add_widget(password)
lay.add_widget(submit)

win.set_layout(lay)
win.show()
app.run()
