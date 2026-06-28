# Example of chain invocation.

from ohmygui import *
from typing import Any

def close(_):
    print("chain demo window closed")

app = Application()
win = Window()
win.set_bg("#a0a0a0a0").load_style_string(
    """
/* Dark Mode - Base */
* {
    background-color: #1a1a1a;
    color: #eeeeee;
    border: none;
    font-family: Arial;
}

/* Button */
QPushButton {
    background-color: #333333;
    padding: 6px 12px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #444444;
}
QPushButton:pressed {
    background-color: #555555;
}

/* RadioButton */
QRadioButton::indicator {
    background-color: #2a2a2a;
    border: 1px solid #777;
    border-radius: 8px;
    width: 14px;
    height: 14px;
}
QRadioButton::indicator:checked {
    background-color: #ffffff;
    border: 2px solid #aaa;
}

/* ComboBox */
QComboBox {
    background-color: #2a2a2a;
    border: 1px solid #555;
    padding: 4px;
    border-radius: 4px;
}
QComboBox::drop-down {
    border: none;
}
QComboBox::down-arrow {
    background-color: #eee;
    width: 8px;
    height: 8px;
}

/* Slider */
QSlider::groove:horizontal {
    background: #444;
    height: 6px;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #eee;
    width: 16px;
    height: 16px;
    border-radius: 8px;
}

/* ProgressBar */
QProgressBar {
    background-color: #333;
    color: #eee;
    border-radius: 4px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #eeeeee;
    border-radius: 4px;
}

/* TextEdit & ListWidget & Table */
QTextEdit, QListWidget, QTableWidget {
    background-color: #252525;
    color: #eeeeee;
    border: 1px solid #555;
}
QListWidget::item:selected {
    background-color: #5588ff;
    color: #fff;
}
QTableWidget::item:selected {
    background-color: #5588ff;
    color: #fff;
}
"""
).on_close(close)

FONT = "Courier New"

text = Text("Nothing submited.", "#000000", "#00000000")
text.set_font(FONT).set_size((300, 100)).set_rounded_corner(8)
cnt = 0

def submit():
    global text, cnt
    text.set_text(f"You submited {cnt} time(s)! Content: {entry.value}")
    cnt += 1


entry = InputEntry("Enter...", "No content.")
# chain invote.
entry.set_size((300, 100)).set_font(FONT).set_shadow(20, 10, 10, "#30308080").set_rounded_corner(8).on_submit(submit)

win.relative_bind(text, (0.5, 0.2)).relative_bind(entry, (0.5, 0.6)).show()
app.run()
