import os
import re

def count_lines_of_code(directory):
    in_block_comment = False

    num_precompiler = 0
    num_log_statements = 0
    num_enum = 0
    num_class = 0
    num_templates = 0
    num_struct = 0
    lines_of_code = 0

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
                            if not line:
                                continue  # Skip blank lines
                            
                            if in_block_comment:
                                if '*/' in line:
                                    line = line.split('*/', 1)[1]
                                    in_block_comment = False
                                else:
                                    continue
                            if '/*' in line and '*/' in line:
                                line = line.split('/*', 1)[0] + line.split('*/', 1)[1]
                            elif '/*' in line:
                                line = line.split('/*', 1)[0]
                                in_block_comment = True
                            if '//' in line:
                                line = line.split('//', 1)[0]
                                
                            if not line:
                                continue  # Skip lines that are now empty
                            
                            lines_of_code += 1

                            if line.startswith("#"):
                                num_precompiler += 1

                            elif log_regex.search(line):
                                num_log_statements += 1

                            elif line.__contains__("enum ") and not line.__contains__(";"):
                                num_enum += 1
                                # print(f"enum: {line}")

                            elif line.__contains__("class ") and not line.__contains__(";"):
                                num_class += 1
                                # print(f"class: {line}")

                            elif line.__contains__("template") and not line.__contains__(";"):
                                num_templates += 1
                                # print(f"template: {line}")

                            elif line.__contains__("struct ") and not line.__contains__(";"):
                                num_struct += 1
                                # print(f"struct: {line}")
                    
                except Exception as e:
                    print(f"Skipping file {file} due to error: {e}")
    
    return num_precompiler, num_log_statements, num_enum, num_class, num_templates, num_struct, lines_of_code

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
        num_precompiler, num_log_statements, num_enum, num_class, num_templates, num_struct, lines_of_code, = count_lines_of_code(project)
    
        print()
        print(f"---- Project '{project_name}' ---- ")
        print(f"   precompiler      {num_precompiler}")
        print(f"   log statements   {num_log_statements}")
        print(f"   enums            {num_enum}")
        print(f"   classes          {num_class}")
        print(f"   templates        {num_templates}")
        print(f"   structs          {num_struct}")
        print(f"   lines-of-code:   {lines_of_code}")
