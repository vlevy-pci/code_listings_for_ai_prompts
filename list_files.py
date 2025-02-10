import argparse
import glob
import os

def list_files(directory, pattern, recursive):
    """Returns a list of file paths matching the given pattern in the specified directory."""
    search_pattern = os.path.join(directory, '**', pattern) if recursive else os.path.join(directory, pattern)
    return glob.glob(search_pattern, recursive=recursive)

def print_file_contents(file_path, base_directory):
    """Prints the contents of the file with a formatted header."""
    relative_path = os.path.relpath(file_path, base_directory)
    print(f"{relative_path}:")
    print("```")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(file.read())
    except Exception as e:
        print(f"Error reading file: {e}")
    print("```")
    print()

def main():
    parser = argparse.ArgumentParser(description="List and print the contents of files matching a pattern.")
    parser.add_argument('-r', '--recursive', action='store_true', help="Recursively search directories.")
    parser.add_argument('-d', '--directory', default=os.getcwd(), help="Directory to search (defaults to current directory).")
    parser.add_argument('pattern', help="File pattern to match (e.g., *.cs).")
    
    args = parser.parse_args()
    
    files = list_files(args.directory, args.pattern, args.recursive)
    if not files:
        print("No matching files found.")
        return
    
    for file_path in sorted(files):
        print_file_contents(file_path, args.directory)

if __name__ == "__main__":
    main()
