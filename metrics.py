"""Воспроизводимый лексический вариант метрик Холстеда и AST Маккейба."""
import ast
from collections import Counter
import io
import json
import keyword
import math
from pathlib import Path
import tokenize


def halstead(source):
    operators, operands = Counter(), Counter()
    for source in source if isinstance(source, list) else [source]:
        tree = ast.parse(source)
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)):
                if node.body and isinstance(node.body[0], ast.Expr):
                    value = node.body[0].value
                    if isinstance(value, ast.Constant) and isinstance(value.value, str):
                        docstrings.add((value.lineno, value.col_offset))
        for token in tokenize.generate_tokens(io.StringIO(source).readline):
            if token.start in docstrings:
                continue
            if token.type == tokenize.OP:
                operators[token.string] += 1
            elif token.type == tokenize.NAME:
                if keyword.iskeyword(token.string):
                    operators[token.string] += 1
                else:
                    operands[token.string] += 1
            elif token.type in (tokenize.STRING, tokenize.NUMBER):
                operands[token.string] += 1
    n1, n2 = len(operators), len(operands)
    N1, N2 = sum(operators.values()), sum(operands.values())
    n, N = n1 + n2, N1 + N2
    volume = N * math.log2(n) if n else 0
    difficulty = n1 / 2 * N2 / n2 if n2 else 0
    return dict(n1=n1, n2=n2, N1=N1, N2=N2, n=n, N=N,
                V=volume, D=difficulty, E=volume * difficulty,
                operators=dict(sorted(operators.items())),
                operands=dict(sorted(operands.items())))


def cyclomatic(source, name):
    function = next(n for n in ast.parse(source).body
                    if isinstance(n, ast.FunctionDef) and n.name == name)
    decisions = []
    for node in ast.walk(function):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler,
                             ast.IfExp)):
            decisions.append([node.lineno, type(node).__name__, 1])
        elif isinstance(node, ast.BoolOp):
            decisions.append([node.lineno, type(node.op).__name__,
                              len(node.values) - 1])
        elif isinstance(node, ast.comprehension):
            decisions.append([node.target.lineno, "comprehension",
                              1 + len(node.ifs)])
    return dict(function=name, decisions=sorted(decisions),
                P=sum(item[2] for item in decisions),
                V=1 + sum(item[2] for item in decisions))


if __name__ == "__main__":
    root = Path(__file__).parent
    sources = [(root / name).read_text(encoding="utf-8")
               for name in ("main.py", "task_manager.py")]
    # Суммирование счётчиков важно: словари двух модулей пересекаются.
    combined = "\n".join(sources)
    result = {"scope": ["main.py", "task_manager.py"],
              "halstead": halstead(sources),
              "mccabe": cyclomatic(sources[1], "complete_task"),
              "python": __import__("sys").version}
    print(json.dumps(result, ensure_ascii=False, indent=2))
