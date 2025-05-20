# tests/test_clipboard.py

import unittest
from unittest.mock import patch, MagicMock
from ideacli.clipboard import copy_to_clipboard, paste_from_clipboard
import subprocess

class TestClipboard(unittest.TestCase):

    @patch('platform.system', return_value="Darwin")
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_darwin(self, mock_popen, mock_system):
        mock_process = MagicMock()
        mock_popen.return_value.__enter__.return_value = mock_process

        result = copy_to_clipboard("test text")

        mock_popen.assert_called_once_with(['pbcopy'], stdin=subprocess.PIPE)
        mock_process.communicate.assert_called_once_with(input=b"test text")
        self.assertTrue(result)

    @patch('platform.system', return_value="Windows")
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_windows(self, mock_popen, mock_system):
        mock_process = MagicMock()
        mock_popen.return_value.__enter__.return_value = mock_process

        result = copy_to_clipboard("test text")

        mock_popen.assert_called_once_with(['clip'], stdin=subprocess.PIPE)
        mock_process.communicate.assert_called_once_with(input=b"test text")
        self.assertTrue(result)

    @patch('platform.system', return_value="Linux")
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_linux_xclip(self, mock_popen, mock_system):
        mock_process = MagicMock()
        mock_popen.return_value.__enter__.return_value = mock_process

        result = copy_to_clipboard("test text")

        mock_popen.assert_called_once_with(
            ['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE
        )
        mock_process.communicate.assert_called_once_with(input=b"test text")
        self.assertTrue(result)

    @patch('platform.system', return_value="Linux")
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_linux_wlcopy(self, mock_popen, mock_system):
        # Simulate xclip not found first
        mock_process = MagicMock()
        mock_popen.side_effect = [
            FileNotFoundError(),
            MagicMock(__enter__=lambda s: mock_process, __exit__=lambda s, a, b, c: None)
        ]

        result = copy_to_clipboard("test text")

        expected_calls = [
            unittest.mock.call(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE),
            unittest.mock.call(['wl-copy'], stdin=subprocess.PIPE),
        ]
        mock_popen.assert_has_calls(expected_calls)
        mock_process.communicate.assert_called_once_with(input=b"test text")
        self.assertTrue(result)

    @patch('platform.system', return_value="Darwin")
    @patch('subprocess.check_output')
    def test_paste_from_clipboard_darwin(self, mock_check_output, mock_system):
        mock_check_output.return_value = "clipboard text"

        result = paste_from_clipboard()

        mock_check_output.assert_called_once_with(['pbpaste'], universal_newlines=True)
        self.assertEqual(result, "clipboard text")

    @patch('platform.system', return_value="Windows")
    @patch('subprocess.check_output')
    def test_paste_from_clipboard_windows(self, mock_check_output, mock_system):
        mock_check_output.return_value = "clipboard text"

        result = paste_from_clipboard()

        mock_check_output.assert_called_once_with(
            ['powershell.exe', '-command', 'Get-Clipboard'],
            universal_newlines=True
        )
        self.assertEqual(result, "clipboard text")

    @patch('platform.system', return_value="Linux")
    @patch('subprocess.check_output')
    def test_paste_from_clipboard_linux_xclip(self, mock_check_output, mock_system):
        mock_check_output.return_value = "clipboard text"

        result = paste_from_clipboard()

        mock_check_output.assert_called_once_with(
            ['xclip', '-selection', 'clipboard', '-o'], universal_newlines=True
        )
        self.assertEqual(result, "clipboard text")

    @patch('platform.system', return_value="Linux")
    @patch('subprocess.check_output')
    def test_paste_from_clipboard_linux_wlpaste(self, mock_check_output, mock_system):
        # Simulate xclip not found first
        mock_check_output.side_effect = [
            FileNotFoundError(),
            "clipboard text"
        ]

        result = paste_from_clipboard()

        expected_calls = [
            unittest.mock.call(['xclip', '-selection', 'clipboard', '-o'], universal_newlines=True),
            unittest.mock.call(['wl-paste'], universal_newlines=True)
        ]
        mock_check_output.assert_has_calls(expected_calls)
        self.assertEqual(result, "clipboard text")

if __name__ == '__main__':
    unittest.main()
