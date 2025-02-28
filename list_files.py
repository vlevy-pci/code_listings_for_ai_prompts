import argparse
import glob
import os
import sys
import re
from typing import List, Optional


def list_files(
    directory: str, pattern: str, recursive: bool, exclude_pattern: Optional[str]
) -> List[str]:
    """Retrieve a sorted list of files matching the pattern in the specified directory, excluding files matching the exclude regex pattern."""
    search_pattern: str = (
        os.path.join(directory, "**", pattern)
        if recursive
        else os.path.join(directory, pattern)
    )
    files = sorted(glob.glob(search_pattern, recursive=recursive))

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


def read_file_content(filepath: str) -> str:
    """Read and return the content of the given file, trimming trailing whitespace and removing BOM if present."""
    try:
        with open(
            filepath, "r", encoding="utf-8-sig"
        ) as file:  # 'utf-8-sig' removes BOM if present
            return "\n".join(
                line.rstrip() for line in file
            )  # Trim trailing whitespace from each line
    except Exception as e:
        return f"[Error reading file: {e}]"


def format_output(file_path: str, content: str, base_dir: str) -> str:
    """Format the output with the file path and content enclosed in triple backticks."""
    relative_path: str = os.path.relpath(file_path, base_dir)
    return f"{relative_path}:\n```\n{content}\n```\n"


def process_files(
    directory: str,
    pattern: str,
    recursive: bool,
    exclude_pattern: Optional[str],
    output_file: Optional[str],
    append_mode: bool,
) -> None:
    """Process files and output incrementally to stdout or a file."""
    files: List[str] = list_files(directory, pattern, recursive, exclude_pattern)

    # If an output file is specified, handle overwrite or append mode
    if output_file:
        if os.path.exists(output_file) and not append_mode:
            user_choice = (
                input(f"File '{output_file}' already exists. Overwrite? (y/n): ")
                .strip()
                .lower()
            )
            if user_choice != "y":
                print("Operation aborted.")
                sys.exit(0)  # Exit the program if the user chooses not to overwrite

        # Open file in append mode ('a') if requested, otherwise overwrite ('w')
        file_mode = "a" if append_mode else "w"
        output_stream = open(output_file, file_mode, encoding="utf-8")
    else:
        output_stream = sys.stdout  # Print to console if no file is specified

    try:
        for file in files:
            content: str = read_file_content(file)
            formatted_output: str = format_output(file, content, directory)

            # Write output incrementally
            print(
                formatted_output, file=output_stream, flush=True
            )  # Flush ensures real-time writing

        if output_file:
            print(
                f"Output {'appended to' if append_mode else 'written to'} {output_file}"
            )
    finally:
        if output_file:
            output_stream.close()  # Close file if writing to one


def main() -> None:
    """Parse command-line arguments and execute the program."""
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
    )


if __name__ == "__main__":
    main()
