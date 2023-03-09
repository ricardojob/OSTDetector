import ast
from pathlib import Path

from monitor import all_files
from writercsv import WriterCSV


class CallVisitor(ast.NodeVisitor):
    def __init__(self, libs, file):   
        self.chaves = dict()
        self.classe = file
        self.funcao = ""
        self.modules = set()
        self.libs_os = libs
        # self.libs_os.update(libs)
        self.chamadas = dict()
        self.package_os = []
        
    def tratar_modulos(self, node, module, package):
        key = node.name
        if node.asname:
            key = node.asname
        # print(f'package:{node.name}, as: {node.asname} -> key: {key}, module:{module}')   
        # print(f'module:{module}, package: {node.name}, name: {key}')   
        self.chamadas[key] = [module, package] # package_name -> [package, module]
        # print(f'module:{module}, package: {package}, name: {key}')   
    def visit_Import(self, node):
        # print(f'imprts: {node.names[0].name}')
        for name in node.names:
            # print(f'{name.name} -> {name.asname}')
            # self.tratar_modulos(name, name.name.split(".")[0])
            module = name.name.split(".")[0]
            # key = module
            # if name.asname:
            #     key = name.asname
            # self.chamadas[key] = [module, None] # package_name -> [package, module]
            # print(f'module:{module}, package: {None}, name: {key}')    
            self.tratar_modulos(name, module, None)
            self.modules.add(name.name.split(".")[0])
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module is not None and node.level == 0:
            module = node.module.split(".")[0]
            [self.tratar_modulos(nam, module, nam.name) for nam in node.names ]    
            self.modules.add(module)
        self.generic_visit(node) 

    def visit_FunctionDef(self, node):
        self.funcao = node.name
        self.generic_visit(node)
                    
    def visit_AsyncFunctionDef(self, node):
        self.funcao = node.name
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # self.classe = node.name
        # ast.NodeVisitor.generic_visit(self, node)
        self.funcao = ''
        self.generic_visit(node)
    
    # def visit_Name(self, node):
    #     # print(f'linha: { node.lineno}, visit_Name: {node.id} {node.__dict__}')
    #     # print(f'linha: { node.lineno}, visit_Name: {node.id}')
    #     if node.id and node.id in self.chamadas:
    #         module_temp = self.chamadas[node.id]
    #         # if module_temp[0] in self.libs_os:
    #         #     print(f'linha: {node.lineno}, package {node.id}, module: {module_temp}')
    #             # print(f'linha: { node.lineno}, visit_Name: {node.id} {node.__dict__}')
    #     self.generic_visit(node) 
    
    def transform(self, context, node):
        pass
        # if isinstance(node, ast.Attribute): 
        #     print(f"classe:{self.classe}, func:{self.funcao}, linha: {node.lineno}, contexto: {context}, Attribute:  {node.value.id}, Attr: {node.attr}")
        #     # self.transform(context, node.value)
        # if isinstance(node, ast.Name):
        #     print(f'classe:{self.classe}, func:{self.funcao}, linha: {node.lineno}, contexto: {context}, Name:  {node.id}')  
        #     if node.id and node.id in self.chamadas:
        #         module_temp = self.chamadas[node.id]
        #         if module_temp[0] in self.libs_os:
        #             print(f'linha: {node.lineno}, module: {module_temp}, package {node.id}')
        # if isinstance(parent, ast.Call):
        #     for arg in parent.args:
        #         self.transform("arg", arg, node)
    def visit_Load(self, node):
        # print(node, ' ', node)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # print(f"classe:{self.classe}, func:{self.funcao}, linha: {node.lineno}, contexto: att, Attribute:  {node.value.id}, Attr: {node.attr}")
        # print(node.lineno, ' ', node.value.__class__)
        att = node.value
        if isinstance(att, ast.Name):
            # print(node.lineno, ' ', att.id)
            self.tratar_Name(att, node)
            # mod = self.chamadas[att.id]
            # print(f"linha: {node.lineno}, module: {mod[0]}, call: {node.attr}")
            # if att.id and att.id in self.chamadas:
            #     module_temp = self.chamadas[att.id]
            #     if module_temp[0] in self.libs_os:
            #         print(f'\tlinha: {att.lineno}, module: {module_temp}, package {att.id}')
        
        if isinstance(att, ast.Call):    
            # print(f"linha: {node.lineno}, module: CALL, call: {node.attr}, att: {att.func}")
            pass
        
        self.generic_visit(node)
        
    def tratar_Name(self, node, parent):
        if isinstance(node, ast.Name):
            # print(node.__dict__)
            if node.id and node.id in self.chamadas:
                mod = self.chamadas[node.id]
                # print(f"linha: {node.lineno}, module: {mod[0]}, call: {parent.attr}")
                # module_temp = self.chamadas[node.id]
                if mod[0] in self.libs_os:
                #     # print(f'\tlinha: {node.lineno}, module: {mod[0]}, package {node.id}')        
                    if parent.attr in self.libs_os[mod[0]] or len(self.libs_os[mod[0]])==0:
                        print(f"  linha: {node.lineno}, module: {mod[0]}, call: {parent.attr} -- Name, classe:{self.classe}, func:{self.funcao}")
                        self.package_os.append([node.lineno, mod[0], parent.attr,self.classe,self.funcao])
    
    def visit_Assign(self, node):
        parent = node.value
        if isinstance(parent, ast.Attribute):
            package = parent.value
            if isinstance(package, ast.Name):
                if package.id and package.id in self.chamadas: 
                    # print(package.id, '->', package.lineno)
                    module_temp = self.chamadas[package.id]
                    # mod = self.chamadas[att.id]
                    # print(f"linha: {node.value.lineno}, module: {module_temp[0]}, package: {node.value.attr}")
                    if module_temp[0] in self.libs_os:
                        targets = node.targets[0]
                        def tratar_pacotes(target):
                            if parent.attr in self.libs_os[module_temp[0]]:
                                self.chamadas[target.id] = [module_temp[0], parent.attr] # package_name -> [package, module]
                                print(f"  linha: {package.lineno}, module: {module_temp[0]}, call: {parent.attr} -- Assign, classe:{self.classe}, func:{self.funcao}")
                                self.package_os.append([package.lineno, module_temp[0], parent.attr,self.classe,self.funcao])
                        # print(target.__class__)
                        if isinstance(targets, ast.Attribute):
                            if targets.value:
                                tratar_pacotes(targets.value)
                        if isinstance(targets, ast.Name):
                            if targets:
                                tratar_pacotes(targets)
            # if isinstance(att, ast.Call):    
            #     print(f"linha: {node.value.lineno}, module: CALL, call: {node.value.attr}, att: {att}")
        # print('-'*30)
        self.generic_visit(node) 
        
    # def visit_Call(self, node):
    #     function = node.func
    #     # print(f'Call  dicts: {node.__dict__}')
    #     self.transform("call",function)
    #     for arg in node.args:
    #         self.transform("arg", arg)
    #     for key in node.keywords: # todo: tratamento ao conditional/decorator
    #         self.transform("keys", key.arg)
    #     self.generic_visit(node) 
        
    def modules(self):
        return self.modules
    
    def print_chamadas(self):
        print('-'*30)
        for k in self.chamadas: 
            print(f'{k} -> {self.chamadas[k]}')
        print('-'*30)
    def print_modules(self):
        print('='*30)
        print(', '.join(list(self.modules)))  # -> 'file_modules'    
        print('='*30)

    # count = 0
    
    # # Attribute(expr value, identifier attr, expr_context ctx)
    # def parse_attr(self, attribute):
    #     if isinstance(attribute.value, ast.Name):
    #         print('value attribute: ', attribute.value.id)
    #     if isinstance(attribute.value, ast.Attribute):
    #         self.parse_attr(attribute.value)
    #     print('name attribute: ', attribute.attr)

    # # Compare(expr left, cmpop* ops, expr* comparators)
    # def parse_compare(self, compare):
    #     if isinstance(compare.left, ast.Name):
    #         print('left compare: ', compare.left.id)
    #     for comparator in compare.comparators:    
    #         if isinstance(comparator, ast.Constant):
    #             print('comparators compare: ', comparator.value)            
    
    # # Call(expr func, expr* args, keyword* keywords)
    # def parse_call(self, call):
    #     # print('call func: ', call.func)
    #     if isinstance(call.func, ast.Name):
    #         print('call func id: ', call.func.id)
    #     if isinstance(call.func, ast.Attribute):
    #         self.parse_attr(call.func)
    #     for arg in call.args:    
    #         if isinstance(arg, ast.Constant):
    #             print('call args: ', arg.value)

    # def visit_If(self, node):
    #     self.count+=1
    #     self.transform("if",node.test)
    #     if isinstance(node.test, ast.Attribute):
    #         self.parse_attr(node.test)
    #     if isinstance(node.test, ast.Compare):
    #         self.parse_compare(node.test)
    #     if isinstance(node.test, ast.Call):
    #         self.parse_call(node.test)
    #     ast.NodeVisitor.generic_visit(self, node)  
