# Example of using events in a custom way. 
# This is not the recommended way to use events, but it is possible.
from ohmygui.core.application import App
from ohmygui.core.window import Window
from ohmygui.widget.basic import *
from ohmygui.dialog import *

# Create basic widgets.
app = App()
win = Window("Event Example", (800, 600))

# Create a button.
button = Button("Click me!", "#ffffff", "#000000")
button.set_size((100, 50))
# Create a text widget to display the event result.
text = Text("Button not clicked yet.", "#000000", "#ffffff")
text.set_size((300, 50))

# Simple event functions for binding.
def on_button_click(_) -> None: # must accept an event argument, even if it's not used.
    text.set_text("Button clicked!")
def on_window_close(_) -> None:
    print("Window is closing...")

button.on_click(on_button_click) # Don't add parentheses, we want to pass the function itself, not call it.
win.on_close(on_window_close)

# Bind widgets on the window.
win.bind_widget(button, 50, 50)
win.bind_widget(text, 50, 100)

# Run
win.show()
app.run()
