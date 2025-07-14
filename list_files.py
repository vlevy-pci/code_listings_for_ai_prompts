import argparse
import glob
import os
import re
import sys


def list_files(
    directory: str, pattern: str, recursive: bool, exclude_pattern: str | None
) -> list[str]:
    """Retrieve a sorted list of files matching the pattern in the specified directory, excluding files matching the exclude regex pattern.

    Args:
        directory (str): The directory to search for files.
        pattern (str): The pattern to match against file names.
        recursive (bool): Whether to search recursively through subdirectories.
        exclude_pattern (str | None): The regex pattern to exclude files from the search.
    """
    search_pattern: str = (
        os.path.join(directory, "**", pattern)
        if recursive
        else os.path.join(directory, pattern)
    )
    files = sorted(glob.glob(search_pattern, recursive=recursive, include_hidden=True))

    # Exclude files using a regex pattern
    if exclude_pattern:
        try:
            exclude_regex = re.compile(exclude_pattern)
            files = [file for file in files if not exclude_regex.search(file)]
            print(f"Excluding files matching regex: {exclude_pattern}")
        except re.error as e:
            print(f"Invalid regex pattern: {e}")
            sys.exit(1)

    print(f"Found {len(files)} files matching pattern: {pattern}")
    return files


def get_relative_file_path(file_path: str, base_dir: str) -> str:
    """Return the relative file path from the specified base directory.

    Args:
        file_path (str): The full path of the file.
        base_dir (str): The base directory to calculate the relative path from.
    """
    return os.path.relpath(file_path, base_dir)


def read_file_content(filepath: str) -> str:
    """Read and return the content of the given file, trimming trailing whitespace and removing BOM if present.

    Args:
        filepath (str): The path to the file to read.
    """
    try:
        with open(
            filepath, "r", encoding="utf-8-sig"
        ) as file:  # 'utf-8-sig' removes BOM if present
            return "\n".join(
                line.rstrip() for line in file
            )  # Trim trailing whitespace from each line
    except Exception as ex:
        return f"[Error reading file: {ex}]"


def process_files(
    directory: str,
    pattern: str,
    recursive: bool,
    exclude_pattern: str | None,
    output_file: str | None,
    append_mode: bool,
    names_only: bool,
) -> None:
    """Process files and output either names only or full contents incrementally to stdout or a file.

    Args:
        directory (str): The directory to search for files.
        pattern (str): The pattern to match against file names.
        recursive (bool): Whether to search recursively through subdirectories.
        exclude_pattern (str | None): The regex pattern to exclude files from the search.
        output_file (str | None): The file to write the output to.
        append_mode (bool): Whether to append to the output file instead of overwriting.
        names_only (bool): Whether to only output file names.
    """
    files: list[str] = list_files(directory, pattern, recursive, exclude_pattern)

    # If an output file is specified, handle overwrite or append mode
    if output_file:
        if os.path.exists(output_file) and not append_mode:
            while True:
                user_choice = (
                    input(
                        f"File '{output_file}' already exists. Overwrite (o) or Append (a)? "
                    )
                    .strip()
                    .lower()
                )
                if user_choice in ["o", "a"]:
                    append_mode = user_choice == "a"
                    break
                print("Please enter 'o' to Overwrite or 'a' to Append.")

        # Open file in append mode ('a') if requested, otherwise overwrite ('w')
        file_mode = "a" if append_mode else "w"
        output_stream = open(output_file, file_mode, encoding="utf-8")
    else:
        output_stream = sys.stdout  # Print to console if no file is specified

    try:
        for file in files:
            relative_path = get_relative_file_path(file, directory)

            if names_only:
                output = relative_path  # Only print file name
            else:
                content: str = read_file_content(file)
                output = f"Start of {relative_path} >>>>\n```\n{content}\n``` <<<< End of {relative_path}\n"

            # Write output incrementally
            print(output, file=output_stream)

        if output_file:
            print(
                f"Output {'appended to' if append_mode else 'written to'} {output_file}"
            )
    finally:
        if output_file:
            output_stream.close()  # Close file if writing to one


def main() -> None:
    """Parse command-line arguments and execute the program.

    Args:
        None
    """
    parser = argparse.ArgumentParser(
        description="List and display file contents based on a pattern."
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Recursively search directories."
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=os.getcwd(),
        help="Directory to search (default: current directory).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file to write the listing (default: standard output).",
    )
    parser.add_argument(
        "-a",
        "--append",
        action="store_true",
        help="Append to the output file instead of overwriting.",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        type=str,
        help="Exclude files matching this regex pattern in their full path (e.g., '.*[/\\\\]obj[/\\\\].*').",
    )
    parser.add_argument(
        "-n",
        "--names-only",
        action="store_true",
        help="Show only file names without displaying contents.",
    )
    parser.add_argument(
        "pattern", type=str, help="File pattern to search (e.g., '*.cs')."
    )

    args = parser.parse_args()

    # Process files with incremental output
    process_files(
        args.directory,
        args.pattern,
        args.recursive,
        args.exclude,
        args.output,
        args.append,
        args.names_only,
    )


if __name__ == "__main__":
    main()
