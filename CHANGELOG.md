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

