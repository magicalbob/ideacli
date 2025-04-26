import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import os
import json
from src.ideacli.add import add
from src.ideacli.repository import IDEAS_REPO

class TestAdd(unittest.TestCase):

    def setUp(self):
        self.args = MagicMock()
        self.args.path = None  # Needed for ensure_repo
        # Make sure test doesn't clash
        os.makedirs(os.path.join(IDEAS_REPO, "conversations"), exist_ok=True)

    @patch('src.ideacli.add.copy_to_clipboard')
    @patch('src.ideacli.add.subprocess.run')
    def test_add_piped_input(self, mock_subprocess, mock_clipboard):
        """Test adding via piped input."""
        # Setup
        test_input = "Test Subject\nThis is the body\nMultiple lines\n"
        sys.stdin = io.StringIO(test_input)
        sys.stdin.isatty = lambda: False

        # Execute
        add(self.args)

        # Check that file was created
        files = os.listdir(os.path.join(IDEAS_REPO, "conversations"))
        self.assertTrue(any(f.endswith(".json") for f in files))

    @patch('src.ideacli.add.copy_to_clipboard')
    @patch('src.ideacli.add.subprocess.run')
    @patch('src.ideacli.add.input', side_effect=["Test Subject"])
    def test_add_interactive_input(self, mock_input, mock_subprocess, mock_clipboard):
        """Test adding via interactive input."""
        # Setup
        sys.stdin = io.StringIO("Body content\nMore lines\n")
        sys.stdin.isatty = lambda: True

        # Execute
        add(self.args)

        # Check that file was created
        files = os.listdir(os.path.join(IDEAS_REPO, "conversations"))
        self.assertTrue(any(f.endswith(".json") for f in files))

    def tearDown(self):
        sys.stdin = sys.__stdin__
        # Clean up files created
        conversation_dir = os.path.join(IDEAS_REPO, "conversations")
        if os.path.exists(conversation_dir):
            for f in os.listdir(conversation_dir):
                os.remove(os.path.join(conversation_dir, f))
