import os
import json
import argparse
import re
import ast
import tokenize
from io import StringIO
from typing import Dict, Any, List, Tuple, Optional
import datetime

# Import LangChain components
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputParser
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables - you'll need to set OPENAI_API_KEY
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def detect_language(filename: str) -> str:
    """Detect programming language from file extension."""
    extension = os.path.splitext(filename)[1].lower()
    
    if extension == ".py":
        return "Python"
    elif extension == ".js":
        return "JavaScript"
    elif extension == ".jsx":
        return "React/JSX"
    else:
        return "Unknown"

def get_language_rules(language: str) -> str:
    """Get language-specific coding standards."""
    rules = {
        "Python": """
        - Follow PEP 8 style guide
        - Use snake_case for functions and variables
        - Use CamelCase for classes
        - Include docstrings for modules, classes, functions
        - Limit line length to 79 characters
        - Use 4 spaces for indentation
        - Avoid global variables
        - Use list/dict comprehensions where appropriate
        - Properly handle exceptions
        - Use descriptive variable names
        """,
        
        "JavaScript": """
        - Use camelCase for variables and functions
        - Use PascalCase for classes
        - Use meaningful variable names
        - Prefer const and let over var
        - Use === and !== instead of == and !=
        - Use arrow functions for callbacks
        - Use template literals for string formatting
        - Handle errors with try/catch
        - Use semicolons consistently
        - Prefer ES6+ features
        """,
        
        "React/JSX": """
        - Use functional components with hooks when possible
        - Keep components small and focused
        - Use PascalCase for component names
        - Use camelCase for props and state
        - Destructure props and state
        - Use proper key props when rendering lists
        - Avoid inline styles
        - Extract reusable logic into custom hooks
        - Handle side effects properly in useEffect
        - Avoid prop drilling with Context or state management
        """
    }
    
    return rules.get(language, "No specific rules available for this language")

def create_analysis_prompt(code: str, filename: str) -> str:
    """Create a prompt for code analysis."""
    language = detect_language(filename)
    language_rules = get_language_rules(language)
    
    system_prompt = """You are an expert code reviewer specializing in clean code practices. 
    Analyze the provided code and score it based on the following criteria:
    
    1. Naming conventions (10 points): Variable and function naming clarity and consistency
    2. Function length and modularity (20 points): How well functions are broken down and organized
    3. Comments and documentation (20 points): Presence and quality of comments and docstrings
    4. Formatting/indentation (15 points): Consistency and readability of code layout
    5. Reusability and DRY (15 points): Avoiding repetition and promoting reuse
    6. Best practices in web dev (20 points): Following language-specific and web development best practices
    
    Provide your assessment as a JSON object with the following structure:
    {
      "overall_score": <integer between 0-100>,
      "breakdown": {
        "naming": <integer between 0-10>,
        "modularity": <integer between 0-20>,
        "comments": <integer between 0-20>,
        "formatting": <integer between 0-15>,
        "reusability": <integer between 0-15>,
        "best_practices": <integer between 0-20>
      },
      "recommendations": [
        <3-5 string recommendations for improving the code>
      ]
    }
    
    The recommendations should be specific, actionable, and clear, pointing to exact issues in the code.
    Your response must be a valid JSON object and nothing else.
    """
    
    human_prompt = f"""
    Please analyze this {language} code:
    
    ```
    {code}
    ```
    
    Consider these {language} best practices:
    {language_rules}
    
    Provide a comprehensive analysis with specific recommendations.
    """
    
    return system_prompt, human_prompt

