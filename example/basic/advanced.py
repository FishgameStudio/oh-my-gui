# Advanced Example of all custom widgets.
# Demonstrates Button, RadioButton, ComboBox, List, Table, Slider, Progress, TextEdit, Canvas.
# Uses ohmygui style: simple, direct, no complex layouts, bind at (x,y) coordinates.
from ohmygui import *

# Create app and main window.
app = App()
win = Window("Advanced Widget Demo", (900, 700))

# --------------------------
# 1. Button
# --------------------------
button = Button("Click Me!", "#ffffff", "#2c7bd4")
button.set_size((120, 40))

info_text = Text("Event log will show here", "#000000", "#f0f0f0")
info_text.set_size((400, 40))

def on_btn_click(_):
    info_text.set_text(f"[Button] Clicked!\n{info_text.text}")

button.on_click(on_btn_click)

# --------------------------
# 2. RadioButton
# --------------------------
radio1 = RadioButton("Option 1", "#000000", "#ffffff")
radio2 = RadioButton("Option 2", "#000000", "#ffffff")
radio3 = RadioButton("Option 3", "#000000", "#ffffff")
radio1.set_size((120, 30))
radio2.set_size((120, 30))
radio3.set_size((120, 30))

def on_radio(_):
    info_text.set_text(f"[Radio] Selected\n{info_text.text}")

radio1.on_click(on_radio)
radio2.on_click(on_radio)
radio3.on_click(on_radio)

# --------------------------
# 3. ComboBox
# --------------------------
cbox = ComboBox("#000000", "#ffffff")
cbox.set_size((200, 40))
cbox.add_items(["Apple", "Banana", "Cherry", "Date"])

def on_cbox(_):
    info_text.set_text(f"[Combo] Selected: {cbox.current_text}\n{info_text.text}")

cbox.on_selection_change(on_cbox)

# --------------------------
# 4. ListWidget
# --------------------------
list_w = ListWidget("#000000", "#ffffff")
list_w.set_size((250, 180))
list_w.add_items(["First Item", "Second Item", "Third Item", "Fourth Item"])

def on_list(_):
    info_text.set_text(f"[List] Selected: {list_w.current_text}\n{info_text.text}")

list_w.on_selection_change(on_list)

# --------------------------
# 5. Table
# --------------------------
table = Table(0x000000, 0xffffff)
table.set_size((350, 180))
table.set_col_count(2)
table.set_row_count(3)
table.set_headers(["Name", "Value"])
table.set_item(0, 0, "Alice")
table.set_item(0, 1, "95")
table.set_item(1, 0, "Bob")
table.set_item(1, 1, "88")

def on_table(row, col):
    val = table[(row, col)]
    info_text.set_text(f"[Table] Cell ({row},{col}) = {val}\n{info_text.text}")

table.on_cell_click(on_table)

# --------------------------
# 6. Slider + Progress
# --------------------------
slider = Slider(0xffffff,0x333333)
slider.set_size((300, 40))
slider.set_range(0, 100)

progress = Progress("#ffffff", "#333333")
progress.set_size((300, 30))
progress.set_range(0, 100)

def on_slider(val):
    progress.set_value(val)
    info_text.set_text(f"[Slider] Value: {val}\n{info_text.text}")

slider.on_value_change(on_slider)

# --------------------------
# 7. TextEdit
# --------------------------
text_edit = TextEdit("#ffffff", "#252525")
text_edit.set_size((400, 150))
text_edit.set_text("Multi-line editor\nType anything here...\n")

# --------------------------
# 8. Canvas (Drawing)
# --------------------------
canvas = Canvas("#00ff00", "#101010")
canvas.set_size((500, 250))
canvas.make_line(20, 20, 200, 200)
canvas.make_dot(100, 100, 6)
canvas.make_rect(250, 30, 100, 80)
canvas.make_circle(400, 120, 50)

# --------------------------
# Bind all widgets to window
# --------------------------
win.bind_widget(button,    (50, 50))
win.bind_widget(info_text, (50, 110))

win.bind_widget(radio1,    (500, 50))
win.bind_widget(radio2,    (500, 80))
win.bind_widget(radio3,    (500, 110))

win.bind_widget(cbox,      (50, 180))
win.bind_widget(list_w,    (50, 240))
win.bind_widget(table,     (320, 240))

win.bind_widget(slider,    (50, 450))
win.bind_widget(progress,  (50, 500))
win.bind_widget(text_edit, (400, 450))
win.bind_widget(canvas,    (50, 550))

# Window close event
def on_close(_):
    print("Advanced demo window closed.")

win.on_close(on_close)

# Show and run
win.show()
app.run()