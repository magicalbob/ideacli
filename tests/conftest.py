import pytest
import tempfile
import shutil
from unittest.mock import patch

@pytest.fixture(autouse=True)
def isolate_repo_path(monkeypatch):
    """Redirect IDEAS_REPO operations to a temporary folder during all tests."""
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setattr("os.getcwd", lambda: temp_dir)
    yield
    shutil.rmtree(temp_dir)