def create_enhanced_system_prompt(analysis_data: Dict[str, Any]) -> str:
    """Create enhanced system prompt with code structure insights."""
    language = analysis_data.get("language", "Unknown")
    metrics = analysis_data.get("metrics", {})
    
    # Format metrics into a readable string
    metrics_str = "\n".join([f"- {k}: {v}" for k, v in metrics.items() if isinstance(v, (int, float))])
    
    prompt = f"""You are an expert code reviewer specializing in {language} and clean code practices.
    Analyze the provided code and score it based on the following criteria:
    
    1. Naming conventions (10 points): Variable and function naming clarity and consistency
    2. Function length and modularity (20 points): How well functions are broken down and organized
    3. Comments and documentation (20 points): Presence and quality of comments and docstrings
    4. Formatting/indentation (15 points): Consistency and readability of code layout
    5. Reusability and DRY (15 points): Avoiding repetition and promoting reuse
    6. Best practices in web dev (20 points): Following language-specific and web development best practices
    
    Code structure information:
    - File: {analysis_data.get("filename", "Unknown")}
    - Language: {language}
    - Lines of code: {analysis_data.get("line_count", 0)}
    - Functions: {analysis_data.get("function_count", 0)}
    - Classes: {analysis_data.get("class_count", 0)}
    - Imports: {analysis_data.get("import_count", 0)}
    - Variables: {analysis_data.get("variable_count", 0)}
    - Comments: {analysis_data.get("comment_count", 0)}
    
    Metrics:
    {metrics_str}
    
    Provide your assessment as a JSON object with the following structure:
    {{
      "overall_score": <integer between 0-100>,
      "breakdown": {{
        "naming": <integer between 0-10>,
        "modularity": <integer between 0-20>,
        "comments": <integer between 0-20>,
        "formatting": <integer between 0-15>,
        "reusability": <integer between 0-15>,
        "best_practices": <integer between 0-20>
      }},
      "recommendations": [
        <3-5 string recommendations for improving the code>
      ]
    }}
    
    The recommendations should be specific, actionable, and clear, pointing to exact issues in the code.
    Your response must be a valid JSON object and nothing else.
    """
    
    return prompt

def create_enhanced_human_prompt(code: str, filename: str, analysis_data: Dict[str, Any]) -> str:
    """Create enhanced human prompt with code and language rules."""
    language = analysis_data.get("language", "Unknown")
    language_rules = get_language_rules(language)
    
    prompt = f"""
    Please analyze this {language} code:
    
    ```
    {code}
    ```
    
    Consider these {language} best practices:
    {language_rules}
    
    Provide a comprehensive analysis with specific recommendations. The focus should be on:
    1. Naming conventions and consistency
    2. Function length and modularity
    3. Quality of comments and documentation
    4. Code formatting and readability
    5. Code reusability and DRY principles
    6. Adherence to {language} best practices
    
    The recommendations should be specific to this code and clearly actionable.
    """
    
    return prompt

