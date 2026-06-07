import ohmygui as omg

# Create application.
app = omg.core.Application()
# Create main window.
win = omg.core.Window("Hello, OhMyGUI!", (400, 300))
# Set size.
win.set_size((800, 600))
# Set window background color.
win.set_bg("#cccccc")
# Create a label.
label = omg.widget.Text("Welcome to OhMyGUI!", "#ffffff", "#0000ff")
# Set size.
label.set_size((200, 50))
# Create a button.
button = omg.widget.Button("Click me!", "#ffffff", "#000000")
# Set size.
button.set_size((100, 50))
# Bind the label and button to the window.
win.bind_widget(label, (50, 50))
win.bind_widget(button, (50, 200))
# Show the window.
win.show()
# Run the application.
app.run()

