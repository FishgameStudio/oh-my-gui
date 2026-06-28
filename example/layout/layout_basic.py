from ohmygui import *

app = App()
win = Window("Layout Basic", (360, 380))
win.set_bg("#f4f4f8")

lay = VerticalLayout()
lay.add_margin(14)
lay.set_common_spacing(12)

header = Text("Login Form", "#ffffff", "#2257a8")
header.set_size((320, 50))

username = InputEntry("Username")
username.set_size((320, 45))

password = InputEntry("Password")
password.set_size((320, 45))

submit = Button("Submit", "#ffffff", "#2257a8")
submit.set_size((320, 45))

lay.add_widget(header)
lay.add_widget(username)
lay.add_widget(password)
lay.add_widget(submit)

win.set_layout(lay)
win.show()
app.run()
