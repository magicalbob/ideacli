"""Tests for the clipboard module."""

import unittest
from unittest.mock import patch, MagicMock
import platform
import subprocess
from src.ideacli.clipboard import copy_to_clipboard, paste_from_clipboard

class TestClipboard(unittest.TestCase):
    """Test clipboard functionality."""

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_darwin(self, mock_popen, mock_system):
        """Test copy_to_clipboard on macOS."""
        # Setup
        mock_system.return_value = "Darwin"
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        # Execute
        result = copy_to_clipboard("test text")
        
        # Assert
        mock_popen.assert_called_once_with('pbcopy', stdin=subprocess.PIPE)
        mock_process.communicate.assert_called_once_with(b"test text")
        self.assertTrue(result)

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_windows(self, mock_popen, mock_system):
        """Test copy_to_clipboard on Windows."""
        # Setup
        mock_system.return_value = "Windows"
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        # Execute
        result = copy_to_clipboard("test text")
        
        # Assert
        mock_popen.assert_called_once_with(['clip'], stdin=subprocess.PIPE)
        mock_process.communicate.assert_called_once_with(b"test text")
        self.assertTrue(result)

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_linux_xclip(self, mock_popen, mock_system):
        """Test copy_to_clipboard on Linux with xclip."""
        # Setup
        mock_system.return_value = "Linux"
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        # Execute
        result = copy_to_clipboard("test text")
        
        # Assert
        mock_popen.assert_called_once_with(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
        mock_process.communicate.assert_called_once_with(b"test text")
        self.assertTrue(result)

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_linux_wl_copy(self, mock_popen, mock_system):
        """Test copy_to_clipboard on Linux with wl-copy."""
        # Setup
        mock_system.return_value = "Linux"
        mock_popen.side_effect = [FileNotFoundError, MagicMock()]
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        # Execute
        result = copy_to_clipboard("test text")
        
        # Assert
        mock_popen.assert_called_with(['wl-copy'], stdin=subprocess.PIPE)
        self.assertTrue(result)

    @patch('platform.system')
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_linux_no_clipboard(self, mock_popen, mock_system):
        """Test copy_to_clipboard on Linux with no clipboard tools."""
        # Setup
        mock_system.return_value = "Linux"
        mock_popen.side_effect = FileNotFoundError
        
        # Execute
        result = copy_to_clipboard("test text")
        
        # Assert
        self.assertFalse(result)

    @patch('platform.system')
    @patch('subprocess.check_output')
    def test_paste_from_clipboard_darwin(self, mock_check_output, mock_system):
        """Test paste_from_clipboard on macOS."""
        # Setup
        mock_system.return_value = "Darwin"
        mock_check_output.return_value = "test clipboard content"
        
        # Execute
        result = paste_from_clipboard()
        
        # Assert
        mock_check_output.assert_called_once_with('pbpaste', universal_newlines=True)
        self.assertEqual(result, "test clipboard content")

    @patch('platform.system')
    @patch('subprocess.check_output')
    def test_paste_from_clipboard_windows(self, mock_check_output, mock_system):
        """Test paste_from_clipboard on Windows."""
        # Setup
        mock_system.return_value = "Windows"
        mock_check_output.return_value = "test clipboard content"
        
        # Execute
        result = paste_from_clipboard()
        
        # Assert
        mock_check_output.assert_called_once_with(['powershell.exe', '-command', 'Get-Clipboard'], universal_newlines=True)
        self.assertEqual(result, "test clipboard content")

    @patch('platform.system')
    @patch('subprocess.check_output')
    def test_paste_from_clipboard_windows_error(self, mock_check_output, mock_system):
        """Test paste_from_clipboard on Windows with error."""
        # Setup
        mock_system.return_value = "Windows"
        mock_check_output.side_effect = Exception("Windows error")
        
        # Execute
        result = paste_from_clipboard()
        
        # Assert
        self.assertEqual(result, "")

    @patch('platform.system')
    @patch('subprocess.check_output')
    def test_paste_from_clipboard_linux_xclip(self, mock_check_output, mock_system):
        """Test paste_from_clipboard on Linux with xclip."""
        # Setup
        mock_system.return_value = "Linux"
        mock_check_output.return_value = "test clipboard content"
        
        # Execute
        result = paste_from_clipboard()
        
        # Assert
        mock_check_output.assert_called_once_with(['xclip', '-selection', 'clipboard', '-o'], universal_newlines=True)
        self.assertEqual(result, "test clipboard content")

    @patch('platform.system')
    @patch('subprocess.check_output')
    def test_paste_from_clipboard_linux_wl_paste(self, mock_check_output, mock_system):
        """Test paste_from_clipboard on Linux with wl-paste."""
        # Setup
        mock_system.return_value = "Linux"
        mock_check_output.side_effect = [FileNotFoundError, "test clipboard content"]
        
        # Execute
        result = paste_from_clipboard()
        
        # Assert
        mock_check_output.assert_called_with(['wl-paste'], universal_newlines=True)
        self.assertEqual(result, "test clipboard content")

    @patch('platform.system')
    @patch('subprocess.check_output')
    def test_paste_from_clipboard_linux_no_clipboard(self, mock_check_output, mock_system):
        """Test paste_from_clipboard on Linux with no clipboard tools."""
        # Setup
        mock_system.return_value = "Linux"
        mock_check_output.side_effect = FileNotFoundError
        
        # Execute
        result = paste_from_clipboard()
        
        # Assert
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
