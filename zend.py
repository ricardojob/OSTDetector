'''
Get all function calls from a python file
The MIT License (MIT)
Copyright (c) 2016 Suhas S G <jargnar@gmail.com>
source: https://gist.github.com/jargnar/0946ab1d985e2b4ab776
'''
import ast
from collections import deque


class FuncCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)


def get_func_calls(tree):
    func_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)
            func_calls.append(callvisitor.name)

    return func_calls

if __name__ == '__main__':
    python_file = 'input/import-sample.py'
    with open(python_file) as file:
        tree = ast.parse(file.read())
        print(get_func_calls(tree))

