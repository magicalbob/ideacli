import unittest
from unittest import mock
from unittest.mock import patch
import sys
import io
import os
import tempfile
import shutil

from ideacli.add import add
from ideacli.repository import IDEAS_REPO

class TestAdd(unittest.TestCase):
    def setUp(self):
        # create isolated temp directory for test repo
        self.test_dir = tempfile.mkdtemp()
        self.repo_path = os.path.join(self.test_dir, IDEAS_REPO)
        os.makedirs(os.path.join(self.repo_path, "conversations"), exist_ok=True)
        self.args = mock.MagicMock()
        self.args.path = self.test_dir

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("ideacli.repository.resolve_repo_root")
    @patch("ideacli.add.copy_to_clipboard")
    @patch("ideacli.add.subprocess.run")
    def test_add_piped_input(self, mock_subprocess, mock_clipboard, mock_repo_root):
        """Test adding via piped stdin"""
        mock_repo_root.return_value = self.test_dir

        test_input = "Test Subject\nThis is the body\nMultiple lines\n"
        sys.stdin = io.StringIO(test_input)
        sys.stdin.isatty = lambda: False

        add(self.args)

        mock_clipboard.assert_called_once()
        mock_subprocess.assert_called()

    @patch("ideacli.repository.resolve_repo_root")
    @patch("ideacli.add.copy_to_clipboard")
    @patch("ideacli.add.subprocess.run")
    @patch("ideacli.add.input", side_effect=["Test Subject"])
    def test_add_interactive_input(self, mock_input, mock_subprocess, mock_clipboard, mock_repo_root):
        """Test adding via interactive user input"""
        mock_repo_root.return_value = self.test_dir

        sys.stdin = io.StringIO("Body content\nMore lines\n")
        sys.stdin.isatty = lambda: True

        add(self.args)

        mock_clipboard.assert_called_once()
        mock_subprocess.assert_called()
