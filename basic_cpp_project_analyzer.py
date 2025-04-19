import os
import re
import argparse

def analyze_project(path):
    metrics = {
        'headers': 0,
        'sources': 0,
        'lines': 0,
        'classes': 0,
        'templates': 0,
        'structs': 0,
        'enums': 0,
        'log_statements': 0,
    }

    # regex patterns
    class_pattern = re.compile(r"\bclass\b")
    template_pattern = re.compile(r"\btemplate\b")
    struct_pattern = re.compile(r"\bstruct\b")
    enum_pattern = re.compile(r"\benum\b")
    log_pattern = re.compile(r"LOG\(")

    for root, dirs, files in os.walk(path):
        # skip 'vendor' directories
        dirs[:] = [d for d in dirs if d.lower() != 'vendor']

        for fname in files:
            _, ext = os.path.splitext(fname)
            if ext not in ['.h', '.hpp', '.cpp', '.cc', '.cxx']:
                continue

            full_path = os.path.join(root, fname)

            # count files
            if ext in ['.h', '.hpp']:
                metrics['headers'] += 1
            else:
                metrics['sources'] += 1

            # analyze file contents
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        metrics['lines'] += 1
                        if class_pattern.search(line):
                            metrics['classes'] += 1
                        if template_pattern.search(line):
                            metrics['templates'] += 1
                        if struct_pattern.search(line):
                            metrics['structs'] += 1
                        if enum_pattern.search(line):
                            metrics['enums'] += 1
                        if log_pattern.search(line):
                            metrics['log_statements'] += 1
            except Exception as e:
                print(f"Warning: could not read {full_path}: {e}")

    return metrics


def print_metrics(metrics):
    print("Analysis Results:")
    print(f"  Number of header files:   {metrics['headers']}")
    print(f"  Number of source files:   {metrics['sources']}")
    print(f"  Total lines of code:      {metrics['lines']}")
    print(f"  Number of classes:        {metrics['classes']}")
    print(f"  Number of templates:      {metrics['templates']}")
    print(f"  Number of structs:        {metrics['structs']}")
    print(f"  Number of enums:          {metrics['enums']}")
    print(f"  Number of LOG statements: {metrics['log_statements']}")


def main():
    parser = argparse.ArgumentParser(description='Analyze C++ project basic properties')
    parser.add_argument('path', help='Path to the root of the C++ project')
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a directory or does not exist.")
        return

    metrics = analyze_project(args.path)
    print_metrics(metrics)

if __name__ == '__main__':
    main()
