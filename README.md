# code_listings_for_ai_prompts

This Python script allows you to list and display file contents based on a specified pattern. It supports recursive directory searching, file exclusion using regex patterns, and outputting results to a file or standard output.

## Features

- **Recursive Search**: Optionally search through subdirectories.
- **Pattern Matching**: Match files using a specified pattern (e.g., `*.txt`).
- **Exclude Files**: Exclude files matching a regex pattern.
- **Output Options**: Print results to the console or write to a file, with options to append or overwrite.
- **Names Only**: Option to display only file names without contents.

## Requirements

- Python 3.6 or higher

## Usage

Run the script using the command line with the following options:

`python list_files.py [-h] [-r] [-d DIRECTORY] [-o OUTPUT] [-a] [-x EXCLUDE] [-n] pattern`

### Arguments

- `pattern`: File pattern to search (e.g., `*.cs`).

### Options

- `-h, --help`: Show the help message and exit.
- `-r, --recursive`: Recursively search directories.
- `-d DIRECTORY, --directory DIRECTORY`: Directory to search (default: current directory).
- `-o OUTPUT, --output OUTPUT`: Output file to write the listing (default: standard output).
- `-a, --append`: Append to the output file instead of overwriting.
- `-x EXCLUDE, --exclude EXCLUDE`: Exclude files matching this regex pattern in their full path.
- `-n, --names-only`: Show only file names without displaying contents.

## Examples

1. **List all `.txt` files in the current directory:**

   ```bash
   python list_files.py "*.txt"
   ```

2. **Recursively list all `.py` files in a specific directory:**

   ```bash
   python list_files.py -r -d /path/to/directory "*.py"
   ```

3. **List files excluding those in `obj` directories:**

   ```bash
   python list_files.py -x ".*[/\\\\]obj[/\\\\].*" "*.cs"
   ```

4. **Output file names only to a file, appending to it:**

   ```bash
   python list_files.py -n -o output.txt -a "*.md"
   ```

## Error Handling

- If an invalid regex pattern is provided for exclusion, the script will print an error message and exit.

## License

This project is licensed under the MIT License.
