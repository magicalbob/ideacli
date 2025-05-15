import os
import json
import tempfile
import unittest
from ideacli.rename import rename_idea

class DummyArgs:
    def __init__(self, path, id, target):
        self.path = path
        self.id = id
        self.target = target

class TestRename(unittest.TestCase):
    def setUp(self):
        # create temp repo structure
        self.temp_dir = tempfile.mkdtemp()
        self.repo_dir = os.path.join(self.temp_dir, ".ideas_repo")
        os.makedirs(os.path.join(self.repo_dir, "conversations"), exist_ok=True)

        # create dummy idea file
        self.idea_id = "testid"
        self.idea_file = os.path.join(self.repo_dir, "conversations", f"{self.idea_id}.json")
        with open(self.idea_file, "w", encoding="utf-8") as f:
            json.dump({"id": self.idea_id, "subject": "Old Title", "body": "Some body text"}, f)

    def tearDown(self):
        # clean up temp dir
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.temp_dir)

    def test_rename_idea(self):
        args = DummyArgs(self.temp_dir, self.idea_id, "New Renamed Title")
        rename_idea(args)

        with open(self.idea_file, "r", encoding="utf-8") as f:
            idea = json.load(f)
        
        self.assertEqual(idea["subject"], "New Renamed Title")
        self.assertEqual(idea["id"], self.idea_id)
        self.assertEqual(idea["body"], "Some body text")

if __name__ == "__main__":
    unittest.main()
