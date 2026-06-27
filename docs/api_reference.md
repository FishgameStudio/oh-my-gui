# OhMyGUI API Reference

## Package overview

Import root modules:

- `import ohmygui as omg`
- `from ohmygui import core, widget, dialog, layout, utils, terminal, oml`

Root packages expose:

- `omg.core` - application wrapper, `Window`, mouse helpers, bind decorator
- `omg.widget` - base widgets, standard UI controls, advanced widgets, page interface
- `omg.layout` - layout containers for window content
- `omg.dialog` - standard dialogs and helper enums
- `omg.utils` - color constants, audio playback, environment and OS helpers, sleep and version checks
- `omg.terminal` - console ANSI output helpers
- `omg.oml` - OML parser and conversion utilities

---

## `ohmygui.core`

### `Application`

A singleton application wrapper around `PySide6`.

Constructor:

- `Application()` - returns the shared application instance

Methods:

- `init_widget_mode() -> Self` - initialize Qt widget mode (`QApplication`)
- `init_qml_mode() -> Self` - initialize QML mode (`QGuiApplication`)
- `run() -> int` - run the Qt event loop
- `on_quit(event: Event) -> None` - bind application quit callback
- `load_style_from(path: str) -> Self` - load a QSS stylesheet from a file
- `load_style_string(qss: str) -> Self` - load stylesheet from a string
- `load_oms_string(oms: str) -> Self` - load OMS stylesheet string
- `load_oms_from(path: str) -> Self` - load OMS stylesheet from a file
- `load_oml_string(oml: str) -> Self` - convert and load OML from a string
- `load_oml_from(path: str) -> Self` - convert and load OML from a file
- `load_qml_from(path: str) -> Self` - load a QML file into the QML engine

Properties:

- `is_qml_mode: bool` - whether current app is in QML mode

Aliases:

- `App = Application`

### `Window`

Main application window wrapper.

Constructor:

- `Window(title: str = "", size: tuple[int, int] = (800, 500))`

Properties:

- `x`, `y`, `w`, `h` - window geometry
- `size` - `(width, height)` tuple
- `parent` - Qt parent object
- `children` - Qt child objects
- `top_widget` - most recently bound widget
- `top_widgets` - deprecated alias for `toplevel_widget`
- `toplevel_widget` - top-level native window widget
- `native` - underlying `QMainWindow`
- `bg_color` - current background color string
- `menus` - added menu list

Methods:

- `set_size(size: tuple[int, int]) -> Self`
- `set_position(pos: tuple[int, int]) -> Self`
- `set_icon(ico_path: str) -> Self`
- `fix_size() -> Self`
- `unfix_size() -> Self`
- `bind_widget(widget: BaseWidget, dir: tuple[int, int]) -> Self`
- `relative_bind(widget: BaseWidget, reldir: tuple[float, float]) -> Self`
- `set_parent(parent: Window) -> Self`
- `set_layout(layout: BaseLayout) -> Self`
- `set_interface(interface: Interface) -> Self`
- `load_style_from(path: str) -> Self`
- `load_style_string(qss: str) -> Self`
- `load_oms_string(oms: str) -> Self`
- `load_oms_from(path: str) -> Self`
- `export_QSS -> str` - get current stylesheet
- `on_resize(callback: Callable[[int, int], None]) -> Self`
- `show() -> Self`
- `hide() -> Self`
- `close() -> Self`
- `on_close(event: Callable[[Any], None]) -> Self`
- `set_bg(color: str) -> Self`
- `add_menu(name: str, shortcut: str, actions: list[tuple[str, Callable] | None]) -> Self`
- `destroy() -> Self`
- `set_frameless(option: bool) -> Self`
- `snap(layout: WinSize) -> Self`

Enums:

- `WinSize` - `Maximum`, `Minimum`, `Regular`, `Left`, `Right`, `Top`, `Bottom`

### Mouse helpers

- `get_mouse_x() -> int`
- `get_mouse_y() -> int`
- `set_mouse_pos(pos: tuple[int, int]) -> None`

### Binding helper

