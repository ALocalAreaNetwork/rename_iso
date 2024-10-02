import argparse
from rename_iso.rename_iso import setup_logging, get_iso_files, rename_iso, rename_directory


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing the directory to search for ISO files,
                            verbosity flag, and quiet flag.
    """
    parser = argparse.ArgumentParser(
        description="Rename ISO files and their directories based on SFV files.")
    parser.add_argument(
        "directory",
        help="The directory to search for ISO files.",
        type=str)
    parser.add_argument(
        "-v",
        "--verbosity",
        action="store_true",
        help="Increase output verbosity to DEBUG level.")
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Decrease output verbosity to WARNING level.")
    return parser.parse_args()


def main():
    """
    Main function to rename ISO files and their directories based on SFV files.
    
    This function parses command-line arguments, sets up logging based on verbosity flags,
    retrieves ISO files from the specified directory, and renames each ISO file and its
    corresponding directory if the renaming is successful.
    """
    args = parse_arguments()
    setup_logging(args.verbosity, args.quiet)

    iso_files = get_iso_files(args.directory)
    for iso_file in iso_files:
        if rename_iso(iso_file):
            rename_directory(iso_file)


if __name__ == "__main__":
    main() # pragma: no cover