class CodeIndex:
    """Class for indexing and analyzing code structure."""
    
    def __init__(self, file_path: str):
        """Initialize with file path and read content."""
        self.file_path = file_path
        self.filename = os.path.basename(file_path)
        self.language = detect_language(self.filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
            
        # Analysis results
        self.functions = []
        self.classes = []
        self.imports = []
        self.variables = []
        self.comments = []
        self.line_count = len(self.content.splitlines())
        self.metrics = {}
        
        # Index the file based on language
        self._index_file()
    
    def _index_file(self):
        """Index file based on language type."""
        if self.language == "Python":
            self._index_python()
        elif self.language in ["JavaScript", "React/JSX"]:
            self._index_javascript()
    
    def _index_python(self):
        """Index Python code using AST."""
        try:
            # Parse the code into an AST
            tree = ast.parse(self.content)
            
            # Extract functions
            for node in ast.walk(tree):
                # Extract function definitions
                if isinstance(node, ast.FunctionDef):
                    function = {
                        'name': node.name,
                        'line_start': node.lineno,
                        'line_end': self._find_node_end_line(node),
                        'args': [arg.arg for arg in node.args.args],
                        'has_docstring': self._has_docstring(node),
                        'complexity': self._calculate_complexity(node)
                    }
                    self.functions.append(function)
                
                # Extract class definitions
                elif isinstance(node, ast.ClassDef):
                    class_def = {
                        'name': node.name,
                        'line_start': node.lineno,
                        'line_end': self._find_node_end_line(node),
                        'methods': [method.name for method in node.body if isinstance(method, ast.FunctionDef)],
                        'has_docstring': self._has_docstring(node)
                    }
                    self.classes.append(class_def)
                
                # Extract import statements
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            self.imports.append({
                                'name': name.name,
                                'alias': name.asname,
                                'line': node.lineno,
                                'from': None
                            })
                    else:  # ImportFrom
                        for name in node.names:
                            self.imports.append({
                                'name': name.name,
                                'alias': name.asname,
                                'line': node.lineno,
                                'from': node.module
                            })
                
                # Extract global variables
                elif isinstance(node, ast.Assign) and hasattr(node, 'lineno'):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var = {
                                'name': target.id,
                                'line': node.lineno,
                                'type': self._get_value_type(node.value)
                            }
                            self.variables.append(var)
            
            # Extract comments
            self._extract_python_comments()
            
            # Calculate metrics
            self._calculate_python_metrics()
            
        except SyntaxError as e:
            print(f"Error parsing Python file {self.filename}: {e}")
    
    def _index_javascript(self):
        """Index JavaScript/JSX code using regex patterns."""
        # Function definition patterns for regular JS and arrow functions
        fn_patterns = [
            r'function\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\([^)]*\)\s*{',  # Regular functions
            r'(?:const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*function\s*\([^)]*\)\s*{',  # Function expressions
            r'(?:const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*\([^)]*\)\s*=>\s*[{(]'  # Arrow functions
        ]
        
        # Class definition pattern
        class_pattern = r'class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)'
        
        # Import pattern
        import_patterns = [
            r'import\s+\{([^}]+)\}\s+from\s+[\'"]([^\'"]+)[\'"]',  # import { x, y } from 'module'
            r'import\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s+from\s+[\'"]([^\'"]+)[\'"]',  # import x from 'module'
            r'import\s+[\'"]([^\'"]+)[\'"]'  # import 'module'
        ]
        
        # Component pattern (for React)
        component_pattern = r'(?:const|let|var)\s+([A-Z][a-zA-Z0-9_$]*)\s*=\s*(?:React\.createClass|React\.memo|React\.forwardRef|\([^)]*\)\s*=>\s*|function\s*\([^)]*\))'
        
        # Extract functions
        for pattern in fn_patterns:
            for match in re.finditer(pattern, self.content):
                name = match.group(1)
                line_start = self.content.count('\n', 0, match.start()) + 1
                
                # Estimate line end by finding the closing brace
                code_after_match = self.content[match.end():]
                open_braces = 1
                char_count = 0
                
                for char in code_after_match:
                    char_count += 1
                    if char == '{':
                        open_braces += 1
                    elif char == '}':
                        open_braces -= 1
                        if open_braces == 0:
                            break
                
                line_end = line_start + code_after_match[:char_count].count('\n')
                
                function = {
                    'name': name,
                    'line_start': line_start,
                    'line_end': line_end,
                    'type': 'arrow_function' if '=>' in match.group(0) else 'function',
                    'complexity': self._estimate_js_complexity(self.content[match.start():match.end() + char_count])
                }
                self.functions.append(function)
        
        # Extract classes
        for match in re.finditer(class_pattern, self.content):
            name = match.group(1)
            line_start = self.content.count('\n', 0, match.start()) + 1
            
            # Similar approach to find the end of the class
            code_after_match = self.content[match.end():]
            open_braces = 0
            char_count = 0
            
            # Find the opening brace first
            for char in code_after_match:
                char_count += 1
                if char == '{':
                    open_braces = 1
                    break
            
            # Then find the matching closing brace
            remaining_code = code_after_match[char_count:]
            for i, char in enumerate(remaining_code):
                if char == '{':
                    open_braces += 1
                elif char == '}':
                    open_braces -= 1
                    if open_braces == 0:
                        char_count += i + 1
                        break
            
            line_end = line_start + code_after_match[:char_count].count('\n')
            
            class_def = {
                'name': name,
                'line_start': line_start,
                'line_end': line_end
            }
            self.classes.append(class_def)
        
        # Extract imports
        for pattern in import_patterns:
            for match in re.finditer(pattern, self.content):
                if '{' in pattern:  # Destructured imports
                    imports = [imp.strip() for imp in match.group(1).split(',')]
                    module = match.group(2)
                    for imp in imports:
                        # Handle aliased imports like "originalName as alias"
                        if ' as ' in imp:
                            name, alias = imp.split(' as ')
                        else:
                            name, alias = imp, None
                        
                        self.imports.append({
                            'name': name.strip(),
                            'alias': alias.strip() if alias else None,
                            'from': module,
                            'line': self.content.count('\n', 0, match.start()) + 1
                        })
                elif 'from' in pattern:  # Default import
                    name = match.group(1)
                    module = match.group(2)
                    self.imports.append({
                        'name': name,
                        'alias': None,
                        'from': module,
                        'line': self.content.count('\n', 0, match.start()) + 1
                    })
                else:  # Side-effect import
                    module = match.group(1)
                    self.imports.append({
                        'name': None,
                        'alias': None,
                        'from': module,
                        'line': self.content.count('\n', 0, match.start()) + 1
                    })
        
        # Extract React components (if it's a React file)
        if self.language == "React/JSX":
            for match in re.finditer(component_pattern, self.content):
                name = match.group(1)
                line = self.content.count('\n', 0, match.start()) + 1
                self.functions.append({
                    'name': name,
                    'line_start': line,
                    'type': 'component',
                    'is_react_component': True
                })
        
        # Extract variables
        var_pattern = r'(?:const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*='
        for match in re.finditer(var_pattern, self.content):
            # Skip if this is a function or component (already captured)
            next_chars = self.content[match.end():match.end()+20].strip()
            if next_chars.startswith('function') or next_chars.startswith('(') or next_chars.startswith('React.'):
                continue
                
            name = match.group(1)
            line = self.content.count('\n', 0, match.start()) + 1
            
            # Try to determine the type
            value_start = match.end()
            value_end = self.content.find(';', value_start)
            if value_end == -1:  # No semicolon, try to find end of line
                value_end = self.content.find('\n', value_start)
            
            if value_end == -1:  # Still not found, take next 50 chars
                value_end = value_start + 50
                
            value_text = self.content[value_start:value_end].strip()
            
            # Determine type based on value
            type_info = 'unknown'
            if value_text.startswith('"') or value_text.startswith("'") or value_text.startswith('`'):
                type_info = 'string'
            elif value_text.startswith('['):
                type_info = 'array'
            elif value_text.startswith('{'):
                type_info = 'object'
            elif value_text.startswith('true') or value_text.startswith('false'):
                type_info = 'boolean'
            elif value_text.replace('.', '', 1).isdigit():
                type_info = 'number'
            elif value_text.startswith('new '):
                type_info = value_text.split('new ')[1].split('(')[0].strip()
            
            self.variables.append({
                'name': name,
                'line': line,
                'type': type_info
            })
        
        # Extract comments
        self._extract_js_comments()
        
        # Calculate metrics
        self._calculate_js_metrics()
    
    def _has_docstring(self, node):
        """Check if a Python AST node has a docstring."""
        if not node.body:
            return False
        
        first_node = node.body[0]
        if isinstance(first_node, ast.Expr) and isinstance(first_node.value, ast.Str):
            return True
        
        return False
    
    def _find_node_end_line(self, node):
        """Find the ending line number of a Python AST node."""
        # Get the maximum line number from the node and all its children
        max_line = getattr(node, 'lineno', 0)
        
        # Check all child nodes
        for child in ast.iter_child_nodes(node):
            if hasattr(child, 'lineno'):
                child_end = self._find_node_end_line(child)
                max_line = max(max_line, child_end)
        
        return max_line
    
    def _get_value_type(self, node):
        """Get the type of a Python AST value node."""
        if isinstance(node, ast.Num):
            return 'number'
        elif isinstance(node, ast.Str):
            return 'string'
        elif isinstance(node, ast.List):
            return 'list'
        elif isinstance(node, ast.Dict):
            return 'dict'
        elif isinstance(node, ast.Tuple):
            return 'tuple'
        elif isinstance(node, ast.NameConstant) and node.value in [True, False]:
            return 'boolean'
        elif isinstance(node, ast.NameConstant) and node.value is None:
            return 'None'
        elif isinstance(node, ast.Call):
            if hasattr(node.func, 'id'):
                return f'call:{node.func.id}'
            elif hasattr(node.func, 'attr'):
                return f'call:{node.func.attr}'
        return 'unknown'
    
    def _calculate_complexity(self, node):
        """Calculate cyclomatic complexity of a Python function."""
        complexity = 1  # Start with 1
        
        # Traverse the AST and count branching nodes
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For)):
                complexity += 1
            elif isinstance(child, ast.BoolOp) and isinstance(child.op, ast.And):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _extract_python_comments(self):
        """Extract comments from Python code."""
        tokens = tokenize.generate_tokens(StringIO(self.content).readline)
        for token in tokens:
            if token.type == tokenize.COMMENT:
                self.comments.append({
                    'text': token.string,
                    'line': token.start[0]
                })
    
    def _extract_js_comments(self):
        """Extract comments from JavaScript/JSX code."""
        # Single line comments
        for match in re.finditer(r'\/\/(.+?)$', self.content, re.MULTILINE):
            line = self.content.count('\n', 0, match.start()) + 1
            self.comments.append({
                'text': match.group(1).strip(),
                'line': line,
                'type': 'single_line'
            })
        
        # Multi-line comments
        for match in re.finditer(r'\/\*(.+?)\*\/', self.content, re.DOTALL):
            start_line = self.content.count('\n', 0, match.start()) + 1
            end_line = start_line + match.group(0).count('\n')
            self.comments.append({
                'text': match.group(1).strip(),
                'line_start': start_line,
                'line_end': end_line,
                'type': 'multi_line'
            })
        
        # JSDoc comments
        for match in re.finditer(r'\/\*\*(.+?)\*\/', self.content, re.DOTALL):
            start_line = self.content.count('\n', 0, match.start()) + 1
            end_line = start_line + match.group(0).count('\n')
            self.comments.append({
                'text': match.group(1).strip(),
                'line_start': start_line,
                'line_end': end_line,
                'type': 'jsdoc'
            })
    
    def _calculate_python_metrics(self):
        """Calculate code quality metrics for Python."""
        metrics = {}
        
        # Function metrics
        if self.functions:
            fn_lines = [fn['line_end'] - fn['line_start'] + 1 for fn in self.functions]
            metrics['avg_function_length'] = sum(fn_lines) / len(fn_lines)
            metrics['max_function_length'] = max(fn_lines)
            metrics['total_functions'] = len(self.functions)
            
            # Complexity
            complexities = [fn.get('complexity', 1) for fn in self.functions]
            metrics['avg_complexity'] = sum(complexities) / len(complexities)
            metrics['max_complexity'] = max(complexities)
        else:
            metrics['avg_function_length'] = 0
            metrics['max_function_length'] = 0
            metrics['total_functions'] = 0
            metrics['avg_complexity'] = 0
            metrics['max_complexity'] = 0
        
        # Documentation metrics
        metrics['documented_functions'] = sum(1 for fn in self.functions if fn.get('has_docstring', False))
        metrics['documentation_ratio'] = metrics['documented_functions'] / max(1, metrics['total_functions'])
        metrics['comment_ratio'] = len(self.comments) / max(1, self.line_count)
        
        # Naming conventions
        snake_case_pattern = re.compile(r'^[a-z][a-z0-9_]*$')
        camel_case_pattern = re.compile(r'^[a-z][a-zA-Z0-9]*$')
        pascal_case_pattern = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
        
        fn_names = [fn['name'] for fn in self.functions]
        var_names = [var['name'] for var in self.variables]
        class_names = [cls['name'] for cls in self.classes]
        
        # Check naming conventions for functions (expected: snake_case)
        metrics['snake_case_functions'] = sum(1 for name in fn_names if snake_case_pattern.match(name))
        metrics['snake_case_ratio_functions'] = metrics['snake_case_functions'] / max(1, len(fn_names))
        
        # Check naming conventions for variables (expected: snake_case)
        metrics['snake_case_variables'] = sum(1 for name in var_names if snake_case_pattern.match(name))
        metrics['snake_case_ratio_variables'] = metrics['snake_case_variables'] / max(1, len(var_names))
        
        # Check naming conventions for classes (expected: PascalCase)
        metrics['pascal_case_classes'] = sum(1 for name in class_names if pascal_case_pattern.match(name))
        metrics['pascal_case_ratio_classes'] = metrics['pascal_case_classes'] / max(1, len(class_names))
        
        self.metrics = metrics
    
    def _calculate_js_metrics(self):
        """Calculate code quality metrics for JavaScript/JSX."""
        metrics = {}
        
        # Function metrics
        if self.functions:
            fn_lines = []
            for fn in self.functions:
                if 'line_end' in fn and 'line_start' in fn:
                    fn_lines.append(fn['line_end'] - fn['line_start'] + 1)
            
            if fn_lines:
                metrics['avg_function_length'] = sum(fn_lines) / len(fn_lines)
                metrics['max_function_length'] = max(fn_lines)
            else:
                metrics['avg_function_length'] = 0
                metrics['max_function_length'] = 0
                
            metrics['total_functions'] = len(self.functions)
            
            # Complexity estimates
            complexities = [fn.get('complexity', 1) for fn in self.functions if 'complexity' in fn]
            if complexities:
                metrics['avg_complexity'] = sum(complexities) / len(complexities)
                metrics['max_complexity'] = max(complexities)
            else:
                metrics['avg_complexity'] = 0
                metrics['max_complexity'] = 0
        else:
            metrics['avg_function_length'] = 0
            metrics['max_function_length'] = 0
            metrics['total_functions'] = 0
            metrics['avg_complexity'] = 0
            metrics['max_complexity'] = 0
        
        # Documentation metrics
        jsdoc_comments = [c for c in self.comments if c.get('type') == 'jsdoc']
        metrics['documented_functions'] = min(len(jsdoc_comments), metrics['total_functions'])
        metrics['documentation_ratio'] = metrics['documented_functions'] / max(1, metrics['total_functions'])
        metrics['comment_ratio'] = len(self.comments) / max(1, self.line_count)
        
        # Naming conventions
        camel_case_pattern = re.compile(r'^[a-z][a-zA-Z0-9]*$')
        pascal_case_pattern = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
        
        fn_names = [fn['name'] for fn in self.functions]
        var_names = [var['name'] for var in self.variables]
        class_names = [cls['name'] for cls in self.classes]
        
        # Check naming conventions for functions (expected: camelCase)
        metrics['camel_case_functions'] = sum(1 for name in fn_names if camel_case_pattern.match(name))
        metrics['camel_case_ratio_functions'] = metrics['camel_case_functions'] / max(1, len(fn_names))
        
        # Check naming conventions for variables (expected: camelCase)
        metrics['camel_case_variables'] = sum(1 for name in var_names if camel_case_pattern.match(name))
        metrics['camel_case_ratio_variables'] = metrics['camel_case_variables'] / max(1, len(var_names))
        
        # Check naming conventions for classes/components (expected: PascalCase)
        metrics['pascal_case_classes'] = sum(1 for name in class_names if pascal_case_pattern.match(name))
        metrics['pascal_case_ratio_classes'] = metrics['pascal_case_classes'] / max(1, len(class_names))
        
        # React specific metrics
        if self.language == "React/JSX":
            metrics['react_components'] = sum(1 for fn in self.functions if fn.get('is_react_component', False))
        
        self.metrics = metrics
    
    def _estimate_js_complexity(self, code_snippet):
        """Estimate cyclomatic complexity of a JavaScript function."""
        complexity = 1  # Start with 1
        
        # Count branching statements
        complexity += code_snippet.count('if (')
        complexity += code_snippet.count('else if')
        complexity += code_snippet.count('for (')
        complexity += code_snippet.count('while (')
        complexity += code_snippet.count('switch (')
        complexity += code_snippet.count('case ')
        complexity += code_snippet.count(' && ')
        complexity += code_snippet.count(' || ')
        complexity += code_snippet.count('?.') # Optional chaining
        complexity += code_snippet.count('??') # Nullish coalescing
        
        return complexity
    
    def get_summary(self):
        """Get a summary of the code structure."""
        return {
            "filename": self.filename,
            "language": self.language,
            "line_count": self.line_count,
            "function_count": len(self.functions),
            "class_count": len(self.classes),
            "import_count": len(self.imports),
            "variable_count": len(self.variables),
            "comment_count": len(self.comments),
            "metrics": self.metrics
        }
    
    def get_detailed_info(self):
        """Get detailed information about the code structure."""
        return {
            "filename": self.filename,
            "language": self.language,
            "line_count": self.line_count,
            "functions": self.functions,
            "classes": self.classes,
            "imports": self.imports,
            "variables": self.variables,
            "comments": self.comments,
            "metrics": self.metrics
        }
    
    def generate_analysis_data(self):
        """Generate data for code quality analysis."""
        analysis_data = self.get_summary()
        
        # Add detailed metrics specific to language
        if self.language == "Python":
            python_specific = {
                "snake_case_compliance": analysis_data["metrics"].get("snake_case_ratio_functions", 0) * 100,
                "pascal_case_compliance": analysis_data["metrics"].get("pascal_case_ratio_classes", 0) * 100,
                "documentation_ratio": analysis_data["metrics"].get("documentation_ratio", 0) * 100,
                "complexity": analysis_data["metrics"].get("avg_complexity", 1)
            }
            analysis_data.update(python_specific)
        elif self.language in ["JavaScript", "React/JSX"]:
            js_specific = {
                "camel_case_compliance": analysis_data["metrics"].get("camel_case_ratio_functions", 0) * 100,
                "pascal_case_compliance": analysis_data["metrics"].get("pascal_case_ratio_classes", 0) * 100,
                "documentation_ratio": analysis_data["metrics"].get("documentation_ratio", 0) * 100,
                "complexity": analysis_data["metrics"].get("avg_complexity", 1)
            }
            analysis_data.update(js_specific)
        
        return analysis_data

