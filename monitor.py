import ast

class MonitorVisitor(ast.NodeVisitor):
    def __init__(self):   
        self.chaves = dict()
    def visit_Attribute(self, node):
        print(f"linhas: {node.lineno}, Attribute:  {node.value.id}, Attr: {node.attr}")
        self.generic_visit(node) 
    
    def visit_Call(self, node):
        function = node.func
        if isinstance(function, ast.Attribute):
            print(f"linha: {function.lineno}, Attribute:  {function.value.id}, Attr: {function.attr}")
        if isinstance(function, ast.Name):
            print(f'linha: {function.lineno}, Name:  {function.id}, Args: {node.args}')    
        self.generic_visit(node) 
        
    def visit_Import(self, node):
        for name in node.names:
            print(f'{name.name} -> {name.asname}')
            modules.add(name.name.split(".")[0])
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module is not None and node.level == 0:
            modules.add(node.module.split(".")[0])
        self.generic_visit(node) 
    
    # def visit_Name(self, node):
    #     print(f'Nome: {node.id} linha: { node.lineno}')
    #     self.generic_visit(node) 

    # def visit_Module(self, node):
    #     print('Modulo: ',  node.__dict__)
    #     self.generic_visit(node)   

modules = set()
if __name__ == '__main__':
    python_file = 'input/import-sample.py'
    with open(python_file) as file:
        monitor = MonitorVisitor()
        monitor.visit(ast.parse(file.read()))
    print('Módulos carregados com AST: ')
    print(', '.join(list(modules)))
        
# Modulo:  {'body': 
# [<_ast.Import object at 0x7f86bd098f40>, 
# <_ast.Import object at 0x7f86bd06c9a0>, 
# <_ast.ClassDef object at 0x7f86bd0850d0>], 
# 'type_ignores': []
# }
    