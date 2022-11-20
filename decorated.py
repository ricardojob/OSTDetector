import ast
import astunparse
from pprint import pprint

class DecoratorVisitor(ast.NodeVisitor):
    def __init__(self, decorator):   
        self.decorator = decorator
    
    def flatten_attr(self, node):
        if isinstance(node, ast.Attribute):
            return str(self.flatten_attr(node.value)) + '.' + node.attr
        elif isinstance(node, ast.Name):
            return str(node.id)
        else:
            pass    
    
    # Attribute(expr value, identifier attr, expr_context ctx)
    def parse_attr(self, attribute):
        if isinstance(attribute.value, ast.Name):
            print('value attribute: ', attribute.value.id)
        if isinstance(attribute.value, ast.Attribute):
            self.parse_attr(attribute.value)
        print('name attribute: ', attribute.attr)

    # Compare(expr left, cmpop* ops, expr* comparators)
    def parse_compare(self, compare):
        if isinstance(compare.left, ast.Attribute):
            self.parse_attr(compare.left)
        if isinstance(compare.left, ast.Name):
            print('left compare: ', compare.left.id)
        for comparator in compare.comparators:    
            if isinstance(comparator, ast.Constant):
                print('comparators compare: ', comparator.value)
    
    def parse_decorator(self, node):
        # d ('func', 'args', 'keywords')
        for d in node.decorator_list: 
            if not isinstance(d, ast.Call):
                continue
            if not self.flatten_attr(d.func) == self.decorator:
                continue
            # @unittest.skipIf(condition, reason) Skip the decorated test if condition is true.   
            # @unittest.skipIf(sys.platform == 'win32', "Windows select() doesn't support file descriptors.")
            # print('[Function] ', node.name)
            for arg in d.args:
                if isinstance(arg, ast.Compare):
                    self.parse_compare(arg)
                if isinstance(arg, ast.Constant):
                    print('[reason] call args: ', arg.value)

    # FunctionDef(identifier name, arguments args,stmt* body, expr* decorator_list, expr? returns, string? type_comment)
    def visit_FunctionDef(self, node):
        # print('visit_FunctionDef')
        self.parse_decorator(node)
        ast.NodeVisitor.generic_visit(self, node)    
                    
    # AsyncFunctionDef(identifier name, arguments args,stmt* body, expr* decorator_list, expr? returns,string? type_comment)
    def visit_AsyncFunctionDef(self, node):
        # print('visit_AsyncFunctionDef')
        self.parse_decorator(node)
        ast.NodeVisitor.generic_visit(self, node)    

    # ClassDef(identifier name,expr* bases,keyword* keywords,stmt* body,expr* decorator_list)
    def visit_ClassDef(self, node):
        # print('visit_ClassDef')
        self.parse_decorator(node)
        ast.NodeVisitor.generic_visit(self, node)
                
class DecoratorReader():
    def __init__(self, filename, decorator):   
        self.filename = filename
        self.decorator = decorator
        
    def fetch(self):
        with open(self.filename, "r") as source:
            tree = ast.parse(source.read())
            # pprint(ast.dump(tree))
            visitor = DecoratorVisitor(self.decorator)
            visitor.visit(tree)

if __name__ == '__main__':
    reader = DecoratorReader("input/decorator-sample.py", 'unittest.skipIf')
    reader.fetch()