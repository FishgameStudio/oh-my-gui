# Contributing to Oh-My-GUI
Thank you for your interest in contributing to **Oh-My-GUI**! All kinds of contributions are welcome, including bug reports, feature requests, code improvements, documentation updates and tests.

Please read this guide before contributing to keep the project consistent and maintainable.

## Code of Conduct
- Be respectful and friendly to all contributors.
- Keep discussions constructive and focused on the project.
- Follow community norms and avoid inappropriate content.

## How to Contribute
### 1. Report Bugs
- Use [Issues](https://github.com/FishgameStudio/oh-my-gui/issues) to submit bug reports.
- Describe the bug clearly: reproduction steps, expected behavior, actual behavior, system & environment information.
- Attach logs, screenshots or minimal demo code if helpful.

### 2. Request Features
- Open an Issue with the `enhancement` label.
- Explain the use case and why this feature is needed.
- If possible, share your design ideas.

### 3. Submit Code Changes (Pull Request)
1. **Fork** this repository to your own account.
2. Clone your forked repo locally:
```bash
git clone https://github.com/FishgameStudio/oh-my-gui.git
cd oh-my-gui
```
3. Create a new branch for your work:
```bash
git checkout -b feature/AmazingFeatures
# or for bug fix
git checkout -b fix/BugFix
```
4. Make your changes, follow the code rules below.
5. Commit your code (follow commit message rules).
6. Push the branch to your fork:
```bash
git push origin YourBeanchName
```
7. Create a **Pull Request** to the main repository.

## Development Setup
### Environment
- Python 3.8+
- PySide6
- Standard Python toolchain

### Install Dependencies
```bash
pip install pyside6
```

## Code Style & Rules
1. Follow **PEP 8** Python style guide.
2. Use type hints for all public classes, methods and functions.
3. Keep code clean and readable; add comments for complex logic.
4. Do not introduce unnecessary external dependencies.
5. Keep backward compatibility as much as possible.


## Pull Request Rules
1. One PR for one feature / one bug fix. Do not mix multiple changes.
2. Ensure all existing code works correctly after your modification.
3. Write simple description for your PR: what you changed and why.
4. Wait for review and fix problems suggested by maintainers.

## Documentation
- Update related docs and comments when you change features or APIs.
- Keep README and examples up-to-date.

## Questions
If you have any questions, feel free to open a discussion or leave comments in Issues.

---
Again, thanks for your support to Oh-My-GUI!