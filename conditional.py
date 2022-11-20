import ast
from pprint import pprint

class IfVisitor(ast.NodeVisitor):
    count = 0
    
    # Attribute(expr value, identifier attr, expr_context ctx)
    def parse_attr(self, attribute):
        if isinstance(attribute.value, ast.Name):
            print('value attribute: ', attribute.value.id)
        if isinstance(attribute.value, ast.Attribute):
            self.parse_attr(attribute.value)
        print('name attribute: ', attribute.attr)

    # Compare(expr left, cmpop* ops, expr* comparators)
    def parse_compare(self, compare):
        if isinstance(compare.left, ast.Name):
            print('left compare: ', compare.left.id)
        for comparator in compare.comparators:    
            if isinstance(comparator, ast.Constant):
                print('comparators compare: ', comparator.value)            
    
    # Call(expr func, expr* args, keyword* keywords)
    def parse_call(self, call):
        # print('call func: ', call.func)
        if isinstance(call.func, ast.Name):
            print('call func id: ', call.func.id)
        if isinstance(call.func, ast.Attribute):
            self.parse_attr(call.func)
        for arg in call.args:    
            if isinstance(arg, ast.Constant):
                print('call args: ', arg.value)

    def visit_If(self, node):
        self.count+=1
        if isinstance(node.test, ast.Attribute):
            self.parse_attr(node.test)
        if isinstance(node.test, ast.Compare):
            self.parse_compare(node.test)
        if isinstance(node.test, ast.Call):
            self.parse_call(node.test)
        ast.NodeVisitor.generic_visit(self, node)    

class IfReader():
    def __init__(self, filename):   
        self.filename = filename
        
    def fetch(self):
        with open(self.filename, "r") as source:
            tree = ast.parse(source.read())
            # pprint(ast.dump(tree))
            visitor = IfVisitor()
            visitor.visit(tree)
            print(visitor.count)

count = 0
if __name__ == '__main__':
    reader = IfReader("input/platform-if-sample.py")
    reader.fetch()
    

