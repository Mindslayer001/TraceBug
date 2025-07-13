"""
RiskAnalyzer: A static code analysis tool for identifying potential security, reliability,
and maintainability risks in Python source code.

This class uses Python's built-in Abstract Syntax Tree (AST) module to traverse
the parsed code and detect a wide range of risky patterns such as:
    - Dangerous function usage (e.g., eval, pickle)
    - Hardcoded secrets and prompts
    - Undefined or shadowed variables
    - SQL injection risks
    - Infinite loops and deep nesting
    - Broad or empty exception handling
    - Mutable default arguments
    - Use of magic numbers, unescaped SQL, and more

Intended use: Static analysis in CI/CD pipelines, security reviews, or educational tools.
"""

import ast
import builtins

class RiskAnalyzer:
    def __init__(self, code):
        # Initialize with source code and parse it into AST
        self.code = code
        self.lines = code.splitlines()
        self.tree = ast.parse(code)
        self.defined_names = set()
        self.used_names = set()

    def get_full_line(self, lineno):
        # Safely retrieves the line of code at the given line number
        if 1 <= lineno <= len(self.lines):
            return self.lines[lineno - 1].strip()
        return ""

    def find_division_risks(self):
        # Detects division operations that may lead to ZeroDivisionError
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div)]

    def find_eval_usage(self):
        # Detects use of the built-in eval() function (can lead to code injection)
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "eval"]

    def find_dangerous_imports(self):
        # Flags imports of modules known for potentially risky behavior
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in {"pickle", "os", "subprocess"}:
                        risky.append((node.lineno, self.get_full_line(node.lineno)))
            elif isinstance(node, ast.ImportFrom):
                if node.module in {"pickle", "os", "subprocess"}:
                    risky.append((node.lineno, self.get_full_line(node.lineno)))
        return risky

    def find_attribute_risks(self):
        # Flags access to special/private attributes like __dict__, __class__, etc.
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.Attribute) and n.attr in {"__dict__", "__class__", "__globals__"}]

    def find_builtin_shadowing(self):
        # Detects assignments that shadow built-in names (e.g., `list = ...`)
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.Assign)
                for target in n.targets
                if isinstance(target, ast.Name) and target.id in dir(builtins)]

    def find_broad_excepts(self):
        # Flags exception handlers that catch all or too broad exceptions
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.ExceptHandler)
                and (n.type is None or (isinstance(n.type, ast.Name) and n.type.id == "Exception"))]

    def find_infinite_loops(self):
        # Detects `while True` loops without a break statement
        risky = []
        for n in ast.walk(self.tree):
            if isinstance(n, ast.While) and isinstance(n.test, ast.Constant) and n.test.value is True:
                if not any(isinstance(child, ast.Break) for child in ast.walk(n)):
                    risky.append((n.lineno, self.get_full_line(n.lineno)))
        return risky

    def find_hardcoded_secrets(self):
        # Detects string literals assigned to variable names containing "key"
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.Assign)
                for target in n.targets
                if isinstance(target, ast.Name)
                and 'key' in target.id.lower()
                and isinstance(n.value, ast.Constant)
                and isinstance(n.value.value, str)]

    def find_unpacking_mismatches(self):
        # Detects mismatches in tuple unpacking (e.g., a, b = (1,))
        risky = []
        for n in ast.walk(self.tree):
            if isinstance(n, ast.Assign):
                if isinstance(n.targets[0], ast.Tuple) and isinstance(n.value, (ast.List, ast.Tuple)):
                    if len(n.targets[0].elts) != len(n.value.elts):
                        risky.append((n.lineno, self.get_full_line(n.lineno)))
        return risky

    def find_undefined_variables(self):
        # Detects use of variables before they are defined
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.defined_names.add(node.name)
                for arg in node.args.args:
                    self.defined_names.add(arg.arg)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.defined_names.add(target.id)
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                self.used_names.add(node.id)
        undefined = self.used_names - self.defined_names - set(dir(builtins))
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Name) and node.id in undefined and isinstance(node.ctx, ast.Load):
                risky.append((node.lineno, self.get_full_line(node.lineno)))
        return risky

    def find_subprocess_shell_usage(self):
        # Detects dangerous use of shell=True in subprocess calls
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in {"call", "Popen"}:
                    for kw in node.keywords:
                        if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                            risky.append((node.lineno, self.get_full_line(node.lineno)))
        return risky

    def find_sql_string_concats(self):
        # Detects SQL query execution that includes string concatenation or f-strings
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "execute":
                    for arg in node.args:
                        if isinstance(arg, (ast.BinOp, ast.JoinedStr)):
                            risky.append((node.lineno, self.get_full_line(n.lineno)))
        return risky

    def find_duplicate_defs(self):
        # Flags duplicate function or class definitions
        seen = set()
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if node.name in seen:
                    risky.append((node.lineno, self.get_full_line(node.lineno)))
                else:
                    seen.add(node.name)
        return risky

    def find_deep_nesting(self, max_depth=3):
        # Detects control structures nested deeper than the allowed threshold
        risky = []
        def visit(node, depth=0):
            if depth > max_depth:
                risky.append((node.lineno, self.get_full_line(node.lineno)))
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.Try)):
                    visit(child, depth + 1)
        visit(self.tree)
        return risky

    def find_empty_except_blocks(self):
        # Flags empty `except` blocks (only contains `pass`)
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.ExceptHandler)
                and len(n.body) == 1
                and isinstance(n.body[0], ast.Pass)]

    def find_too_many_arguments(self, limit=6):
        # Detects functions with more than the recommended number of arguments
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.FunctionDef) and len(n.args.args) > limit]

    def find_yield_outside_generator(self):
        # Flags `yield` used outside of generator functions
        risky = []
        yield_lines = {n.lineno for n in ast.walk(self.tree) if isinstance(n, ast.Yield)}
        for n in ast.walk(self.tree):
            if isinstance(n, ast.FunctionDef):
                if not any(isinstance(child, ast.Yield) for child in ast.walk(n)):
                    yield_lines -= {c.lineno for c in ast.walk(n) if isinstance(c, ast.Yield)}
        for lineno in yield_lines:
            risky.append((lineno, self.get_full_line(lineno)))
        return risky

    def find_mutable_defaults(self):
        # Flags functions with mutable default arguments like lists or dicts
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        risky.append((node.lineno, self.get_full_line(node.lineno)))
        return risky

    def find_is_literal_comparisons(self):
        # Detects `is` used to compare against literals (should use `==` instead)
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Compare):
                if isinstance(node.ops[0], ast.Is):
                    if any(isinstance(comp, (ast.Num, ast.Str, ast.Constant)) for comp in node.comparators):
                        risky.append((node.lineno, self.get_full_line(node.lineno)))
        return risky

    def find_pickle_usage(self):
        # Detects use of pickle.load (potentially unsafe deserialization)
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "load" and isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":
                    risky.append((node.lineno, self.get_full_line(node.lineno)))
        return risky

    def find_magic_numbers(self, exceptions={0, 1, -1}):
        # Flags numeric constants (except safe ones) directly in code
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                if node.value not in exceptions and node.lineno:
                    risky.append((node.lineno, self.get_full_line(node.lineno)))
        return risky

    def find_prompt_leaks(self):
        # Flags string constants assigned to prompt-like variable names
        risky = []
        keywords = {"prompt", "instruction", "secret"}
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and any(k in target.id.lower() for k in keywords):
                        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                            risky.append((node.lineno, self.get_full_line(node.lineno)))
        return risky

    def find_unescaped_sql_params(self):
        # Detects raw SQL queries passed to `.execute()` without parameterization
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "execute":
                    if len(node.args) == 1:
                        risky.append((node.lineno, self.get_full_line(node.lineno)))
        return risky

    def run_all_checks(self):
        # Runs all risk-detection methods and returns them grouped by category
        checks = {
            "division_risks": self.find_division_risks(),
            "eval_usage": self.find_eval_usage(),
            "dangerous_imports": self.find_dangerous_imports(),
            "attribute_risks": self.find_attribute_risks(),
            "builtin_shadowing": self.find_builtin_shadowing(),
            "broad_excepts": self.find_broad_excepts(),
            "infinite_loops": self.find_infinite_loops(),
            "hardcoded_secrets": self.find_hardcoded_secrets(),
            "unpacking_mismatches": self.find_unpacking_mismatches(),
            "undefined_variables": self.find_undefined_variables(),
            "subprocess_shell_usage": self.find_subprocess_shell_usage(),
            "sql_string_concats": self.find_sql_string_concats(),
            "duplicate_defs": self.find_duplicate_defs(),
            "deep_nesting": self.find_deep_nesting(),
            "empty_except_blocks": self.find_empty_except_blocks(),
            "too_many_arguments": self.find_too_many_arguments(),
            "yield_outside_generator": self.find_yield_outside_generator(),
            "mutable_defaults": self.find_mutable_defaults(),
            "is_literal_comparisons": self.find_is_literal_comparisons(),
            "pickle_usage": self.find_pickle_usage(),
            "magic_numbers": self.find_magic_numbers(),
            "prompt_leaks": self.find_prompt_leaks(),
            "unescaped_sql_params": self.find_unescaped_sql_params(),
        }
        return checks

    def flatten_risks(self):
        # Flattens all issues into a single list of (line number, code) tuples
        all_risks = self.run_all_checks()
        if not all_risks:
            return list('No risks found in the provided code snippet.')
        flattened = []
        for issues in all_risks.values():
            if issues:
                flattened.extend(issues)
        return flattened
