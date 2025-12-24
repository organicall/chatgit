import ast
import networkx as nx

from pathlib import Path
import re

class FunctionDependencyAnalyzer:
    """Analyzes function dependencies in code using AST"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.function_info = {}
    
    def analyze_python_file(self, file_path):
        """Parse a Python file and extract function dependencies"""
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read(), filename=str(file_path))
            except SyntaxError:
                return
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                self.graph.add_node(func_name)
                
                self.function_info[func_name] = {
                    'file': str(file_path),
                    'line': node.lineno,
                    'docstring': ast.get_docstring(node) or "No docstring"
                }
                
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name):
                            called_func = child.func.id
                            self.graph.add_edge(func_name, called_func)
    
    def analyze_repository(self, repo_path):
        """Analyze all supported files in a repository"""
        repo_path = Path(repo_path)
        
        # Define supported extensions
        supported_exts = {'.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.swift', '.c', '.cpp', '.cc', '.cxx', '.h', '.hpp'}
        
        for file_path in repo_path.rglob("*.*"):
            if any(skip in str(file_path) for skip in ['venv', '__pycache__', '.git', 'node_modules']):
                continue
            
            ext = file_path.suffix.lower()
            if ext not in supported_exts:
                continue
                
            if ext == '.py':
                self.analyze_python_file(file_path)
            else:
                self.analyze_generic_file(file_path)

    def analyze_generic_file(self, file_path):
        """Analyze a non-Python file for function definitions and calls using regex"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            ext = Path(file_path).suffix.lower()
            
            # Function definition patterns
            func_patterns = []
            if ext in {'.js', '.jsx', '.ts', '.tsx'}:
                func_patterns = [
                    r"function\s+(\w+)\s*\(", 
                    r"const\s+(\w+)\s*=\s*\(.*?\)\s*=>", 
                    r"const\s+(\w+)\s*=\s*function"
                ]
            elif ext == '.java':
                func_patterns = [r"(?:public|protected|private)\s+\w+\s+(\w+)\s*\("]
            elif ext == '.swift':
                func_patterns = [r"func\s+(\w+)"]
            elif ext in {'.c', '.cpp', '.cc', '.cxx', '.h', '.hpp'}:
                func_patterns = [r"\w+\s+(\w+)\s*\("]
            
            # Find definitions
            defined_funcs_with_pos = []
            for pat in func_patterns:
                for match in re.finditer(pat, content):
                    func_name = match.group(1)
                    if func_name in {'if', 'while', 'for', 'switch', 'catch'}:
                        continue
                        
                    self.graph.add_node(func_name)
                    self.function_info[func_name] = {
                        'file': str(file_path),
                        'line': content[:match.start()].count('\n') + 1,
                        'docstring': "No docstring (regex)"
                    }
                    defined_funcs_with_pos.append((match.start(), func_name))
            
            defined_funcs_with_pos.sort()
            
            # Find calls (simple heuristic: word followed by parenthesis)
            call_pattern = r"(\w+)\s*\("
            
            for match in re.finditer(call_pattern, content):
                called_name = match.group(1)
                if called_name in {'if', 'while', 'for', 'switch', 'catch', 'return'}:
                    continue
                
                call_index = match.start()
                
                # Find which function this call belongs to
                caller_name = None
                for i in range(len(defined_funcs_with_pos)):
                    start, name = defined_funcs_with_pos[i]
                    if call_index > start:
                        if i + 1 < len(defined_funcs_with_pos):
                            next_start, _ = defined_funcs_with_pos[i+1]
                            if call_index < next_start:
                                caller_name = name
                                break
                        else:
                            caller_name = name
                            break
                
                if caller_name and caller_name != called_name:
                    self.graph.add_edge(caller_name, called_name)

        except Exception as e:
            print(f"Error analyzing generic file {file_path}: {e}")
    
    def find_dependencies(self, function_name):
        """Find all functions this function calls"""
        if function_name not in self.graph:
            return []
        return list(self.graph.successors(function_name))
    
    def find_callers(self, function_name):
        """Find all functions that call this function"""
        if function_name not in self.graph:
            return []
        return list(self.graph.predecessors(function_name))
    
    def get_function_importance(self):
        """Calculate importance scores using PageRank"""
        try:
            pagerank = nx.pagerank(self.graph)
            return sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
        except:
            return []
    
