import os
import logging
from typing import List, Optional

def setup_logging(verbosity: bool, quiet: bool):
    """
    Set up logging configuration based on verbosity and quiet flags.

    Args:
        verbosity (bool): If True, set logging level to DEBUG.
        quiet (bool): If True, set logging level to WARNING.

    Raises:
        ValueError: If both verbosity and quiet are True.
    """
    if verbosity and quiet:
        raise ValueError(
            "Cannot use both verbosity and quiet options together."
        )
    elif verbosity:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    elif quiet:
        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')


def get_iso_files(directory: str) -> List[str]:
    """
    Get a list of all ISO files in the given directory and its subdirectories.

    Args:
        directory (str): The directory to search for ISO files.

    Returns:
        List[str]: A list of paths to ISO files.
    """
    iso_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.iso'):
                iso_files.append(os.path.join(root, file))
    return iso_files


def get_sfv_file_name(directory: str) -> Optional[str]:
    """
    Get the base name of the SFV file in the given directory.

    Args:
        directory (str): The directory to search for an SFV file.

    Returns:
        Optional[str]: The base name of the SFV file, or None if no valid SFV file is found.
    """
    sfv_files = [file for file 
                 in os.listdir(directory) 
                 if file.endswith('.sfv')]

    if len(sfv_files) == 0:
        logging.warning(f"No .sfv files found in directory: {directory}")
        return None
    elif len(sfv_files) > 1:
        logging.warning(f"Multiple .sfv files found in directory: {directory}")
        return None

    return os.path.splitext(os.path.basename(sfv_files[0]))[0]


def rename_iso(iso_file: str) -> bool:
    """
    Rename the ISO file to match the SFV file name in the same directory.

    Args:
        iso_file (str): The path to the ISO file to rename.

    Returns:
        bool: True if the ISO file was renamed, False otherwise.
    """
    iso_directory = os.path.dirname(iso_file)
    iso_file_name = os.path.splitext(os.path.basename(iso_file))[0]
    sfv_file_name = get_sfv_file_name(iso_directory)

    if not sfv_file_name:
        logging.warning(
            f"Skipping ISO file {iso_file} because no .sfv file found."
        )
        return False

    if iso_file_name == sfv_file_name:
        logging.info(
            f"ISO file {iso_file} already has the correct name."
        )
        return False

    new_iso_file = os.path.join(iso_directory, sfv_file_name + '.iso')
    os.rename(iso_file, new_iso_file)
    logging.info(
        f"Renamed ISO file from {iso_file} to {new_iso_file}"
    )

    return True


def rename_directory(iso_file: str) -> bool:
    """
    Rename the directory containing the ISO file to match the ISO file name.

    Args:
        iso_file (str): The path to the ISO file whose directory is to be renamed.

    Returns:
        bool: True if the directory was renamed, False otherwise.
    """
    directory = os.path.dirname(iso_file)
    iso_file_name = os.path.splitext(os.path.basename(iso_file))[0]
    parent_directory = os.path.basename(directory)

    if parent_directory == iso_file_name:
        logging.info(
            f"Directory {directory} already has the correct name."
        )
        return False

    files_in_directory = [file for file
                          in os.listdir(directory)
                          if os.path.isfile(
                            os.path.join(directory, file))]

    iso_files_in_directory = [file for file
                              in files_in_directory
                              if file.endswith('.iso')]

    if len(iso_files_in_directory) != 1:
        logging.warning(
            f"Directory {directory} contains multiple .iso files. Skipping renaming."
        )
        return False

    new_directory = os.path.join(os.path.dirname(directory), iso_file_name)
    os.rename(directory, new_directory)
    logging.info(
        f"Renamed directory from {directory} to {new_directory}"
    )
    
    return True


