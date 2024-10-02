import os
import unittest
import shutil
import argparse
from unittest.mock import patch, MagicMock
from rename_iso.main import parse_arguments, main


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = '/tmp/test_rename_iso'
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        

class TestParseArguments(BaseTest):

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(directory='/path/to/dir', verbosity=True, quiet=False))
    def test_parse_arguments(self, mock_parse_args):
        args = parse_arguments()
        self.assertEqual(args.directory, '/path/to/dir')
        self.assertTrue(args.verbosity)
        self.assertFalse(args.quiet)


class TestMainFunction(BaseTest):

    @patch('rename_iso.main.get_iso_files')
    @patch('rename_iso.main.rename_iso')
    @patch('rename_iso.main.rename_directory')
    @patch('rename_iso.main.setup_logging')
    @patch('rename_iso.main.parse_arguments', 
           return_value=argparse.Namespace(
               directory='/path/to/dir', 
               verbosity=False, 
               quiet=False))
    def test_main_function(self, mock_parse_arguments, 
                           mock_setup_logging, mock_rename_directory, 
                           mock_rename_iso, mock_get_iso_files):
        mock_get_iso_files.return_value = [
            os.path.join(self.test_dir, 'test.iso')
        ]
        mock_rename_iso.return_value = True

        main()

        mock_parse_arguments.assert_called_once()
        mock_setup_logging.assert_called_once_with(False, False)
        mock_get_iso_files.assert_called_once_with('/path/to/dir')
        mock_rename_iso.assert_called_once_with(
            os.path.join(self.test_dir, 'test.iso')
        )
        mock_rename_directory.assert_called_once_with(
            os.path.join(self.test_dir, 'test.iso')
        )


if __name__ == '__main__':
    unittest.main()  # pragma: no cover