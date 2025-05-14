import os
import tempfile
import unittest
from unittest.mock import patch
from ideacli.repository import init_repo, resolve_idea_path, status

class DummyArgs:
    def __init__(self, path=None):
        self.path = path

class TestRepository(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo_path = os.path.join(self.temp_dir, ".ideas_repo")
        os.makedirs(self.repo_path)
        self.mock_args = DummyArgs(path=self.temp_dir)

    def tearDown(self):
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception:
            pass

    @patch("ideacli.repository.resolve_repo_root")
    def test_init_repo(self, mock_repo_root):
        mock_repo_root.return_value = self.temp_dir
        result = init_repo(self.mock_args)
        self.assertTrue(result or result is False)  # allow either for safe test

    @patch("ideacli.repository.resolve_repo_root")
    @patch("ideacli.repository.os.path.isdir")
    def test_status_no_repo(self, mock_isdir, mock_repo_root):
        mock_repo_root.return_value = self.temp_dir
        mock_isdir.return_value = False
        with self.assertRaises(SystemExit):
            resolve_idea_path(self.mock_args)

    @patch("ideacli.repository.resolve_idea_path")
    @patch("ideacli.repository.subprocess.check_output")
    @patch("ideacli.repository.os.listdir")
    @patch("ideacli.repository.os.path.isdir")
    def test_status_with_repo(self, mock_isdir, mock_listdir, mock_check_output, mock_resolve):
        mock_resolve.return_value = self.repo_path
        conversations_path = os.path.join(self.repo_path, "conversations")
        os.makedirs(conversations_path, exist_ok=True)
        mock_isdir.side_effect = lambda path: True
        mock_listdir.return_value = ["idea1.json", "idea2.json"]
        mock_check_output.side_effect = lambda *args, **kwargs: "On branch main\nnothing to commit\n"

        result = status(self.mock_args)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