def analyze_code(file_path: str, model_name: str = "gpt-4") -> Dict[str, Any]:
    """
    Analyze code file and return quality assessment.
    
    Args:
        file_path: Path to the code file
        model_name: OpenAI model to use
        
    Returns:
        Dictionary with analysis results
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check file extension
    filename = os.path.basename(file_path)
    extension = os.path.splitext(filename)[1].lower()
    if extension not in [".py", ".js", ".jsx"]:
        raise ValueError(f"Unsupported file type: {extension}. Supported types: .py, .js, .jsx")
    
    # Index the code file
    code_index = CodeIndex(file_path)
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        code_content = f.read()
    
    # Create a more detailed prompt using the code index data
    analysis_data = code_index.generate_analysis_data()
    system_prompt = create_enhanced_system_prompt(analysis_data)
    human_prompt = create_enhanced_human_prompt(code_content, filename, analysis_data)
    
    # Initialize the LLM
    llm = ChatOpenAI(model_name=model_name)
    
    # Create messages
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    
    # Generate the response
    response = llm.invoke(messages)
    
    # Extract content from the response
    response_content = response.content
    
    # Parse the JSON response
    try:
        results = json.loads(response_content)
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract JSON from the response
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', response_content, re.DOTALL)
        if json_match:
            results = json.loads(json_match.group(1))
        else:
            raise ValueError("Failed to parse response as JSON")
    
    # Validate the response format
    required_keys = ["overall_score", "breakdown", "recommendations"]
    breakdown_keys = ["naming", "modularity", "comments", "formatting", "reusability", "best_practices"]
    
    for key in required_keys:
        if key not in results:
            raise ValueError(f"Missing required key in response: {key}")
    
    for key in breakdown_keys:
        if key not in results["breakdown"]:
            raise ValueError(f"Missing required breakdown key in response: {key}")
    
    return results

def save_results(results: Dict[str, Any], file_path: str) -> str:
    """Save analysis results to a JSON file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(file_path)
    output_file = f"{filename}_{timestamp}_analysis.json"
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return output_file

