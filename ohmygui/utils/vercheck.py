# Version check.
from requests import get, HTTPError
from logging import info as _info, warning as _warning, error as _error
from typing import Literal, Optional
from subprocess import run, CalledProcessError, PIPE
from packaging.version import Version, InvalidVersion

PKG_NAME = "oh-my-gui"
PYPI_API_URL = f"https://pypi.org/pypi/{PKG_NAME}/json"
REQUEST_TIMEOUT = 10

try:
    from ..__init__ import __version__
except ImportError:
    __version__ = "0.0.0"

_info(f"module {__name__} loaded")

def get_latest_ver(pkg: str = PKG_NAME) -> Optional[str]:
    """Get the latest version of a package from PyPI"""
    url = f"https://pypi.org/pypi/{pkg}/json"
    try:
        resp = get(url, timeout=REQUEST_TIMEOUT)
        _info(f"PyPI server response status code: {resp.status_code}")
        resp.raise_for_status()
        data = resp.json()
        return data["info"]["version"]
    except HTTPError as e:
        _warning(f"Failed to fetch version from {url}, error: {e}")
    except Exception as e:
        _warning(f"Network unknown error fetching version: {e}")
    return None

def get_local_version() -> str:
    """Return current local library version"""
    return __version__

def compare_ver(v1: str, v2: str) -> Literal[-1, 0, 1]:
    """
    Compare two semantic versions
    return -1: v1 < v2
    return 0:  v1 == v2
    return 1:  v1 > v2
    """
    try:
        ver1 = Version(v1)
        ver2 = Version(v2)
    except InvalidVersion as e:
        _warning(f"Invalid version string: {v1} | {v2}, error: {e}")
        return 0
    if ver1 < ver2:
        return -1
    elif ver1 == ver2:
        return 0
    else:
        return 1

def is_latest_version() -> bool:
    """Check whether local version is equal or newer than PyPI latest"""
    remote_ver = get_latest_ver()
    local_ver = get_local_version()

    if remote_ver is None:
        _warning("Failed to get remote version, skip update check")
        return True

    cmp_res = compare_ver(local_ver, remote_ver)
    return cmp_res != -1

def _get_python_exec() -> str:
    """Cross-platform get available python executable"""
    candidates = ["py", "python3", "python"]
    for exe in candidates:
        try:
            run([exe, "-c", "pass"], stdout=PIPE, stderr=PIPE, check=True)
            return exe
        except (FileNotFoundError, CalledProcessError):
            continue
    raise RuntimeError("No valid Python executable found for upgrade")

def upgrade_ohmygui() -> bool:
    """Upgrade oh-my-gui to the newest release on PyPI"""
    _info("Start upgrading oh-my-gui...")
    remote_ver = get_latest_ver()
    if remote_ver is None:
        _error("Abort upgrade: cannot fetch latest version number")
        return False

    try:
        py_exe = _get_python_exec()
        cmd = [
            py_exe, "-m", "pip", "install", "--upgrade", f"{PKG_NAME}=={remote_ver}"
        ]
        run(
            cmd,
            encoding="utf-8",
            check=True,
            stdout=PIPE,
            stderr=PIPE
        )
    except CalledProcessError as e:
        _error(f"Upgrade failed, subprocess return code: {e.returncode}, error: {e}")
        return False
    except RuntimeError as e:
        _error(f"Cannot find python executable to run pip: {e}")
        return False
    _info(f"Successfully upgraded {PKG_NAME} to version {remote_ver}")
    return True