#!/usr/bin/env python3

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the main function
from src.ideacli.cli import main

if __name__ == "__main__":
    main()