- `bind(register_method)` - decorator that binds a function through a register method, such as `core.bind(win.on_close)`

---

## `ohmygui.widget`

### `BaseWidget`

Common widget base class for all widgets.

Methods:

- `show() -> Self`
- `hide() -> Self`
- `set_pos(x: int, y: int, w: int | None = None, h: int | None = None) -> Self`
- `set_size(size: tuple[int, int]) -> Self`
- `set_transparency(val: float) -> Self`
- `on_hover(enter, leave=None, move=None) -> Self`
- `load_stylesheet(qss: str) -> Self`
- `load_omstylesheet(oms: str) -> Self`
- `lock() -> Self`
- `unlock() -> Self`
- `set_rounded_corner(radius: int) -> Self`
- `on_any_keypressed(callback: Callable[[int], None]) -> Self`
- `on_keypress(ascii: int, callback: Callable[[], None]) -> Self`
- `set_shadow(blur_radius: int = 10, x_offset: int = 0, y_offset: int = 3, color: str = "#00000080") -> Self`
- `remove_shadow() -> Self`
- `get_size -> tuple[int, int]`
- `native` - underlying Qt widget

Properties:

- `x_pos`, `y_pos`, `width`, `height`
- `is_locked`

### `Text`

Label widget.

Constructor:

- `Text(text: str = "", fg: str = "#000000", bg: str = "#ffffff")`

Methods:

- `set_text(text: str) -> Self`
- `set_foreground(fg: str) -> Self`
- `set_background(bg: str) -> Self`
- `set_color(fg: str, bg: str) -> Self`
- `set_font(font: str, size: int | None = None, bold: bool = False, italic: bool = False) -> Self`

Properties:

- `text`, `fg`, `bg`, `font`

### `Button`

Clickable push button.

Constructor:

