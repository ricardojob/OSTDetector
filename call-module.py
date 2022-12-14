import ast
from pathlib import Path


class CallVisitor(ast.NodeVisitor):
    def __init__(self, libs):   
        self.chaves = dict()
        self.classe = ""
        self.funcao = ""
        self.modules = set()
        self.libs_os = libs
        # self.libs_os.update(libs)
        self.chamadas = dict()
        
    def tratar_modulos(self, node, module):
        key = node.name
        if node.asname:
            key = node.asname
        # print(f'lib:{node.name}, as: {node.asname} -> key: {key}, module:{module}')   
        self.chamadas[key] = [module, node.name] # package_name -> [package, module]
    def visit_Import(self, node):
        for name in node.names:
            # print(f'{name.name} -> {name.asname}')
            # print(name.name)
            self.tratar_modulos(name, name.name.split(".")[0])
            self.modules.add(name.name.split(".")[0])
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module is not None and node.level == 0:
            # print(node.module)
            [self.tratar_modulos(nam, node.module.split(".")[0]) for nam in node.names ]    
            self.modules.add(node.module.split(".")[0])
        self.generic_visit(node) 

    # def visit_FunctionDef(self, node):
    #     self.funcao = node.name
    #     ast.NodeVisitor.generic_visit(self, node)    
                    
    # def visit_AsyncFunctionDef(self, node):
    #     self.funcao = node.name
    #     ast.NodeVisitor.generic_visit(self, node)           

    # def visit_ClassDef(self, node):
    #     self.classe = node.name
    #     ast.NodeVisitor.generic_visit(self, node)
        
    
    def visit_Name(self, node):
        # print(f'linha: { node.lineno}, visit_Name: {node.id} {node.__dict__}')
        # print(f'linha: { node.lineno}, visit_Name: {node.id}')
        if node.id and node.id in self.chamadas:
            module_temp = self.chamadas[node.id]
            if module_temp[0] in self.libs_os:
                print(f'linha: {node.lineno}, module: {module_temp}, package {node.id}')
                # print(f'linha: { node.lineno}, visit_Name: {node.id} {node.__dict__}')
        self.generic_visit(node) 
    
    def transform(self, context, node):
        # pass
        if isinstance(node, ast.Attribute): 
            print(f"classe:{self.classe}, func:{self.funcao}, linha: {node.lineno}, contexto: {context}, Attribute:  {node.value}, Attr: {node.attr}")
            self.transform("atributo", node.value)
        if isinstance(node, ast.Name):
            print(f'classe:{self.classe}, func:{self.funcao}, linha: {node.lineno}, contexto: {context}, Name:  {node.id}')  
            # if node.id and node.id in self.chamadas:
            #     module_temp = self.chamadas[node.id]
            #     if module_temp[0] in self.libs_os:
            #         print(f'linha: {node.lineno}, module: {module_temp}, package {node.id}')
        # if isinstance(parent, ast.Call):
        #     for arg in parent.args:
        #         self.transform("arg", arg, node)

    # def visit_ (self, node):
    def visit_Assign(self, node):
        self.transform("assign",node.value)
        self.generic_visit(node) 
        
    def visit_Call(self, node):
        function = node.func
        # print(f'Call  dicts: {node.__dict__}')
        self.transform("call",function)
        for arg in node.args:
            self.transform("arg", arg)
        for key in node.keywords: # todo: tratamento ao conditional/decorator
            self.transform("keys", key.arg)
        self.generic_visit(node) 
        
    def modules(self):
        return self.modules
    
    def print_chamadas(self):
        print('-'*30)
        for k in self.chamadas: 
            print(f'{k} -> {self.chamadas[k]}')
        print('-'*30)
        
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
        self.transform("if",node.test)
        if isinstance(node.test, ast.Attribute):
            self.parse_attr(node.test)
        if isinstance(node.test, ast.Compare):
            self.parse_compare(node.test)
        if isinstance(node.test, ast.Call):
            self.parse_call(node.test)
        ast.NodeVisitor.generic_visit(self, node)  
# modules = set()

if __name__ == '__main__':
    # python_file = "data/django/django/tests/asgi/tests.py"
    python_file = "input/sys-sample.py"
    # python_file = "input/import-sample.py"
    libs = set()
    libs.add('os')
    libs.add('platform')
    libs.add('sys')
        # libs.add('unittest')

    try:
        parser = ast.parse(open(python_file).read())
        monitor = CallVisitor(libs)
        monitor.visit(parser)
        if not monitor.modules: # continue
            print('no modules')
        else:
            print(', '.join(list(monitor.modules)))  # -> 'file_modules'
            if libs.intersection(monitor.modules): # verify file with modules -> 'file_modules_excludes'
                print(f'has modules: {len(monitor.modules)}') # -> 'file_modules_excludes'
            else:
                print('no modules') # -> 'file_modules_excludes'
        if 'test' in python_file: # verify file with test -> 'file_with_tests'
            print(f'has test: {python_file}')
        else:
            print('no test')
        
        monitor.print_chamadas()
    except SyntaxError as ex:
        print('erro', python_file) 
    