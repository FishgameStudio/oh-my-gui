# OhMyGUI API Reference

## Package overview

Import root modules:

- `import ohmygui as omg`
- `from ohmygui import core, widget, dialog, layout, utils, terminal`

Root packages expose:

- `omg.core` - application, window, mouse utilities
- `omg.widget` - base widgets, basic widgets, advanced widgets, event helper
- `omg.layout` - layout containers for window content
- `omg.dialog` - standard dialog windows and helper enums
- `omg.utils` - color constants, sound playback, sleep helpers
- `omg.terminal` - console styling and IO utilities

---

## `ohmygui.core`

### `Application`

A singleton application wrapper around `PySide6`.

Methods:

- `Application()` - get the application instance
- `init_widget_mode()` - initialize desktop widget mode (`QApplication`)
- `init_qml_mode()` - initialize QML mode (`QGuiApplication`)
- `run() -> int` - run the application event loop
- `on_quit(event: Event) -> None` - bind application quit callback
- `load_qml_from(path: str) -> None` - load a QML file and start QML engine

Properties:

- `is_qml_mode: bool` - true when in QML mode

Methods:

`set_size(size: tuple[int, int]) -> Self`
`set_position(x: int, y: int) -> Self`
`get_size -> tuple[int, int]`
`fix_size() -> Self`
`unfix_size() -> Self`
`bind_widget(widget: BaseWidget, dir: tuple[int, int]) -> Self`
`relative_bind(widget: BaseWidget, reldir: tuple[float, float]) -> Self`
`set_parent(parent: Window) -> Self`
`set_layout(layout: BaseLayout) -> Self`
`load_style_from(path: str) -> Self`
`load_style_string(qss: str) -> Self`
`export_QSS -> str`
`on_resize(callback: Callable[[int, int], None]) -> Self`
`show() -> Self`
`hide() -> Self`
`close() -> Self`
`on_close(event: Callable[[Any], None]) -> Self`
`set_bg(color: str) -> Self`

Properties:

`x`, `y`, `w`, `h` - window geometry
`bg_color: str` - current background color
`top_widget` - most recently bound widget
`top_widgets` - top-level native window/widget
`children` - Qt children objects
`parent` - window parent
`native` - underlying `QMainWindow`

### Mouse helpers

- `get_mouse_x() -> int`
- `get_mouse_y() -> int`
- `set_mouse_pos(pos: tuple[int, int]) -> None`

---

## `ohmygui.widget`

### `BaseWidget`

Common widget base class.

Methods:
`show()`, `hide()`
`set_pos(x: int, y: int, w: int | None = None, h: int | None = None) -> Self`
`set_size(size: tuple[int, int]) -> Self`
`set_transparency(val: float) -> Self`
`on_hover(enter, leave=None, move=None) -> Self`
`load_stylesheet(qss: str) -> Self`
`lock() -> Self`
`unlock() -> Self`
`set_rounded_corner(radius: int) -> Self`
`on_any_keypressed(callback: Callable[[int], None]) -> Self`
`on_keypress(ascii: int, callback: Callable[[], None]) -> Self`
`set_shadow(blur_radius: int = 10, x_offset: int = 0, y_offset: int = 3, color: str = "#00000080") -> Self`
`remove_shadow() -> Self`
`get_size -> tuple[int, int]`
`native` - underlying Qt widget

Properties:

- `x_pos`, `y_pos`, `width`, `height`
- `is_locked` - whether the widget is disabled

### `Text`

A label widget.

Constructor:

- `Text(text: str = "", fg: str = "#000000", bg: str = "#ffffff")`

Methods:

- `set_text(text: str) -> None`
- `set_foreground(fg: str) -> None`
- `set_background(bg: str) -> None`
- `set_color(fg: str, bg: str) -> None`
- `set_font(font: str) -> None`

Properties:

- `text`, `fg`, `bg`

### `Button`

A clickable push button.

Constructor:

