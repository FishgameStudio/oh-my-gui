from setuptools import setup, find_packages

setup(
    name="ohmygui",
    version="0.9.0",
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