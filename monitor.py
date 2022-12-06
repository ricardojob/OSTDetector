import ast

def all_files(dir, extension='.py'):
    """ 
    List all files in dir
    """
    from pathlib import Path
    path = Path(dir)
    files = []
    for file in path.rglob(pattern=f'*{extension}'):
        files.append(file)
    
    # [print(f) for f in files]
    return files
    
class MonitorVisitor(ast.NodeVisitor):
    def __init__(self):   
        self.chaves = dict()
        self.classe = ""
        self.funcao = ""
        
    def transform(self, context, node):
        pass
        # if isinstance(node, ast.Attribute): 
        #     print(f"classe:{self.classe}, func:{self.funcao}, linha: {node.lineno}, contexto: {context}, Attribute:  {node.value.id}, Attr: {node.attr}")
        # if isinstance(node, ast.Name):
        #     print(f'classe:{self.classe}, func:{self.funcao}, linha: {node.lineno}, contexto: {context}, Name:  {node.id}')  
        # if isinstance(parent, ast.Call):
        #     for arg in parent.args:
        #         self.transform("arg", arg, node)

    
    def visit_Call(self, node):
        function = node.func
        # print(f'Call  dicts: {node.__dict__}')
        self.transform("call",function)
        for arg in node.args:
            self.transform("arg", arg)

        for key in node.keywords: # todo: tratamento ao conditional/decorator
            self.transform("keys", key.arg)

        self.generic_visit(node) 
        
    def visit_Import(self, node):
        for name in node.names:
            # print(f'{name.name} -> {name.asname}')
            modules.add(name.name.split(".")[0])
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module is not None and node.level == 0:
            modules.add(node.module.split(".")[0])
        self.generic_visit(node) 

    def visit_FunctionDef(self, node):
        self.funcao = node.name
        ast.NodeVisitor.generic_visit(self, node)    
                    
    def visit_AsyncFunctionDef(self, node):
        self.funcao = node.name
        ast.NodeVisitor.generic_visit(self, node)    
    # def visit_Module(self, node):
    #     print('load:',node.__dict__)
    #     ast.NodeVisitor.generic_visit(self, node)        

    def visit_ClassDef(self, node):
        self.classe = node.name
        ast.NodeVisitor.generic_visit(self, node)
    # def visit_Attribute(self, node):
    #     print(f"linhas: {node.lineno}, Attribute:  {node.value.id}, Attr: {node.attr}")
    #     self.generic_visit(node) 
    # def visit_Name(self, node):
    #     print(f'linha: { node.lineno}, visit_Name: {node.id} {node.__dict__}')
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
    # all_files('/home/ricardojob/dev/study-01-platform/')

# print('default')
# import sys
# print(sys.modules)
        
# Modulo:  {'body': 
# [<_ast.Import object at 0x7f86bd098f40>, 
# <_ast.Import object at 0x7f86bd06c9a0>, 
# <_ast.ClassDef object at 0x7f86bd0850d0>], 
# 'type_ignores': []
# }
    