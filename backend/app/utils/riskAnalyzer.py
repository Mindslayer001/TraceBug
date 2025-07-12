import ast
import builtins

class RiskAnalyzer:
    def __init__(self, code):
        self.code = code
        self.lines = code.splitlines()
        self.tree = ast.parse(code)
        self.defined_names = set()
        self.used_names = set()

    def get_full_line(self, lineno):
        if 1 <= lineno <= len(self.lines):
            return self.lines[lineno - 1].strip()
        return ""

    def find_division_risks(self):
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div)]

    def find_eval_usage(self):
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Name)
                and n.func.id == "eval"]

    def find_dangerous_imports(self):
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
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.Attribute) and n.attr in {"__dict__", "__class__", "__globals__"}]

    def find_builtin_shadowing(self):
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.Assign)
                for target in n.targets
                if isinstance(target, ast.Name) and target.id in dir(builtins)]

    def find_broad_excepts(self):
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.ExceptHandler)
                and (n.type is None or (isinstance(n.type, ast.Name) and n.type.id == "Exception"))]

    def find_infinite_loops(self):
        risky = []
        for n in ast.walk(self.tree):
            if isinstance(n, ast.While) and isinstance(n.test, ast.Constant) and n.test.value is True:
                if not any(isinstance(child, ast.Break) for child in ast.walk(n)):
                    risky.append((n.lineno, self.get_full_line(n.lineno)))
        return risky

    def find_hardcoded_secrets(self):
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.Assign)
                for target in n.targets
                if isinstance(target, ast.Name)
                and 'key' in target.id.lower()
                and isinstance(n.value, ast.Constant)
                and isinstance(n.value.value, str)]

    def find_unpacking_mismatches(self):
        risky = []
        for n in ast.walk(self.tree):
            if isinstance(n, ast.Assign):
                if isinstance(n.targets[0], ast.Tuple) and isinstance(n.value, (ast.List, ast.Tuple)):
                    if len(n.targets[0].elts) != len(n.value.elts):
                        risky.append((n.lineno, self.get_full_line(n.lineno)))
        return risky

    def find_undefined_variables(self):
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
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in {"call", "Popen"}:
                    for kw in node.keywords:
                        if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                            risky.append((node.lineno, self.get_full_line(node.lineno)))
        return risky

    def find_sql_string_concats(self):
        risky = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "execute":
                    for arg in node.args:
                        if isinstance(arg, (ast.BinOp, ast.JoinedStr)):
                            risky.append((node.lineno, self.get_full_line(node.lineno)))
        return risky

    def find_duplicate_defs(self):
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
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.ExceptHandler)
                and len(n.body) == 1
                and isinstance(n.body[0], ast.Pass)]

    def find_too_many_arguments(self, limit=6):
        return [(n.lineno, self.get_full_line(n.lineno))
                for n in ast.walk(self.tree)
                if isinstance(n, ast.FunctionDef) and len(n.args.args) > limit]

    def find_yield_outside_generator(self):
        risky = []
        yield_lines = {n.lineno for n in ast.walk(self.tree) if isinstance(n, ast.Yield)}

        for n in ast.walk(self.tree):
            if isinstance(n, ast.FunctionDef):
                if not any(isinstance(child, ast.Yield) for child in ast.walk(n)):
                    # Remove valid yields inside generators
                    yield_lines -= {c.lineno for c in ast.walk(n) if isinstance(c, ast.Yield)}

        for lineno in yield_lines:
            risky.append((lineno, self.get_full_line(lineno)))
        return risky

    def run_all_checks(self):
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
            "yield_outside_generator": self.find_yield_outside_generator()
        }
        return checks
    
    def flatten_risks(self):
        all_risks = self.run_all_checks()
        if not all_risks:
            return []

        flattened = []
        for issues in all_risks.values():
            if issues:
                flattened.extend(issues)
        return flattened