def print_results(results: Dict[str, Any], file_path: str) -> None:
    """Print analysis results in a readable format."""
    filename = os.path.basename(file_path)
    language = detect_language(filename)
    
    print("\n" + "=" * 50)
    print(f"CODE ANALYSIS RESULTS: {filename}")
    print("=" * 50)
    
    print(f"\nOverall Score: {results['overall_score']}/100")
    print("\nBreakdown:")
    print(f"  Naming Conventions:      {results['breakdown']['naming']}/10")
    print(f"  Function/Modularity:     {results['breakdown']['modularity']}/20")
    print(f"  Comments/Documentation:  {results['breakdown']['comments']}/20")
    print(f"  Formatting/Indentation:  {results['breakdown']['formatting']}/15")
    print(f"  Reusability/DRY:         {results['breakdown']['reusability']}/15")
    print(f"  Best Practices:          {results['breakdown']['best_practices']}/20")
    
    print("\nRecommendations:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print("\n" + "=" * 50)

def main():
    """Main entry point for command line usage."""
    parser = argparse.ArgumentParser(description="Analyze code quality")
    parser.add_argument("file_path", help="Path to the code file to analyze")
    parser.add_argument("--model", default="gpt-4", help="OpenAI model to use")
    parser.add_argument("--save", action="store_true", help="Save results to a JSON file")
    
    args = parser.parse_args()
    
    try:
        # Analyze the code
        results = analyze_code(args.file_path, args.model)
        
        # Print results
        print_results(results, args.file_path)
        
        # Save results if requested
        if args.save:
            output_file = save_results(results, args.file_path)
            print(f"\nResults saved to: {output_file}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
