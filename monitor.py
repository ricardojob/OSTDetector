import ast


class MonitorVisitor(ast.NodeVisitor):
    # def __init__(self, file_name):   
        # self.file_name = file_name
        
# def with_ast(file_name):

    def visit_Module(self, node):
        print('Modulo: ',  node.__dict__)
        self.generic_visit(node)
        # for name in node.names:
        #     modules.add(name.name.split(".")[0])

    def visit_Import(self, node):
        for name in node.names:
            modules.add(name.name.split(".")[0])
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module is not None and node.level == 0:
            modules.add(node.module.split(".")[0])
        self.generic_visit(node) 
    
    
    # def report(self):
    #     return list(self.modules)


modules = set()
if __name__ == '__main__':
    python_file = 'input/decorator-sample.py'
    # with_finder(python_file)    
    with open(python_file) as file:
        monitor = MonitorVisitor()
        monitor.visit(ast.parse(file.read()))
        print('Módulos carregados com AST: ')
        # print(monitor.report())
    for mod in modules:
        print(mod)
# Modulo:  {'body': 
# [<_ast.Import object at 0x7f86bd098f40>, 
# <_ast.Import object at 0x7f86bd06c9a0>, 
# <_ast.ClassDef object at 0x7f86bd0850d0>], 
# 'type_ignores': []
# }
    