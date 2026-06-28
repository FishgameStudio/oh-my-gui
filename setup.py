from setuptools import setup, find_packages

setup(
    name="ohmygui",
    version="1.2.4",
    author="FishgameStudio",
    description="A lightweight GUI library wrapping PySide6 for Python",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FishgameStudio/oh-my-gui",
    packages=find_packages(),
    install_requires=[
        "PySide6>=6.0"
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: User Interfaces",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    include_package_data=True,
    zip_safe=False
)

print("Setup finished, configuring PYTHONPATH...")
import os
import sys
import platform

def add_pythonpath_permanently(new_path):
    new_path = os.path.abspath(new_path)
    sep = ";" if platform.system() == "Windows" else ":"

    current = os.environ.get("PYTHONPATH", "")
    path_list = current.split(sep) if current else []

    if new_path in path_list:
        print(f"Path {new_path} already in PYTHONPATH, skip")
        return

    path_list.append(new_path)
    new_value = sep.join(path_list)

    if platform.system() == "Windows":
        import winreg
        reg_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_WRITE
        )
        winreg.SetValueEx(reg_key, "PYTHONPATH", 0, winreg.REG_EXPAND_SZ, new_value)
        winreg.CloseKey(reg_key)
        print("Has been written to Windows user environment variable, restart the terminal to take the effect")

    else:
        shell_rc = None
        if "zsh" in os.environ.get("SHELL", ""):
            shell_rc = os.path.expanduser("~/.zshrc")
        else:
            shell_rc = os.path.expanduser("~/.bashrc")

        line = f'export PYTHONPATH="{new_value}"'
        with open(shell_rc, "a", encoding="utf-8") as f:
            f.write("\n" + line + "\n")
        print(f"Has been written to {shell_rc}, execute `source {os.path.basename(shell_rc)}` to take effect")
