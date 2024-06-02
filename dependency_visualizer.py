import os
import re
from collections import defaultdict

def count_lines_of_code(directory):
    include_regex = re.compile(r'#include\s*["<](.*?)[">]')
    dependency_dict = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        # Skip any 'vendor' directories
        dirs[:] = [d for d in dirs if d != 'vendor']
        for file in files:
            if file.endswith('.h'):
                try:
                    with open(os.path.join(root, file), 'r', encoding='latin-1') as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith("#include"):
                                match = include_regex.search(line)
                                if match:
                                    file_path = match.group(1)
                                    included_file_name_with_ext = os.path.basename(file_path)
                                    included_file_name, _ = os.path.splitext(included_file_name_with_ext)
                                    file_name, _ = os.path.splitext(file)
                                    
                                    # Add to the dependency dictionary
                                    dependency_dict[included_file_name].append(file_name)
                except Exception as e:
                    print(f"Skipping file {file} due to error: {e}")

    return dependency_dict

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

def build_tree(dependency_dict, root, indent=""):
    print(f"{indent}{root}")

    if indent == "":
        indent = " └─ "

    if root in dependency_dict:
        for dep in dependency_dict[root]:
            build_tree(dependency_dict, dep, "  " + indent)

if __name__ == "__main__":
    directory = input("Enter the path to the main directory: ")
    projects = find_projects(directory)
    for project in projects:
        project_name = os.path.basename(project)
    
        print()
        print(f"---- Project '{project_name}' ---- ")
        dependency_dict = count_lines_of_code(project)
        
        # Print the tree-graph representation
        for root in dependency_dict:
            if all(root not in deps for deps in dependency_dict.values()):
                build_tree(dependency_dict, root)
        print()
