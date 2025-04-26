"""Clipboard handling functionality for botcli."""

import platform
import subprocess

def copy_to_clipboard(text):
    """Copy text to clipboard based on platform"""
    if platform.system() == "Darwin":  # macOS
        process = subprocess.Popen('pbcopy', stdin=subprocess.PIPE)
        process.communicate(text.encode())
    elif platform.system() == "Windows":
        process = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
        process.communicate(text.encode())
    elif platform.system() == "Linux":
        try:
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            process.communicate(text.encode())
        except FileNotFoundError:
            try:
                process = subprocess.Popen(['wl-copy'], stdin=subprocess.PIPE)
                process.communicate(text.encode())
            except FileNotFoundError:
                print("Error: No clipboard command found. Install xclip or wl-copy.")
                return False
    print("Copied to clipboard!")
    return True

def paste_from_clipboard():
    """Get text from clipboard based on platform"""
    if platform.system() == "Darwin":  # macOS
        return subprocess.check_output('pbpaste', universal_newlines=True)
    elif platform.system() == "Windows":
        try:
            return subprocess.check_output(['powershell.exe', '-command', 'Get-Clipboard'], universal_newlines=True)
        except:
            print("Error getting clipboard contents on Windows")
            return ""
    elif platform.system() == "Linux":
        try:
            return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o'], universal_newlines=True)
        except FileNotFoundError:
            try:
                return subprocess.check_output(['wl-paste'], universal_newlines=True)
            except FileNotFoundError:
                print("Error: No clipboard command found. Install xclip or wl-copy.")
                return ""
