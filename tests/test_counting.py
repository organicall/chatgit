#!/usr/bin/env python3
"""Test script to verify AST counting logic"""

import os
import sys
from rag_101.retriever import generate_repo_ast

# Test on current directory
repo_path = "/Users/ritwikbhattacharyya/Downloads/ChatGit"
print(f"Analyzing repository: {repo_path}\n")

result = generate_repo_ast(repo_path)

print("=" * 60)
print("REPOSITORY STATISTICS")
print("=" * 60)
print(f"Total Files: {result['stats']['total_files']}")
print(f"Total Functions: {result['stats']['total_functions']}")
print(f"Total Classes: {result['stats']['total_classes']}")
print(f"Total Imports: {result['stats']['total_imports']}")
print()

# Show breakdown by file
print("=" * 60)
print("BREAKDOWN BY FILE")
print("=" * 60)
for file_path, file_info in sorted(result['files'].items()):
    if file_path.endswith('.py'):
        if 'error' in file_info:
            print(f"\n{file_path}: ERROR - {file_info['error']}")
        else:
            num_funcs = len(file_info.get('functions', []))
            num_classes = len(file_info.get('classes', []))
            num_imports = len(file_info.get('imports', []))
            print(f"\n{file_path}:")
            print(f"  Functions: {num_funcs}")
            print(f"  Classes: {num_classes}")
            print(f"  Imports: {num_imports}")
            
            # Show function names
            if num_funcs > 0:
                func_names = [f['name'] for f in file_info.get('functions', [])]
                print(f"  Function names: {', '.join(func_names)}")
            
            # Show class names with method counts
            if num_classes > 0:
                for cls in file_info.get('classes', []):
                    print(f"  Class '{cls['name']}' with {len(cls.get('methods', []))} methods")

print("\n" + "=" * 60)
print("ALL FUNCTIONS FOUND")
print("=" * 60)
for func in result['functions']:
    print(f"  {func['file']}::{func['name']} (line {func['line']})")

print(f"\nTotal unique functions: {len(result['functions'])}")
