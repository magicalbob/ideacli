import unittest
from unittest.mock import patch, MagicMock
import os
from src.ideacli.repository import status, IDEAS_REPO


class TestRepository(unittest.TestCase):

    def setUp(self):
        self.mock_args = MagicMock()
        self.mock_args.path = None

    @patch('os.path.exists')
    def test_status_no_repo(self, mock_exists):
        """Test status when no repo exists."""
        mock_exists.side_effect = [False, False]

        result = status(self.mock_args)
        self.assertFalse(result)

        expected_path = os.path.join(os.path.abspath(IDEAS_REPO), ".git")
        mock_exists.assert_any_call(expected_path)

    @patch('os.path.isdir')
    @patch('subprocess.check_output')
    @patch('os.listdir')
    @patch('os.path.exists')
    @patch('os.path.abspath')
    def test_status_with_repo(self, mock_abspath, mock_exists, mock_listdir, mock_check_output, mock_isdir):
        """Test status when repo exists and git status works."""
        mock_abspath.return_value = os.path.abspath(IDEAS_REPO)
        mock_exists.side_effect = [True, True]
        mock_listdir.return_value = ["file1.json", "file2.json"]
        mock_check_output.return_value = "On branch main\nnothing to commit\n"
        mock_isdir.return_value = True

        result = status(self.mock_args)
        self.assertTrue(result)

        expected_path = os.path.join(os.path.abspath(IDEAS_REPO), ".git")
        mock_exists.assert_any_call(expected_path)

    @patch('os.path.exists')
    @patch('subprocess.check_output')
    def test_status_exception(self, mock_check_output, mock_exists):
        """Test status when git command fails."""
        mock_exists.side_effect = [True, True]
        mock_check_output.side_effect = Exception("Git error")

        result = status(self.mock_args)
        self.assertFalse(result)

        expected_path = os.path.join(os.path.abspath(IDEAS_REPO), ".git")
        mock_exists.assert_any_call(expected_path)
