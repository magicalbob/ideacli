"""Clipboard handling functionality for ideacli."""

import platform
import subprocess


def copy_to_clipboard(text):
    """Copy text to clipboard based on platform."""
    system = platform.system()

    if system == "Darwin":
        return _copy_mac(text)
    if system == "Windows":
        return _copy_windows(text)
    if system == "Linux":
        return _copy_linux(text)

    print(f"Unsupported platform: {system}")
    return False


def _copy_mac(text):
    try:
        with subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE) as process:
            process.communicate(input=text.encode())
        print("Copied to clipboard!")
        return True
    except OSError as err:
        print(f"Error copying to clipboard (macOS): {err}")
        return False


def _copy_windows(text):
    try:
        with subprocess.Popen(['clip'], stdin=subprocess.PIPE) as process:
            process.communicate(input=text.encode())
        print("Copied to clipboard!")
        return True
    except OSError as err:
        print(f"Error copying to clipboard (Windows): {err}")
        return False


def _copy_linux(text):
    try:
        with subprocess.Popen(['xclip', '-selection', 'clipboard'],
                              stdin=subprocess.PIPE) as process:
            process.communicate(input=text.encode())
        print("Copied to clipboard!")
        return True
    except FileNotFoundError:
        return _copy_linux_wlcopy(text)
    except OSError as err:
        print(f"Error copying to clipboard (Linux): {err}")
        return False


def _copy_linux_wlcopy(text):
    try:
        with subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE) as process:
            process.communicate(input=text.encode())
        print("Copied to clipboard!")
        return True
    except FileNotFoundError:
        print("Error: No clipboard command found. Install xclip or wl-copy.")
        return False
    except OSError as err:
        print(f"Error copying to clipboard (Linux wl-copy): {err}")
        return False


def paste_from_clipboard():
    """Get text from clipboard based on platform."""
    system = platform.system()

    if system == "Darwin":
        return _paste_mac()
    if system == "Windows":
        return _paste_windows()
    if system == "Linux":
        return _paste_linux()

    print(f"Unsupported platform: {system}")
    return ""


def _paste_mac():
    try:
        return subprocess.check_output(['pbpaste'], universal_newlines=True)
    except Exception as err:  # pylint: disable=broad-except
        print(f"Error pasting from clipboard (macOS): {err}")
        return ""


def _paste_windows():
    try:
        return subprocess.check_output(
            ['powershell.exe', '-command', 'Get-Clipboard'],
            universal_newlines=True
        )
    except Exception as err:  # pylint: disable=broad-except
        print(f"Error getting clipboard contents on Windows: {err}")
        return ""


def _paste_linux():
    try:
        return subprocess.check_output(
            ['xclip', '-selection', 'clipboard', '-o'],
            universal_newlines=True
        )
    except FileNotFoundError:
        return _paste_linux_wlpaste()
    except Exception as err:  # pylint: disable=broad-except
        print(f"Error pasting from clipboard (Linux): {err}")
        return ""


def _paste_linux_wlpaste():
    try:
        return subprocess.check_output(['wl-paste'], universal_newlines=True)
    except FileNotFoundError:
        print("Error: No clipboard command found. Install xclip or wl-copy.")
        return ""
    except Exception as err:  # pylint: disable=broad-except
        print(f"Error pasting from clipboard (Linux wl-paste): {err}")
        return ""