- `Button(text: str, fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `set_text(text: str) -> None`
- `set_foreground(fg: str) -> None`
- `set_background(bg: str) -> None`
- `set_color(fg: str, bg: str) -> None`
- `on_click(event) -> None`
- `set_font(font: str) -> None`

Properties:

- `text`, `fg`, `bg`

### `InputEntry`

Single-line text input.

Constructor:

- `InputEntry(default_prompt: str = "", default_value: str = "")`

Methods:

- `set_value(value: str) -> Self`
- `on_submit(event) -> Self`
- `on_key_press(callback: Callable[[str], None]) -> Self`

Property:

- `value`

### `PasswordEntry`

Password input field.

Constructor:

- `PasswordEntry(default_prompt: str = "Password: ", default_value: str = "")`

Methods:

- `show_password() -> None`
- `hide_password() -> None`
- `on_submit(event) -> None`
- `set_font(font: str) -> None`

Property:

- `value`

### `RadioButton`

Single-selection radio button.

Constructor:

- `RadioButton(text: str, fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `set_text(text: str) -> None`
- `set_checked(state: bool) -> None`
- `on_click(event) -> None`
- `set_color(fg: str, bg: str) -> None`
- `set_font(font: str) -> None`

Properties:

- `text`, `fg`, `bg`, `checked`

### `ComboBox`

Dropdown selector.

Constructor:

- `ComboBox(fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `add_item(text: str) -> None`
- `add_items(items: list[str]) -> None`
- `clear_items() -> None`
- `set_current_index(index: int) -> None`
- `on_selection_change(event) -> None`
- `set_color(fg: str, bg: str) -> None`
- `set_font(font: str) -> None`

Properties:

- `current_text`, `current_index`, `fg`, `bg`

### `ListWidget`

List selection widget.

Constructor:

- `ListWidget(fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `add_item(text: str) -> None`
- `add_items(items: list[str]) -> None`
- `clear_items() -> None`
- `remove_current_item() -> None`
- `set_current_index(index: int) -> None`
- `on_selection_change(event) -> None`
- `set_color(fg: str, bg: str) -> None`
- `set_font(font: str) -> None`

Properties:

- `current_text`, `current_index`, `fg`, `bg`

### `Table`

Grid table widget.

Constructor:

- `Table(rows: int = 0, cols: int = 0, fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `set_headers(headers: list[str]) -> Self`
- `set_item(row: int, col: int, text: str) -> Self`
- `add_row() -> Self`
- `remove_row(row: int) -> Self`
- `clear() -> Self`
- `clear_all() -> Self`
- `set_row_count(rows: int) -> Self`
- `set_col_count(cols: int) -> Self`
- `on_cell_click(event) -> Self`
- `set_color(fg: str, bg: str) -> Self`
- `set_font(font: str) -> Self`

Properties:

- `row_count`, `col_count`, `current_row`, `current_col`, `fg`, `bg`

### `Slider`

Horizontal slider control.

Constructor:

- `Slider(min_val: int = 0, max_val: int = 100, fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `set_value(val: int) -> Self`
- `set_range(min_val: int, max_val: int) -> Self`
- `set_single_step(step: int) -> Self`
- `set_page_step(step: int) -> Self`
- `on_value_change(event) -> Self`
- `set_color(fg: str, bg: str) -> Self`
- `set_font(font: str) -> Self`

Properties:

- `value`, `min_value`, `max_value`, `fg`, `bg`

### `Progress`

Progress bar.

Constructor:

- `Progress(fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `set_value(value: int) -> Self`
- `set_range(min_val: int, max_val: int) -> Self`
- `reset() -> Self`
- `on_value_change(event) -> Self`
- `set_color(fg: str, bg: str) -> Self`
- `set_font(font: str) -> Self`

Properties:

- `value`, `maximum`, `minimum`, `fg`, `bg`

### `TextEdit`

Multi-line text editor.

Constructor:

- `TextEdit(fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `set_text(text: str) -> Self`
- `append(text: str) -> Self`
- `clear() -> Self`
- `set_color(fg: str, bg: str) -> Self`
- `set_font(font: str) -> Self`

Properties:

- `text`, `fg`, `bg`

### `Canvas`

Basic drawing view.

Constructor:

- `Canvas(fg: str = "#ffffff", bg: str = "#222222")`

Methods:

- `set_foreground(fg: str) -> None`
- `set_background(bg: str) -> None`
- `set_color(fg: str, bg: str) -> None`
- `make_dot(x: float, y: float, size: float = 4) -> None`
- `make_line(x1: float, y1: float, x2: float, y2: float) -> None`
- `make_rect(x: float, y: float, w: float, h: float) -> None`
- `make_circle(x: float, y: float, radius: float) -> None`
- `clear() -> None`
- `set_font(font: str) -> None`

Properties:

- `fg`, `bg`

### `Event`

Event helper for callbacks.

- `Event(func: Callable)`
- `set_func(func: Callable)`
- `get_func -> Callable`

---

## `ohmygui.layout`

### `BaseLayout`

Common layout base.

Methods:

- `add_widget(widget: BaseWidget) -> None`
- `delete_widget(widget: BaseWidget) -> None`
- `clear() -> None`
- `add_layout(layout: BaseLayout) -> None`
- `lock() -> None`
- `unlock() -> None`

Properties:

- `is_locked`, `native`

### `VerticalLayout`

- `add_stretch() -> None`
- `add_spacing(size: int) -> None`
- `add_margin(size: int) -> None`
- `set_common_spacing(size: int) -> None`
- `set_common_margin(size: int) -> None`
- `set_common_stretch(stretch: int) -> None`

### `HorizentalLayout`

- `add_stretch() -> None`
- `add_spacing(size: int) -> None`
- `add_margin(size: int) -> None`
- `set_common_spacing(size: int) -> None`
- `set_common_margin(size: int) -> None`
- `set_common_stretch(stretch: int) -> None`

### `GridLayout`

- `add_widget(widget: BaseWidget, row: int = 0, column: int = 0, row_span: int = 1, column_span: int = 1) -> None`
- `add_margin(size: int) -> None`
- `set_common_spacing(size: int) -> None`
- `set_common_margin(size: int) -> None`

### `FormLayout`

- `add_widget(widget: BaseWidget, label: str = "") -> None`
- `add_margin(size: int) -> None`
- `set_common_spacing(size: int) -> None`
- `set_common_margin(size: int) -> None`

---

## `ohmygui.dialog`

### `BaseDialog`

Base dialog window.

Methods:

- `show() -> None`
- `hide() -> None`
- `close() -> None`
- `set_title(title: str) -> None`
- `set_content(content: str) -> None`
- `load_stylesheet(qss: str) -> None`
- `lock() -> None`
- `unlock() -> None`

Properties:

- `is_locked`, `get_title`, `get_content`, `native`

### `MessageBox`

Standard message dialog.

Constructor:

- `MessageBox(title: str, content: str, icon: Icon = Icon.NoIcon, buttons: Button = Button.Ok)`

Methods:

- `set_icon(icon: QMessageBox.Icon) -> None`
- `set_content(content: str) -> None`
- `set_info(info: str) -> None`
- `set_detail(detail: str) -> None`
- `on_click(event: Callable[[int], None])`
- `set_buttons(buttons: Button) -> None`

### `FileChooser`

File selection dialog.

Methods:

- `get_selections() -> list[str]`

### `ColorPicker`

Color selection dialog.

Methods:

- `get_color() -> str`

### `Icon`, `Button`

Enums imported from `PySide6.QtWidgets.QMessageBox`.

---

## `ohmygui.utils`

### `constants`

Color constants:

- `WHITE`, `BLACK`, `GRAY`, `RED`, `ORANGE`, `YELLOW`, `GREEN`, `CYAN`, `BLUE`, `PURPLE`, `PINK`, plus light/dark variants.

Message box templates:

- `ASSERTION`, `ERROR`, `WARNING`, `SAVE_FILE`, `CANT_OPEN_FILE`, `OVERWRITE_FILE`, `INFO`, `CONFIRM_EXIT`, `PERMISSION_DENIED`

### `sound`

- `play_audio(file_path: str, *, sync: bool = False) -> None`

Supported formats: `.wav`, `.mp3`

### `sleep`

- `sleep(second: float) -> None`
- `sleep_ms(millisecond: int) -> None`

---

## `ohmygui.terminal`

### `ConsoleIO`

Console helper for colored output.

Constructor:

- `ConsoleIO(fg: int = 0xffffff, bg: int = 0x000000)`

Methods:

- `hex2ansi(rgb: int, *, bg: bool = False, highlight: bool = False, bold: bool = False, italic: bool = False, underline: bool = False) -> str`
- `print(text: str, *, fg: int | None = None, bg: int | None = None, highlight: bool = False, bold: bool = False, italic: bool = False, underline: bool = False, end: str = "\n") -> Self`
- `input(prompt: str, *, fg: int | None = None, bg: int | None = None, highlight: bool = False, bold: bool = False, italic: bool = False, underline: bool = False, callback: Callable[[str], None] | None = None) -> str`
- `make_progress(prompt: str, total: int, curr: int) -> Self`

---

## Notes

- `ohmygui.core.Application` is a singleton.
- Use `Window.show()` before `Application.run()`.
- Bind widgets directly with `bind_widget()` or use `set_layout()` to apply a layout.
- `Window.load_style_from()` accepts QSS files for theming.
