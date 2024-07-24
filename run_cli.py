import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from cli.cli import main

if __name__ == "__main__":
    """
    Entry point for the Control System Simulation and Analysis CLI.

    This script sets up the necessary environment by adding the project root directory
    to the system path, allowing for the correct resolution of imports. It then calls
    the main function from cli.cli to handle the command-line interface operations.
    """
    main()
