#!/usr/bin/env python3
"""Test FlashCode repository analysis"""

import os
import sys
from rag_101.retriever import generate_repo_ast

# Test on FlashCode
repo_path = "/tmp/FlashCode"
print(f"Analyzing repository: {repo_path}\n")

result = generate_repo_ast(repo_path)

print("=" * 70)
print("FLASHCODE REPOSITORY STATISTICS")
print("=" * 70)
print(f"Total Files: {result['stats']['total_files']}")
print(f"Total Functions: {result['stats']['total_functions']}")
print(f"Total Classes: {result['stats']['total_classes']}")
print(f"Total Imports: {result['stats']['total_imports']}")
print()

# Show breakdown by file
print("=" * 70)
print("BREAKDOWN BY FILE")
print("=" * 70)
for file_path, file_info in sorted(result['files'].items()):
    if file_path.endswith('.py'):
        if 'error' in file_info:
            print(f"\n{file_path}: ERROR - {file_info['error']}")
        else:
            num_funcs = len(file_info.get('functions', []))
            num_classes = len(file_info.get('classes', []))
            num_imports = len(file_info.get('imports', []))
            if num_funcs > 0 or num_classes > 0:
                print(f"\n{file_path}:")
                print(f"  Functions: {num_funcs}")
                print(f"  Classes: {num_classes}")
                print(f"  Imports: {num_imports}")
                
                # Show function names
                if num_funcs > 0:
                    func_names = [f['name'] for f in file_info.get('functions', [])]
                    print(f"  Functions: {', '.join(func_names)}")
                
                # Show class names with method counts
                if num_classes > 0:
                    for cls in file_info.get('classes', []):
                        method_names = [m['name'] for m in cls.get('methods', [])]
                        print(f"  Class '{cls['name']}': {len(cls.get('methods', []))} methods ({', '.join(method_names)})")

print("\n" + "=" * 70)
print("ALL FUNCTIONS SUMMARY")
print("=" * 70)
print(f"\nTotal Functions: {len(result['functions'])}")
print(f"Total Classes: {len(result['classes'])}")
print(f"Total Imports: {len(result['imports'])}")

print("\n" + "=" * 70)
print("LIST OF ALL FUNCTIONS")
print("=" * 70)
for idx, func in enumerate(result['functions'], 1):
    print(f"{idx:3}. {func['file']}::{func['name']} (line {func['line']})")

print("\n" + "=" * 70)
print("LIST OF ALL CLASSES")
print("=" * 70)
for idx, cls in enumerate(result['classes'], 1):
    methods_count = len(cls.get('methods', []))
    print(f"{idx}. {cls['name']} in {cls['file']} (line {cls['line']}) - {methods_count} methods - {cls.get('language', 'unknown')}")
