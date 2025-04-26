"""Tests for the repository module."""

import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import os
import subprocess
from src.ideacli.repository import init_repo, status, IDEAS_REPO

class TestRepository(unittest.TestCase):
    """Test repository functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_args = MagicMock()
        self.mock_args.path = None

    @patch('os.path.exists')
    def test_init_repo_exists_is_git(self, mock_exists):
        """Test init_repo when repo exists and is a git repo."""
        # Setup
        mock_exists.side_effect = [True, True]  # Path exists, .git exists

        # Execute
        result = init_repo(self.mock_args)

        # Assert
        self.assertTrue(result)
        mock_exists.assert_called_with(os.path.join(IDEAS_REPO, ".git"))

    @patch('os.path.exists')
    def test_init_repo_exists_not_git(self, mock_exists):
        """Test init_repo when repo exists but is not a git repo."""
        # Setup
        mock_exists.side_effect = [True, False]  # Path exists, .git doesn't exist

        # Execute
        result = init_repo(self.mock_args)

        # Assert
        self.assertFalse(result)
        mock_exists.assert_called_with(os.path.join(IDEAS_REPO, ".git"))

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_init_repo_new(self, mock_file, mock_run, mock_makedirs, mock_exists):
        """Test init_repo when creating a new repo."""
        # Setup
        mock_exists.side_effect = [False]  # Path doesn't exist

        # Execute
        result = init_repo(self.mock_args)

        # Assert
        self.assertTrue(result)
        mock_makedirs.assert_has_calls([
            call(IDEAS_REPO, exist_ok=True),
            call(os.path.join(IDEAS_REPO, "conversations"), exist_ok=True)
        ], any_order=True)
        mock_run.assert_has_calls([
            call(["git", "init"], cwd=IDEAS_REPO, check=True),
            call(["git", "add", "."], cwd=IDEAS_REPO, check=True),
            call(["git", "commit", "-m", "Initial repository structure"], cwd=IDEAS_REPO, check=True)
        ])
        mock_file.assert_called_once_with(os.path.join(IDEAS_REPO, "README.md"), "w")

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('subprocess.run')
    def test_init_repo_exception(self, mock_run, mock_makedirs, mock_exists):
        """Test init_repo with an exception."""
        # Setup
        mock_exists.return_value = False
        mock_run.side_effect = Exception("Git error")

        # Execute
        result = init_repo(self.mock_args)

        # Assert
        self.assertFalse(result)
        mock_makedirs.assert_called_once_with(IDEAS_REPO, exist_ok=True)

    @patch('os.path.exists')
    def test_status_no_repo(self, mock_exists):
        """Test status when no repo exists."""
        # Setup
        mock_exists.return_value = False

        # Execute
        result = status(self.mock_args)

        # Assert
        self.assertFalse(result)
        mock_exists.assert_called_once_with(os.path.join(IDEAS_REPO, ".git"))

    @patch('os.path.exists')
    @patch('subprocess.check_output')
    @patch('os.listdir')
    @patch('os.path.abspath')
    def test_status_with_repo(self, mock_abspath, mock_listdir, mock_check_output, mock_exists):
        """Test status with a repo."""
        # Setup
        mock_exists.return_value = True
        mock_check_output.return_value = "On branch main\nnothing to commit\n"
        mock_listdir.return_value = ["file1.txt", "file2.txt"]
        mock_abspath.return_value = "/abs/path/.ideas_repo"

        # Execute
        result = status(self.mock_args)

        # Assert
        self.assertTrue(result)
        mock_exists.assert_called_once_with(os.path.join(IDEAS_REPO, ".git"))
        mock_check_output.assert_called_once_with(["git", "status"], cwd=IDEAS_REPO, universal_newlines=True)
        mock_listdir.assert_called_once_with(os.path.join(IDEAS_REPO, "conversations"))

    @patch('os.path.exists')
    @patch('subprocess.check_output')
    def test_status_exception(self, mock_check_output, mock_exists):
        """Test status with an exception."""
        # Setup
        mock_exists.return_value = True
        mock_check_output.side_effect = Exception("Git error")

        # Execute
        result = status(self.mock_args)

        # Assert
        self.assertFalse(result)
        mock_exists.assert_called_once_with(os.path.join(IDEAS_REPO, ".git"))

    @patch('os.path.exists')
    def test_custom_path(self, mock_exists):
        """Test using a custom path."""
        # Setup
        self.mock_args.path = "/custom/path"
        mock_exists.side_effect = [True, True]  # Path exists, .git exists

        # Execute
        result = init_repo(self.mock_args)

        # Assert
        self.assertTrue(result)
        mock_exists.assert_has_calls([
            call("/custom/path"),
            call(os.path.join("/custom/path", ".git"))
        ])

if __name__ == '__main__':
    unittest.main()
