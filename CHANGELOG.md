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

# Changelog of [v1.2.1]

### Added
#### Core Runtime & Logging
- Added ANSI colored logging formatter; log levels (DEBUG/INFO/WARNING/ERROR) automatically render blue/green/yellow/red text in terminal
- Added strict parsing error limit mechanism (`ERROR_LIMIT = 15`) for both OMS and OML parsers
- Introduced `ErrorLimitExceededError` custom exception; parsing terminates immediately once error count exceeds threshold to avoid cascading failures
- Added `bind()` decorator callback logging, prints function registration information during event binding

#### OML Parser Upgrade
- Implemented block-internal template macro call parsing, supporting `TemplateName(arg1, arg2)` directly inside component braces
- Enhanced value parser to automatically splice numeric values + unit suffix (`20em` becomes a complete literal instead of two separate tokens)
- Added automatic trailing semicolon swallowing for component statements to eliminate syntax conflicts
- Added `all` alias mapped to wildcard selector `*`, consistent with OMS syntax

#### QML Loading Engine
- Added new `load_qml_string()` method inside `Application`
- Implemented asynchronous `QQmlComponent` compilation with `statusChanged` signal callback
- Captured and printed QML compile errors explicitly; fixed the "Component is not ready" asynchronous loading problem
- Added runtime log tracking for QML source loading snippet

#### Widget API
- Added `focus()` / `defocus()` chainable methods on `BaseWidget` to control keyboard focus programmatically

#### Module Export Standardization
- All submodules switched to automatic `__all__` generation via module inspection
- Only expose public members; all private underscore-prefixed variables are hidden from external imports
- Rewrote manual import lists for `core`, `widget`, `layout`, `dialog`, `terminal`, `oml`, `utils` modules
- Exposed concrete classes directly instead of submodule names in package exports

### Changed
#### Syntax Lexer Breaking Adjustment
- Changed comment syntax from `#` to `//` in both OMS and OML lexers
- Resolved character conflict between hex color literal `#RRGGBB` and line comment symbol
- Lexer now skips all content after `//` until line break

#### OMS & OML Parser Refactoring
- Unified log text by removing redundant `OMS / OML` prefix inside parser messages
- Refactored import preprocessing logic and error handling for `@import` file reading
- Rewrote cursor helper functions with unified error counting via global `ERRORS` counter
- Simplified AST traversal code; cleaned up redundant version upgrade annotations
- Updated header comment of generated QSS/QML files

#### Core Module Refactoring
- Rewrote `core/__init__.py`: export concrete classes (`Window`, `App`, `bind`) instead of submodules
- Changed `App` from simple alias to formal `TypeAlias = Application` type declaration
- Refactored auto-upgrade logic: switched internal logger from `utils.info/warning` to direct logging module functions to eliminate circular import risk
- Cleaned up redundant `from *` wildcard imports across the entire project

#### Documentation & Installation
- Updated README installation command from `pip install .` to public PyPI package `pip install oh-my-gui`
- Added module running instruction: recommend `python -m module.name` instead of direct script execution
- Removed local git clone instruction from quick start section

#### Project Structure
- Deleted obsolete `example/full_demo.py` source file; demo code will be reorganized into standalone samples later
- Bumped package version in `pyproject.toml` and `setup.py` to `1.2.1`
- Version constant `__version__` inside `ohmygui/__init__.py` synchronized to `1.2.1`

### Fixed
1. OML issue: template calls cannot be parsed when placed inside `Window {}` child nodes
2. OMS & OML lexer: numeric values and unit suffixes were split into two independent tokens
3. QML loading: synchronous `create()` invoked before component asynchronous compilation finished, causing "Component not ready" warning and silent failure
4. Parser: unclosed string, unknown character and file import failures did not accumulate error counters properly
5. Module export: inconsistent `__all__` lists leading to inconsistent public API between different subpackages
6. Exit risk: closing `sys.stderr` in error scenarios was avoided by strictly using logging stream handler bound to stdout
7. Minor bugs: missing brace error capture, leftover stray semicolons breaking component parsing

### Deprecated
- No API deprecation in this patch version; all 1.2.0 public interfaces remain fully backward compatible
