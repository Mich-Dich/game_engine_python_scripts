import os
import re

def count_lines_of_code(directory):
    in_block_comment = False

    log_patterns = [r'\bCORE_LOG\b', r'\bLOG\b']
    log_regex = re.compile('|'.join(log_patterns))

    for root, dirs, files in os.walk(directory):
        # Skip any 'vendor' directories
        dirs[:] = [d for d in dirs if d != 'vendor']
        for file in files:
            if file.endswith('.cpp') or file.endswith('.h'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='latin-1') as f:
                        for line in f:

                            line = line.strip()
                            if line.startswith("#include"):
                                print(f"line: {line}")
                    
                except Exception as e:
                    print(f"Skipping file {file} due to error: {e}")
    
    return

def find_projects(directory):
    projects = []
    for root, dirs, files in os.walk(directory):
        # Skip any 'vendor' directories
        dirs[:] = [d for d in dirs if 'vendor' not in root.split(os.sep)]
        for file in files:
            if file.endswith('.vcxproj'):
                projects.append(root)
                break
    return projects

if __name__ == "__main__":
    directory = input("Enter the path to the main directory: ")
    projects = find_projects(directory)
    for project in projects:
        project_name = os.path.basename(project)
    
        print()
        print(f"---- Project '{project_name}' ---- ")
        count_lines_of_code(project)
        print()
