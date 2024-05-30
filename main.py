import glob
import os
import re


def read_all_files_from_directory(directory, pattern="*"):
    all_files = []
    # Use glob to match the pattern
    for file_path in glob.glob(os.path.join(directory, pattern), recursive=True):
        if os.path.isfile(file_path):
            all_files.append(file_path)
        elif os.path.isdir(file_path):
            read_all_files_from_directory(file_path, pattern)
    return all_files

# Specify the directory and pattern (e.g., "*.txt" for text files)
directory_path = './pandas/pandas/core/methods'
file_pattern = '**/*.py'

# Read all files from the directory matching the pattern
files = read_all_files_from_directory(directory_path, file_pattern)

global LOC
LOC = 0

global empty_lines
empty_lines = 0

global SLOC
SLOC = 0

global LSI
LSI = 0

global CLOC
CLOC = 0


def calculate_stats(filepath):
    global LOC
    global empty_lines
    global SLOC
    global CLOC
    with open(filepath, 'r') as file:
        lines = file.readlines()
        line_count = len(lines)
        LOC += line_count

        empty_lines_in_file = sum(1 for line in lines if line in ('\n', '\r\n'))
        empty_lines += empty_lines_in_file


        with open(filepath, 'r') as file:
            content = file.read()
            # Regular expression to match comments
            comment_pattern = r'#.*|(\'\'\'[\s\S]*?\'\'\'|\"\"\"[\s\S]*?\"\"\")'
            comments = re.findall(comment_pattern, content)
            CLOC += len(comments)

            comment_line_numbers = set()
            for comment in comments:
                # Find the line number of each comment
                start_line = content.count('\n', 0, content.find(comment)) + 1
                end_line = start_line + comment.count('\n')
                comment_line_numbers.update(range(start_line, end_line + 1))
            total_lines = len(lines)
            blank_line_numbers = {i for i, line in enumerate(content.split('\n'), start=1) if not line.strip()}

            non_comment_count = sum(
                1 for i in range(1, total_lines + 1) if i not in comment_line_numbers and i not in blank_line_numbers)
            SLOC += non_comment_count



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for filename in files:
        calculate_stats(filename)
    print("LOC: %i" % LOC)
    print("Empty lines: %i" % empty_lines)
    print("SLOC: %i" % SLOC)
    print("CLOC: %i" % CLOC)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
