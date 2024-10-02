import os
import shutil
import unittest
import logging
from unittest.mock import patch, MagicMock
from rename_iso.rename_iso import setup_logging, get_iso_files, get_sfv_file_name, rename_iso, rename_directory, main

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = '/tmp/test_rename_iso'
        self.game_dir_0 = os.path.join(self.test_dir, 'game_0')
        self.game_dir_1 = os.path.join(self.test_dir, 'game_1')
        self.game_dir_2 = os.path.join(self.test_dir, 'game_2')
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_file(self, path, content=''):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

class TestSetupLogging(BaseTest):

    def test_verbosity_and_quiet(self):
        with self.assertRaises(ValueError):
            setup_logging(verbosity=True, quiet=True)

    @patch('logging.basicConfig')
    def test_verbosity(self, mock_basicConfig):
        setup_logging(verbosity=True, quiet=False)
        mock_basicConfig.assert_called_once_with(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    @patch('logging.basicConfig')
    def test_quiet(self, mock_basicConfig):
        setup_logging(verbosity=False, quiet=True)
        mock_basicConfig.assert_called_once_with(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

    @patch('logging.basicConfig')
    def test_neither_verbosity_nor_quiet(self, mock_basicConfig):
        setup_logging(verbosity=False, quiet=False)
        mock_basicConfig.assert_called_once_with(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestGetIsoFiles(BaseTest):

    def test_get_iso_files_single(self):
        iso_path = os.path.join(self.game_dir_0, 'test0.iso')
        self.create_file(iso_path)
        iso_files = get_iso_files(self.test_dir)
        self.assertIn(iso_path, iso_files)

    def test_get_iso_files_multiple(self):
        iso_path_1 = os.path.join(self.game_dir_0, 'test0.iso')
        iso_path_2 = os.path.join(self.game_dir_1, 'test1.iso')
        self.create_file(iso_path_1)
        self.create_file(iso_path_2)
        iso_files = get_iso_files(self.test_dir)
        self.assertIn(iso_path_1, iso_files)
        self.assertIn(iso_path_2, iso_files)

    def test_get_iso_files_empty(self):
        iso_files = get_iso_files(self.test_dir)
        self.assertEqual(iso_files, [])

class TestGetSfvFileName(BaseTest):

    def test_get_sfv_file_name_no_sfv(self):
        sfv_file_name = get_sfv_file_name(self.test_dir)
        self.assertIsNone(sfv_file_name)

    def test_get_sfv_file_name_single_sfv(self):
        sfv_path = os.path.join(self.test_dir, 'test.sfv')
        self.create_file(sfv_path)
        sfv_file_name = get_sfv_file_name(self.test_dir)
        self.assertEqual(sfv_file_name, 'test')

    def test_get_sfv_file_name_multiple_sfv(self):
        sfv_path_1 = os.path.join(self.test_dir, 'test1.sfv')
        sfv_path_2 = os.path.join(self.test_dir, 'test2.sfv')
        self.create_file(sfv_path_1)
        self.create_file(sfv_path_2)
        sfv_file_name = get_sfv_file_name(self.test_dir)
        self.assertIsNone(sfv_file_name)

class TestRenameIso(BaseTest):

    def test_rename_iso_no_sfv(self):
        iso_path = os.path.join(self.test_dir, 'test.iso')
        self.create_file(iso_path)
        result = rename_iso(iso_path)
        self.assertFalse(result)
        self.assertTrue(os.path.exists(iso_path))

    def test_rename_iso_with_sfv(self):
        iso_path = os.path.join(self.test_dir, 'test.iso')
        sfv_path = os.path.join(self.test_dir, 'new_name.sfv')
        self.create_file(iso_path)
        self.create_file(sfv_path)
        result = rename_iso(iso_path)
        new_iso_path = os.path.join(self.test_dir, 'new_name.iso')
        self.assertTrue(result)
        self.assertTrue(os.path.exists(new_iso_path))
        self.assertFalse(os.path.exists(iso_path))

class TestRenameDirectory(BaseTest):

    def test_rename_directory_single_iso(self):
        iso_path = os.path.join(self.game_dir_0, 'test.iso')
        sfv_path = os.path.join(self.game_dir_0, 'test.sfv')
        self.create_file(iso_path)
        self.create_file(sfv_path)
        rename_iso(iso_path)  # Ensure the ISO file is renamed first
        result = rename_directory(os.path.join(self.game_dir_0, 'test.iso'))
        new_directory = os.path.join(self.test_dir, 'test')
        self.assertTrue(result)
        self.assertTrue(os.path.exists(new_directory))
        self.assertFalse(os.path.exists(self.game_dir_0))

    def test_rename_directory_multiple_iso(self):
        iso_path_1 = os.path.join(self.game_dir_0, 'test1.iso')
        iso_path_2 = os.path.join(self.game_dir_0, 'test2.iso')
        self.create_file(iso_path_1)
        self.create_file(iso_path_2)
        result = rename_directory(iso_path_1)
        self.assertFalse(result)
        self.assertTrue(os.path.exists(self.game_dir_0))

    @patch('logging.info')
    def test_rename_directory_already_correct_name(self, mock_logging_info):
        iso_path = os.path.join(self.test_dir, 'game_0', 'game_0.iso')
        os.makedirs(os.path.dirname(iso_path), exist_ok=True)
        self.create_file(iso_path)
        result = rename_directory(iso_path)
        self.assertFalse(result)
        mock_logging_info.assert_called_once_with(f"Directory {os.path.dirname(iso_path)} already has the correct name.")

class TestMainFunction(BaseTest):

    @patch('rename_iso.rename_iso.get_iso_files')
    @patch('rename_iso.rename_iso.rename_iso')
    @patch('rename_iso.rename_iso.rename_directory')
    def test_main_function(self, mock_rename_directory, mock_rename_iso, mock_get_iso_files):
        mock_get_iso_files.return_value = [os.path.join(self.test_dir, 'test.iso')]
        mock_rename_iso.return_value = True

        main(self.test_dir)

        mock_get_iso_files.assert_called_once_with(self.test_dir)
        mock_rename_iso.assert_called_once_with(os.path.join(self.test_dir, 'test.iso'))
        mock_rename_directory.assert_called_once_with(os.path.join(self.test_dir, 'test.iso'))

if __name__ == '__main__':
    unittest.main()  # pragma: no cover