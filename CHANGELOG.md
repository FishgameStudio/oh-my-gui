# THE CHANGELOG

## Changelog of \[v1.1.0\]

### Added
- **Core System**
  - Added `core.bind` module with `@bind` decorator for cleaner event callback registration
  - Added page management system under `widget.page`, including `Page` component and `Interface` multi-page controller
  - Added `Window.set_interface()` method to mount multi-page manager directly on window
- **Window Capabilities**
  - Added `WinSize` enum and `Window.snap()` method for one-click window tiling (left / right / top / bottom / maximize / minimize)
  - Added `Window.set_icon()` method with built-in handling for file missing and permission errors
  - Added `Window.destroy()` method for active window instance destruction
  - Enabled dock widget nesting support for more flexible layout composition
  - Introduced `weakref.finalize` destructor to auto-clean caches and native widget resources on window disposal
- **Extension Widgets**
  - Added `SplashScreen` startup splash widget with custom background color and loading message support
  - Added `IntegerEntry` (QSpinBox wrapper) with configurable range, step and value change callback
  - Added `DoubleEntry` (QDoubleSpinBox wrapper) with adjustable decimal precision
  - Added `Dial` rotary control with notch visibility toggle and value change events
  - Added `Tree` tree view widget with multi-level nodes, expand/collapse and click / double-click callbacks
- **Version & Upgrade System**
  - Added `utils.vercheck` module, including PyPI latest version query, semantic version comparison and auto-upgrade capability
  - Automatic version check runs on library import, with interactive one-click upgrade in terminal environments
  - Added `OMGUI_NO_AUTO_UPGRADE=1` environment variable to disable the upgrade reminder
- **Project & Docs**
  - Added official `CHANGELOG.md` file to track version changes
  - Updated README Roadmap with full iteration plan from v1.1.0 to v2.0.0
  - Added `requests` and `packaging` as dependencies for version check functionality

### Changed
- Updated `__all__` export lists across all modules to align with newly added submodules
- Added permission exception capture and error logging in `Window.load_style_from()`
- Unified exception fallback logic for style sheet loading and window icon setting
- Added `python.REPL.enableREPLSmartSend` rule to VSCode settings for consistent development environment

### Deprecated
- `Window.top_widgets` property is marked as deprecated. Use `toplevel_widget` instead.

# Changelog of \[v1.2.0]

### Added

#### Core Engine \& Custom Syntax System

* **Full OMS (Oh My Stylesheet) V2 Engine**
* Added brand new `core.oms` module, implements OMS markup to standard QSS compilation
* Supports unit suffixes (`px/em/pt`), hex/RGB color literals without quotes, global variables `$xxx`
* Supports reusable global `@style` blocks, `use` inheritance keyword, multi-state widget chain (`:hover:pressed`)
* Added `rect{}` shorthand syntax for rapid size/background configuration, built-in boolean/None constants
* Fixed traditional @import file reading bugs in original stylesheet parser
* **Full OML (Oh My Modeling Language) Engine**
* Added brand new `oml` top-level module with complete OML-to-QML compiler
* Supports parametric `@template` component macros, global `@meta` metadata blocks
* Added signal binding syntax `-> func::slot` for one-line event registration
* Compatible with OMS core syntax features (variables, style inheritance, rect shorthand)
* Exposed top-level API: `convert\_oml\_to\_qml` for manual syntax conversion

#### Application \& Window Core API Expansion

* Extended `core.Application` singleton with full style/OML loading capabilities
* Added `load\_style\_from()` / `load\_style\_string()` for standard QSS loading
* Added `load\_oms\_from()` / `load\_oms\_string()` for direct OMS stylesheet parsing \& loading
* Added `load\_oml\_from()` / `load\_oml\_string()` for OML markup compilation and QML engine loading
* Added `App = Application` global alias for simpler code writing
* Extended `core.Window` with OMS native support: `load\_oms\_from()` / `load\_oms\_string()`
* Added `Window.set\_frameless()` method for one-click frameless window configuration
* Added robust exception handling for style/OMS/OML file missing and permission errors

#### Widget System Expansion

* Added `BaseWidget.load\_omstylesheet()` method to support OMS style injection for all widgets
* Added multiple brand-new standard widgets
* **Slider**: Full-featured slider control with range/step configuration and value change callback
* **Progress**: Progress bar widget with reset and range adjustment methods
* **TextEdit**: Multi-line editable text component with append/clear capabilities
* **Canvas**: Basic drawing canvas supporting dot/line/rect/circle rendering
* **Picture**: Image widget compatible with raster and SVG images
* **Video**: Video playback widget with play/stop/loop/fullscreen control

#### Layout System Completion

* Completed full layout suite functional methods
* `BaseLayout`: Added widget/layout add/delete/clear, lock/unlock management
* `BoxLayout/VerticalLayout/HorizontalLayout`: Added stretch/spacing/margin universal configuration
* `GridLayout`: Perfected row/span layout placement and margin configuration
* `FormLayout`: Added label binding and global spacing/margin settings

#### Dialog \& Tool Module Enhancement

* Completed `dialog` module API documentation and method supplementation
* Perfect `MessageBox`, `FileChooser`, `ColorPicker` full lifecycle methods
* Exposed Qt native `Icon` and `Button` enumerations for dialog customization
* Expanded `utils` module: environment variable reading, clipboard operation, system notification, user directory acquisition
* Enriched `utils.color` global color constant library with light/dark gradient color sets
* Upgraded `terminal.ConsoleIO`: Added hex-to-ANSI conversion, progress bar rendering, rich text input/output

#### Demo \& Example Project Supplement

* Added multiple official demo cases covering core new features
* `full\_demo.py`: Comprehensive demo integrating core, widgets, layout, terminal and OML functions
* `toolbox.py`: Terminal progress task demo based on ConsoleIO
* `terminal\_demo.py`: Independent terminal rich text input/output \& progress bar demo
* `oml\_demo.py`: Independent OML markup conversion and QML loading demo

#### Project Environment Optimization

* Automatically inject project root directory into`sys.path` on module import to optimize internal module import logic
* Added `oml` module to top-level export list, supporting direct `import ohmygui.oml`

### Changed

#### API Standardization \& Return Value Uniformity

* Unified return value of all widget methods to `Self`, supporting chain calls comprehensively
* Standardized method naming and parameter specifications of `Text/Button/InputEntry/PasswordEntry` and other basic widgets
* Upgraded font-related methods to support size/bold/italic multi-parameter configuration
* Optimized property exposure of all widgets, unified `font/fg/bg/value` attribute access rules

#### Documentation Optimization

* Fully updated `docs/api\_reference.md`, completed API documentation of all new modules and widgets
* Refined module function descriptions, optimized parameter and return value annotations
* Adjusted README roadmap sequence, swapped v1.3.0 (3D engine) and v1.4.0 (animation optimization) iteration plans

#### Code Specification Correction

* Fixed spelling error: renamed `horizental.py` to standard `horizontal.py`, updated all reference imports
* Optimized OMS/OML parser error prompts and log output, improved debugging friendliness
* Cleaned redundant code and fixed Pylance unbound variable warning in parser module

### Deprecated

* `Window.top\_widgets` property is officially deprecated, replaced by `toplevel\_widget` (added runtime warning prompt)

### Fixed

* Fixed import file coverage bug in original OMS parser (solved incomplete imported content replacement)
* Fixed missing exception capture for style sheet file loading
* Fixed partial widget method no-return value specification inconsistency
* Fixed spelling error of horizontal layout module name to eliminate import ambiguity
