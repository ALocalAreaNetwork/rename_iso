# Rename ISO

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A tool to rename ISO files and their directories based on SFV files.

## Features

- Rename ISO files to match the corresponding SFV file name in the same directory.
- Rename directories containing ISO files to match the ISO file name.
- Configurable logging levels for verbosity and quiet modes.

## Installation

You can install the package using `pip`:

```sh
pip install .
```

## Usage

To use the `rename_iso` tool, run the following command:

```sh
rename_iso <directory> [options]
```

### Options

- `-v`, `--verbosity`: Increase output verbosity to DEBUG level.
- `-q`, `--quiet`: Decrease output verbosity to WARNING level.

### Example

```sh
rename_iso /path/to/directory -v
```

## Functions

### `setup_logging(verbosity: bool, quiet: bool)`

Set up logging configuration based on verbosity and quiet flags.

### `get_iso_files(directory: str) -> List[str]`

Get a list of all ISO files in the given directory and its subdirectories.

### `get_sfv_file_name(directory: str) -> Optional[str]`

Get the base name of the SFV file in the given directory.

### `rename_iso(iso_file: str) -> bool`

Rename the ISO file to match the SFV file name in the same directory.

### `rename_directory(iso_file: str) -> bool`

Rename the directory containing the ISO file to match the ISO file name.

### `main(directory: str, verbosity: bool, quiet: bool)`

Main function to rename ISO files and their directories based on SFV files.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or suggestions, feel free to contact [ALocalAreaNetwork](mailto:alocalareanet@proton.me).