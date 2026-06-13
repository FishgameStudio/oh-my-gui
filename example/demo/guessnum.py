# Guess number demo.
# Only 31 lines.

from ohmygui import *
from random import randint
app = core.App()
win = core.Window("Guess Number", (1000, 700))
win.set_bg("#a0efa0")

target = randint(1, 100)

with layout.VerticalLayout() as lay:
    lay.set_common_margin(100).set_common_spacing(30)  
    msg = widget.Text("Guess the number between 1 and 100", "#000000", "#00000000")

    msg.set_font("Consolas 14")  

    entry = widget.InputEntry("Enter a valid number...")
    

    def submit() -> None:
        global msg, entry
        text = entry.value.strip()
        digit: int
        try:
            digit = int(text)
        except ValueError:
            msg.set_text("Invalid number!")
            entry.set_value("")
            return
        if digit > target:
            msg.set_text("Too large!")
        elif digit < target:
            msg.set_text("Too small!")
        else:
            msg.set_text("Congratulations! You got it!")
            entry.hide()
    entry.on_submit(submit)

    lay.add_widget(msg).add_widget(entry)

win.set_layout(lay).show()
app.run()