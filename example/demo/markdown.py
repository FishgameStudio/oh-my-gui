# Basic markdown viewer.
# Only 36 lines.

from ohmygui import *

app = core.App()
win = core.Window("Simple Markdown Viewer", (1000, 700))

MARKDOWN = """
# Title
## Subtitle
text text text text text
`short code`
**bold text**
*italic text*
"""

with layout.VerticalLayout() as lay:
    store: list[widget.Text] = []
    for line in MARKDOWN.splitlines():
        obj = widget.Text()
        obj.set_color(utils.WHITE, utils.BLACK).set_font(obj.font, 15)
        if line.startswith("# "):
            obj.set_font(obj.font, 50).set_text(line[2:])
        elif line.startswith("## "):
            obj.set_font(obj.font, 25).set_text(line[3:])
        elif line.startswith("**") and line.endswith("**"):
            obj.native.font().setBold(True)
            obj.set_text(line[2:-2])
        elif line.startswith("*") and line.endswith("*"):
            obj.native.font().setItalic(True)
            obj.set_text(line[1:-1])
        elif line.startswith("`") and line.endswith("`"):
            obj.set_font("JetBrains Mono").set_color(utils.WHITE, "#404040").set_text(line[1:-1])
        else:
            obj.set_text(line[:])
            
        store.append(obj)
    for obj in store:
        lay.add_widget(obj)

win.set_bg("#000000").set_layout(lay).show()
app.run()