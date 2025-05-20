"""CLI tool for managing LLM conversation ideas."""

# Use relative import
from .cli import main

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # For Python <3.8, but you can skip this if you only support 3.8+
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("ideacli")
except PackageNotFoundError:
    __version__ = "unknown"
