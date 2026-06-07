# Quick Start Guide

## 1. Install dependencies

OhMyGUI is built on `PySide6`. Install it first:

```bash
pip install PySide6
```

Then install the package locally if needed:

```bash
pip install -e .
```

## 2. Basic application

Create a simple window with a label and a button.

```python
import ohmygui as omg

app = omg.core.Application()
window = omg.core.Window("Hello, OhMyGUI!", (480, 320))

label = omg.widget.Text("Welcome to OhMyGUI", "#000000", "#f0f0f0")
button = omg.widget.Button("Click me", "#ffffff", "#1b7cff")

button.on_click(lambda: print("Button clicked!"))

window.bind_widget(label, (50, 50))
window.bind_widget(button, (50, 120))

window.show()
app.run()
```

## 3. Use layouts

Layouts help manage widget arrangement automatically.

```python
layout = omg.layout.VerticalLayout()
layout.add_margin(12)
layout.add_spacing(8)
layout.add_widget(omg.widget.Text("Title", "#ffffff", "#333333"))
layout.add_widget(omg.widget.Button("Start", "#ffffff", "#0078d4"))

window.set_layout(layout)
```

Supported layout types:

- `omg.layout.VerticalLayout`
- `omg.layout.HorizentalLayout`
- `omg.layout.GridLayout`
- `omg.layout.FormLayout`

## 4. Relative positioning

Use relative binding to keep widgets centered or anchored during resize.

```python
center_label = omg.widget.Text("Centered", "#ffffff", "#444444")
window.relative_bind(center_label, (0.5, 0.5))
```

## 5. Input and events

Example of input events:

```python
entry = omg.widget.InputEntry("Enter text...", "")
entry.on_submit(lambda: print("Submit:", entry.value))
window.bind_widget(entry, (50, 190))
```

Example of resize and close callbacks:

```python
window.on_resize(lambda w, h: print(f"Window resized: {w}x{h}"))
window.on_close(lambda event: print("Window closing"))
```

## 6. Dialogs

Basic dialogs are available under `omg.dialog`.

```python
from ohmygui.dialog.enums import Icon, Button as DialogButton

msg = omg.dialog.MessageBox(
    "Info",
    "This is a message.",
    icon=Icon.Information,
    buttons=DialogButton.Ok,
)
msg.show()

picker = omg.dialog.ColorPicker("Choose color", "Pick a color")
color = picker.get_color()
print("Selected color:", color)
```

## 7. Advanced widgets

Advanced widgets include:

- `omg.widget.RadioButton`
- `omg.widget.ComboBox`
- `omg.widget.ListWidget`
- `omg.widget.Table`
- `omg.widget.Slider`
- `omg.widget.Progress`
- `omg.widget.TextEdit`
- `omg.widget.Canvas`

Example:

```python
slider = omg.widget.Slider(0, 100, "#ffffff", "#333333")
progress = omg.widget.Progress("#ffffff", "#333333")
slider.on_value_change(lambda value: progress.set_value(value))
window.bind_widget(slider, (50, 220))
window.bind_widget(progress, (50, 270))
```

## 8. Utilities

Play sound:

```python
omg.utils.play_audio("sound.mp3", sync=False)
```

Non-blocking sleep helpers:

```python
omg.utils.sleep.sleep(2.0)
omg.utils.sleep.sleep_ms(500)
```

Console helpers:

```python
from ohmygui.terminal.conio import ConsoleIO
io = ConsoleIO()
io.print("Hello terminal", fg=0xffaa00, bg=0x000000, bold=True)
```

## 9. Styling

Load theme files or inline styles:

```python
window.load_style_from("resources/dark.qss")
window.load_style_string("QPushButton { font-size: 16px; padding: 8px; }")
```

## 10. Quick tips

- `omg.core.App` is an alias for `Application`.
- Always call `window.show()` before `app.run()`.
- Use `bind_widget()` for absolute placement and `set_layout()` for managed layout.
- `window.load_style_from()` supports `.qss` theme files.
