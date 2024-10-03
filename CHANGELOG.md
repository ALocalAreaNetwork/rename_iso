# Changelog

All notable changes to this project will be documented in this file.

## 2024-10-02 - 0.2.1

### Changed
- `rename_iso` function now returns a string of the file name if the name matches the SFV file name
- `rename_directory` function now returns a string of the file name if the name matches the ISO file name

### Fixed
- `main` will now pass in the `renamed_iso_file` to the `rename_directory` function as it should

### Known Bugs
- CRITICAL: Multiple ISOs in the same directory will cause an issue where ISOs will be overwritten until one ISO remains. Data will be lost if multiple ISOs are in a single directory.

## 2024-10-02 - 0.2.0

### Added
- `main.py` to improve code readability and maintainability for main program and argument handling.
- `test_main.py` to properly unit test the main function of the application.
- `parse_arguments` function for better argument handling.
- Tests for the `parse_arguments` function.
- Improved test coverage of the overall project (100%)

### Fixed
- `main` function now properly handles the argument parsing and main program execution rather than the entry point `__main__()`

## 2024-10-02 - 0.1.1 [YANKED]

### Fixed
- Improved logging setup to handle verbosity and quiet options correctly.

## 2024-10-02 - 0.1.0 [YANKED]

### Added
- Initial release of [`rename_iso`] tool.
- Implemented logging setup with verbosity and quiet options.
- Implemented function to get ISO files and SFV file names within subdirectories of a specified directory.
- Implemented renaming of ISO files and their directories.