- `Button(text: str, fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `set_text(text: str) -> Self`
- `set_foreground(fg: str) -> Self`
- `set_background(bg: str) -> Self`
- `set_color(fg: str, bg: str) -> Self`
- `on_click(event) -> Self`
- `set_font(font: str, size: int | None = None, bold: bool = False, italic: bool = False) -> Self`

Properties:

- `text`, `fg`, `bg`, `font`

### `InputEntry`

Single-line text input.

Constructor:

- `InputEntry(default_prompt: str = "", default_value: str = "")`

Methods:

- `set_value(value: str) -> Self`
- `clear_value() -> Self`
- `on_submit(event) -> Self`
- `on_key_press(callback: Callable[[str], None]) -> Self`
- `set_font(font: str, size: int | None = None, bold: bool = False, italic: bool = False) -> Self`

Properties:

- `value`, `font`

### `PasswordEntry`

Password input field.

Constructor:

- `PasswordEntry(default_prompt: str = "Password: ", default_value: str = "")`

Methods:

- `show_password() -> Self`
- `hide_password() -> Self`
- `on_submit(event) -> Self`
- `set_font(font: str, size: int | None = None, bold: bool = False, italic: bool = False) -> Self`

Properties:

- `value`, `font`

### `RadioButton`

Single-selection radio button.

Constructor:

- `RadioButton(text: str, fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `set_text(text: str) -> Self`
- `set_checked(state: bool) -> Self`
- `on_click(event) -> Self`
- `set_color(fg: str, bg: str) -> Self`
- `set_font(font: str) -> Self`

Properties:

- `text`, `fg`, `bg`, `checked`

### `ComboBox`

Dropdown selector.

Constructor:

- `ComboBox(fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `add_item(text: str) -> Self`
- `add_items(items: list[str]) -> Self`
- `clear_items() -> Self`
- `set_current_index(index: int) -> Self`
- `on_selection_change(event) -> Self`
- `set_color(fg: str, bg: str) -> Self`
- `set_font(font: str) -> Self`

Properties:

- `current_text`, `current_index`, `fg`, `bg`

### `ListWidget`

List selection widget.

Constructor:

- `ListWidget(fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `add_item(text: str) -> Self`
- `add_items(items: list[str]) -> Self`
- `clear_items() -> Self`
- `remove_current_item() -> Self`
- `set_current_index(index: int) -> Self`
- `on_selection_change(event) -> Self`
- `set_color(fg: str, bg: str) -> Self`
- `set_font(font: str) -> Self`

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

Slider control.

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

- `set_foreground(fg: str) -> Self`
- `set_background(bg: str) -> Self`
- `set_color(fg: str, bg: str) -> Self`
- `make_dot(x: float, y: float, size: float = 4) -> Self`
- `make_line(x1: float, y1: float, x2: float, y2: float) -> Self`
- `make_rect(x: float, y: float, w: float, h: float) -> Self`
- `make_circle(x: float, y: float, radius: float) -> Self`
- `clear() -> Self`
- `set_font(font: str) -> Self`

Properties:

- `fg`, `bg`

### `Picture`

Image widget supporting raster and SVG images.

Constructor:

- `Picture(path: str)`

Methods:

- `load_picture(path: str) -> Self`

Properties:

- `is_svg`

### `Video`

Video playback widget.

Constructor:

- `Video(path)`

Methods:

- `play() -> Self`
- `stop() -> Self`
- `set_fullscreen(option: bool) -> Self`
- `set_loop(option: bool) -> Self`

Properties:

- `audio_output`, `player_object`, `is_playing`

### `SplashScreen`

Startup splash widget.

Constructor:

- `SplashScreen(pixmap: QPixmap, fg: str = "#ffffff", bg: str = "#000000")`

Methods:

- `set_color(fg: str, bg: str) -> Self`
- `set_foreground(fg: str) -> Self`
- `set_background(bg: str) -> Self`
- `show_message(msg: str, align: int = 64) -> Self`
- `finish(main_win: Any) -> Self`
- `show() -> Self`
- `close() -> Self`
- `set_font(font: str) -> Self`

---

## `ohmygui.widget.page`

### `Page`

- `Page(layout: BaseLayout)`
- `set_layout(layout: BaseLayout) -> Self`
- `show() -> Self`
- `hide() -> Self`

### `Interface`

- `Interface(pages: list[Page])`
- `all_pages -> list[Page]`
- `set_active_page(idx: int) -> Self`

---

## `ohmygui.layout`

### `BaseLayout`

Common layout base class.

Methods:

- `add_widget(widget: BaseWidget) -> Self`
- `delete_widget(widget: BaseWidget) -> Self`
- `clear() -> Self`
- `add_layout(layout: BaseLayout) -> Self`
- `lock() -> Self`
- `unlock() -> Self`

Properties:

- `is_locked`, `native`

### `BoxLayout`

- `add_stretch(stretch: int = 0) -> Self`
- `add_spacing(size: int) -> Self`
- `set_common_spacing(size: int) -> Self`
- `set_common_margin(size: int) -> Self`
- `set_common_stretch(stretch: int) -> Self`

### `VerticalLayout`

- `add_stretch() -> Self`
- `add_spacing(size: int) -> Self`
- `add_margin(size: int) -> Self`
- `set_common_spacing(size: int) -> Self`
- `set_common_margin(size: int) -> Self`
- `set_common_stretch(stretch: int) -> Self`

### `HorizentalLayout`

- `add_stretch() -> Self`
- `add_spacing(size: int) -> Self`
- `add_margin(size: int) -> Self`
- `set_common_spacing(size: int) -> Self`
- `set_common_margin(size: int) -> Self`
- `set_common_stretch(stretch: int) -> Self`

### `GridLayout`

- `add_widget(widget: BaseWidget, row: int = 0, column: int = 0, row_span: int = 1, column_span: int = 1) -> Self`
- `add_margin(size: int) -> Self`
- `set_common_spacing(size: int) -> Self`
- `set_common_margin(size: int) -> Self`

### `FormLayout`

- `add_widget(widget: BaseWidget, label: str = "") -> Self`
- `add_margin(size: int) -> None`
- `set_common_spacing(size: int) -> None`
- `set_common_margin(size: int) -> None`

---

## `ohmygui.dialog`

### `BaseDialog`

Base dialog window.

Methods:

- `show() -> Self`
- `hide() -> Self`
- `close() -> Self`
- `set_title(title: str) -> Self`
- `set_content(content: str) -> Self`
- `load_stylesheet(qss: str) -> Self`
- `lock() -> Self`
- `unlock() -> Self`

Properties:

- `is_locked`, `get_title`, `get_content`, `native`

### `MessageBox`

Standard message dialog.

Constructor:

- `MessageBox(title: str, content: str, icon: Icon = Icon.NoIcon, buttons: Button = Button.Ok)`

Methods:

- `set_icon(icon: QMessageBox.Icon) -> Self`
- `set_content(content: str) -> Self`
- `set_info(info: str) -> Self`
- `set_detail(detail: str) -> Self`
- `on_click(event: Callable[[int], None])`
- `set_buttons(buttons: Button) -> Self`

### `FileChooser`

File selection dialog.

Constructor:

- `FileChooser(title: str)`

Methods:

- `get_selections() -> list[str]`
- `set_default_dir(dir: str) -> None`

### `ColorPicker`

Color selection dialog.

Constructor:

- `ColorPicker(title: str, content: str)`

Methods:

- `get_color() -> str`

### Enums

- `Icon` - imported from `PySide6.QtWidgets.QMessageBox.Icon`
- `Button` - imported from `PySide6.QtWidgets.QMessageBox.StandardButton`

---

## `ohmygui.utils`

### `constants`

Color constants:

- `WHITE`, `BLACK`, `GRAY`, `RED`, `ORANGE`, `YELLOW`, `GREEN`, `CYAN`, `BLUE`, `PURPLE`, `PINK`
- `LIGHT_GRAY`, `LIGHT_RED`, `LIGHT_ORANGE`, `LIGHT_YELLOW`, `LIGHT_GREEN`, `LIGHT_CYAN`, `LIGHT_BLUE`, `LIGHT_PURPLE`, `LIGHT_PINK`
- `DARK_GRAY`, `DARK_RED`, `DARK_ORANGE`, `DARK_YELLOW`, `DARK_GREEN`, `DARK_CYAN`, `DARK_BLUE`, `DARK_PURPLE`, `DARK_PINK`

Message box templates:

- `ASSERTION`, `ERROR`, `WARNING`, `SAVE_FILE`, `CANT_OPEN_FILE`, `FILE_NOT_FOUND`, `OVERWRITE_FILE`, `INFO`, `CONFIRM_EXIT`, `PERMISSION_DENIED`

### `sound`

- `play_audio(file_path: str, *, sync: bool = False) -> None`

Supported audio formats: `.wav`, `.mp3`

### `utils`

- `get_environment_variable(key: str, default: str | None = None) -> str`
- `set_clip(text: str, /, *, strip: bool = True, encoding: str = "utf-8", errors: str = "strict")`
- `get_clip() -> str`
- `get_user_root_dir() -> str`
- `send_system_notification(title_: str, text_: str) -> None`

### `sleep`

- `sleep(second: float) -> None` - non-blocking sleep using a daemon thread
- `sleep_ms(millisecond: int) -> None` - non-blocking sleep in milliseconds

### `vercheck`

- `get_latest_ver(pkg: str = "oh-my-gui") -> Optional[str]`
- `get_local_version() -> str`
- `compare_ver(v1: str, v2: str) -> Literal[-1, 0, 1]`
- `is_latest_version() -> bool`
- `upgrade_ohmygui() -> bool`

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

## `ohmygui.oml`

### `convert_oml_to_qml`

Convert OML source into a QML string.

---

## Notes

- `ohmygui.core.Application` is a singleton. Use `App = Application` or `Application()` to get the instance.
- Use `Window.show()` before `Application.run()`.
- Bind widgets directly with `bind_widget()` or use `set_layout()` to apply a layout.
- `Window.load_style_from()` accepts QSS files for theming.
- `Application.load_oml_from()` / `load_oml_string()` can load OML source through the internal OML converter.
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