# modules = set()

if __name__ == '__main__':
    # python_file = "data/django/django/tests/asgi/tests.py"
    # python_file = "data/django/django/tests/migrations/test_writer.py"
    # python_file = "data/django/django/tests/shell/tests.py"
    # python_file = "data/django/django/tests/admin_filters/tests.py"
    # python_file = "data/django/django/tests/template_tests/test_loaders.py"
    # python_file = "input/sys-sample.py"
    # python_file = "input/import-sample.py"
    # python_file = "data/django/django/tests/mail/tests.py"
    
    # libs = set()
    # libs.add('os')
    # libs.add('platform')
    # libs.add('sys')
    # libs_os =  dict()
    # libs_os['os'] = ['path', 'listdir']
    # libs_os['platform'] = ['machine', 'system']
    # libs_os['sys'] = ['path', 'platform']
    
    libs_os =  dict()
    # libs_os['platform'] = ['machine', 'system']
    # libs_os['os'] = ['path', 'listdir']
    # libs_os['os'] = []
    # libs_os['platform'] = []
    libs_os['sys'] = [ 'platform']
    # libs_os['sys'] = []
        # libs.add('unittest')
    pacotes = []
    # project_dir = "input"
    project_dir = "data/django/django/tests/"
    for python_file in all_files(project_dir):
        if python_file.is_dir(): continue
        try:
            if 'test' in str(python_file): # verify file with test -> 'file_with_tests'
                # print(f'has test: {python_file}')
                pass
            else:
                # print('no test')
                pass
            filename = str(python_file).replace(project_dir,"")
            parser = ast.parse(open(python_file).read())
            monitor = CallVisitor(libs_os, filename)
            monitor.visit(parser)
            if not monitor.modules: # continue
                # print('no modules')
                pass
            else:
                # print(', '.join(list(monitor.modules)))  # -> 'file_modules'
                # monitor.print_modules()
                if set(libs_os.keys()).intersection(monitor.modules): # verify file with modules -> 'file_modules_excludes'
                    # print(f'has modules: {len(monitor.modules)}') # -> 'file_modules_excludes'
                    pass
                else:
                    # print('no modules') # -> 'file_modules_excludes'
                    pass
            # file_list.append(str(filename))
            # monitor.print_chamadas()
            if len(monitor.package_os) > 0:
                pacotes.extend(monitor.package_os)
        except SyntaxError as ex:
            print('erro', python_file) 
                    # self.package_os.append([node.lineno, mod[0], parent.attr,self.classe,self.funcao])
    heads = ['linhas', 'module', 'package', 'file', 'function']
    writer = WriterCSV(name="packages_os", path="analysis")
    writer.write(head=heads, rows=pacotes) 