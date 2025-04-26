import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import io
import os
import json
from src.ideacli.add import add
from src.ideacli.repository import IDEAS_REPO

class TestAdd(unittest.TestCase):

    def setUp(self):
        self.args = MagicMock()
        self.args.path = None  # Needed because ensure_repo uses this

    @patch('src.ideacli.add.copy_to_clipboard')
    @patch('src.ideacli.add.subprocess.run')
    @patch('src.ideacli.add.open', new_callable=mock_open)
    @patch('src.ideacli.add.os.makedirs')
    @patch('src.ideacli.add.ensure_repo')
    def test_add_piped_input(self, mock_ensure_repo, mock_makedirs, mock_open_file, mock_subprocess, mock_clipboard):
        """Test adding via piped input."""
        # Setup
        test_input = "Test Subject\nThis is the body\nMultiple lines\n"
        sys.stdin = io.StringIO(test_input)

        # Execute
        add(self.args)

        # Assert
        mock_ensure_repo.assert_called_once()
        mock_makedirs.assert_called()
        mock_open_file.assert_called()
        mock_subprocess.assert_called()
        mock_clipboard.assert_called()

    @patch('src.ideacli.add.input', side_effect=["Test Subject"])
    @patch('src.ideacli.add.copy_to_clipboard')
    @patch('src.ideacli.add.subprocess.run')
    @patch('src.ideacli.add.open', new_callable=mock_open)
    @patch('src.ideacli.add.os.makedirs')
    @patch('src.ideacli.add.ensure_repo')
    def test_add_interactive_input(self, mock_ensure_repo, mock_makedirs, mock_open_file, mock_subprocess, mock_clipboard, mock_input):
        """Test adding via interactive input."""
        # Setup
        sys.stdin = io.StringIO("This is the body\nAnother line\n")
        sys.stdin.isatty = lambda: True

        # Execute
        add(self.args)

        # Assert
        mock_ensure_repo.assert_called_once()
        mock_makedirs.assert_called()
        mock_open_file.assert_called()
        mock_subprocess.assert_called()
        mock_clipboard.assert_called()

    def tearDown(self):
        sys.stdin = sys.__stdin__  # Restore stdin after test
