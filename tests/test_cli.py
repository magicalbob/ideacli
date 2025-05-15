"""Tests for the CLI module."""

import unittest
from unittest.mock import patch, MagicMock
import sys
import argparse
from ideacli.cli import main

class TestCLI(unittest.TestCase):
    """Test CLI functionality."""

    @patch('argparse.ArgumentParser.parse_args')
    @patch('ideacli.cli.init_repo')
    def test_init_command(self, mock_init_repo, mock_parse_args):
        """Test the init command."""
        # Setup
        mock_args = MagicMock()
        mock_args.command = "init"
        mock_args.path = "/test/path"
        mock_parse_args.return_value = mock_args
        mock_init_repo.return_value = True

        # Execute
        main()

        # Assert
        mock_init_repo.assert_called_once_with(mock_args)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('ideacli.cli.status')
    def test_status_command(self, mock_status, mock_parse_args):
        """Test the status command."""
        # Setup
        mock_args = MagicMock()
        mock_args.command = "status"
        mock_args.path = "/test/path"
        mock_parse_args.return_value = mock_args
        mock_status.return_value = True

        # Execute
        main()

        # Assert
        mock_status.assert_called_once_with(mock_args)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('argparse.ArgumentParser.print_help')
    def test_no_command(self, mock_print_help, mock_parse_args):
        """Test when no command is provided."""
        # Setup
        mock_args = MagicMock()
        mock_args.command = None
        mock_parse_args.return_value = mock_args

        # Execute
        main()

        # Assert
        mock_print_help.assert_called_once()

    @patch('sys.argv', ['ideacli'])
    @patch('argparse.ArgumentParser.print_help')
    def test_no_args(self, mock_print_help):
        """Test when no arguments are provided."""
        # Execute
        main()

        # Assert
        mock_print_help.assert_called_once()


        # This test might exit before print_help is called due to argparse behavior

    @patch('sys.argv', ['ideacli', 'init', '--path', '/custom/path'])
    @patch('ideacli.cli.init_repo')
    def test_init_with_path_arg(self, mock_init_repo):
        """Test init command with path argument."""
        # Setup
        mock_init_repo.return_value = True

        # Execute
        try:
            main()
        except SystemExit:
            pass  # Ignore SystemExit that might be raised by argparse

        # Assert
        args = mock_init_repo.call_args[0][0]
        self.assertEqual(args.path, '/custom/path')

    @patch('sys.argv', ['ideacli', 'status', '--path', '/custom/path'])
    @patch('ideacli.cli.status')
    def test_status_with_path_arg(self, mock_status):
        """Test status command with path argument."""
        # Setup
        mock_status.return_value = True

        # Execute
        try:
            main()
        except SystemExit:
            pass  # Ignore SystemExit that might be raised by argparse

        # Assert
        args = mock_status.call_args[0][0]
        self.assertEqual(args.path, '/custom/path')

    @patch('argparse.ArgumentParser.parse_args')
    @patch('ideacli.cli.add')
    def test_add_command(self, mock_add, mock_parse_args):
        """Test the add command."""
        mock_args = MagicMock()
        mock_args.command = "add"
        mock_parse_args.return_value = mock_args
        mock_add.return_value = None

        main()

        mock_add.assert_called_once_with(mock_args)

if __name__ == '__main__':
    unittest.main()
