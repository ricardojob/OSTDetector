import ast
from pathlib import Path

from monitor import all_files
from writercsv import WriterCSV

# DEBUG = True
DEBUG = False

class CallVisitor(ast.NodeVisitor):         
       # if e compare
    def __init__(self, libs, project_name, project_hash, file, decorator):   
        self.project_name = project_name
        self.project_hash = project_hash
        self.filename = file
        self.libs_os = libs
        self.chaves = dict()
        self.funcao = ""
        self.modules = set()
        # self.libs_os.update(libs)
        self.chamadas = dict()
        self.package_os = []
        self.p=None   
        self.decorator = decorator
        self.razions = []
        self.razion = dict()
        self.classe = ""
        self.atts = []
        self.platform = ''
        self.compare_temp = []
        
    def visit_Import(self, node):
        for name in node.names:
            module = name.name.split(".")[0]
            self.tratar_modulos(name, module, None)
            if module in self.libs_os:
                self.modules.add(module)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module is not None and node.level == 0:
            module = node.module.split(".")[0]
            [self.tratar_modulos(nam, module, nam.name) for nam in node.names ]    
            if module in self.libs_os:
                self.modules.add(module)
        self.generic_visit(node) 

    # FunctionDef(identifier name, arguments args,stmt* body, expr* decorator_list, expr? returns, string? type_comment)
    def visit_FunctionDef(self, node):
        self.funcao = node.name
        self.parse_decorator(node)
        self.generic_visit(node)                    
        
    # AsyncFunctionDef(identifier name, arguments args,stmt* body, expr* decorator_list, expr? returns,string? type_comment)
    def visit_AsyncFunctionDef(self, node):
        self.funcao = node.name
        self.parse_decorator(node)
        self.generic_visit(node)    

    # ClassDef(identifier name,expr* bases,keyword* keywords,stmt* body,expr* decorator_list)
    def visit_ClassDef(self, node):
        self.classe = node.name
        self.funcao = ""
        self.parse_decorator(node)
        self.generic_visit(node)
           
    def visit_Compare(self, node):
        self.p = node
        self.generic_visit(node)
        self.p = None
    
    def visit_If(self, node):
        self.p = node
        self.generic_visit(node)
        self.p = None
    
    def visit_Attribute(self, node):
        att = node.value
        if isinstance(att, ast.Name):
            self.tratar_Name(att, node)
        self.generic_visit(node)
        
    def flatten_attr(self, node):
        if isinstance(node, ast.Attribute):
            return str(self.flatten_attr(node.value)) + '.' + node.attr
        elif isinstance(node, ast.Name):
            return str(node.id)
        else:
            pass    
    
    # Attribute(expr value, identifier attr, expr_context ctx)
    def parse_attr(self, attribute):
        if isinstance(attribute.value, ast.Attribute):
            self.parse_attr(attribute.value)
        if isinstance(attribute.value, ast.Name):
            self.razion['module'] = attribute.value.id
            self.razion['line'] = attribute.lineno
            self.razion['url'] = self.gerar_url(attribute.lineno)
            
        if not 'package' in self.razion:
            self.razion['package'] = attribute.attr
        self.atts.append(attribute)
    
    # Compare(expr left, cmpop* ops, expr* comparators)
    def parse_compare(self, compare):
        self.debug(f'[compare] {compare.comparators}, left: {compare.left}')
        if isinstance(compare.left, ast.Attribute):
            self.parse_attr(compare.left)

        for comparator in compare.comparators:    
            if isinstance(comparator, ast.Constant):
                self.debug(f'comparators compare: {comparator.value}')
                self.razion['platform'] = comparator.value
                self.platform = comparator.value
            if isinstance(comparator, ast.Tuple):
                self.compare_temp = comparator.elts
            if isinstance(comparator, ast.List):
                self.compare_temp = comparator.elts
                # pass    
    # Call(expr func, expr* args, keyword* keywords)
    def parse_call(self, node):
        self.debug(f'[c] {node.func}')    
        # self.debug(f'[c] - {node.func.value.value.id} , {node.keywords}, {node.lineno}')
        if isinstance(node.func, ast.Attribute):
            self.parse_attr(node.func)
        for arg in node.args:    
            if isinstance(arg, ast.Constant):
                self.razion['platform'] = arg.value
                self.platform = arg.value
                self.debug(f'[p] call platform: {arg.value} ')

    def parse_decorator(self, node):
        
        for d in node.decorator_list:
            if not isinstance(d, ast.Call):
                continue
            decoratorAtt = self.flatten_attr(d.func)
            if not decoratorAtt in self.decorator:
                continue
            self.debug(f'[d]: {decoratorAtt}, func line: {node.lineno}, func name: {node.name} , (d): {d}')
            self.razion = dict()
            self.razion['decorator'] = decoratorAtt
            for a in d.keywords:
                if isinstance(a.value, ast.Constant):
                    self.debug(f'[k] line: {a.value.lineno}, val: {a.value.value}, arg: {a.arg}')
                    if 'reason' == a.arg:
                        self.razion['razion'] = a.value.value
                        self.razion['line'] = a.value.lineno
                        self.razion['url'] = self.gerar_url(a.value.lineno)
            for arg in d.args:
                if isinstance(arg, ast.Call):
                    self.parse_call(arg)
                if isinstance(arg, ast.Compare):
                    self.parse_compare(arg)
                if isinstance(arg, ast.Constant): # when not definier a reason at annotation
                    self.razion['razion'] = arg.value
            self.debug(f'[r] razion: {self.razion}')
            self.razion ['func_def'] = self.funcao
            self.razion ['class_def'] = self.classe
            if 'module' in self.razion:
                pack = self.razion ['package']
                mod = self.razion ['module']
                lib_and_module = any(pack in item for item in self.libs_os.values()) and (mod in self.libs_os)
                if lib_and_module:
                    self.razion['filename'] = self.filename
                    self.razion['project_name'] = self.project_name
                    self.razion['project_hash'] = self.project_hash
                    
                    if(len(self.compare_temp)>0): # sys.platform not in ("linux", "darwin")
                        for plat in self.compare_temp:
                            temp = self.razion.copy()
                            temp['platform'] = plat.value
                            self.razions.append(temp)
                        self.compare_temp = []
                    else:
                        self.razions.append(self.razion)        
                    
            self.razion = dict()
            self.compare_temp = []
            self.debug(f'')
            

    def tratar_modulos(self, node, module, package):
        key = node.name
        if node.asname:
            key = node.asname
        self.debug(f'package:{node.name}, as: {node.asname} -> key: {key}, module:{module}')   
        self.chamadas[key] = [module, package] # package_name -> [package, module]
        self.debug(f'module:{module}, package: {package}, name: {key}, cham: {self.chamadas}')   
    
    def tratar_call_plaftorm(self, call):
        if isinstance(call, ast.Call):
            for arg in call.args:    
                if isinstance(arg, ast.Constant):
                    self.platform = arg.value
                if isinstance(arg, ast.Tuple):
                    self.compare_temp = arg.elts
                if isinstance(arg, ast.List):
                    self.compare_temp = arg.elts
        pass    
    def tratar_Name(self, node, parent):
        if isinstance(node, ast.Name):
            if node.id and node.id in self.chamadas:
                mod = self.chamadas[node.id]

                if mod[0] in self.libs_os:
                #     # print(f'\tlinha: {node.lineno}, module: {mod[0]}, package {node.id}')        
                    if (parent.attr in self.libs_os[mod[0]] or len(self.libs_os[mod[0]])==0) and (self.p):
                        if isinstance(self.p, ast.Compare):
                            for comparator in self.p.comparators:    
                                if isinstance(comparator, ast.Constant):
                                    self.platform = comparator.value
                                if isinstance(comparator, ast.Tuple):
                                    self.compare_temp = comparator.elts
                                if isinstance(comparator, ast.List):
                                    self.compare_temp = comparator.elts    
                        if isinstance(self.p, ast.If):
                            if isinstance(self.p.test, ast.Call):
                                self.tratar_call_plaftorm(self.p.test)
                                # for arg in self.p.test.args:    
                                #     if isinstance(arg, ast.Constant):
                                #         self.platform = arg.value
                                #     if isinstance(arg, ast.Tuple):
                                #         self.compare_temp = arg.elts
                                #     if isinstance(arg, ast.List):
                                #         self.compare_temp = arg.elts    
                            if isinstance(self.p.test, ast.UnaryOp):
                                self.tratar_call_plaftorm(self.p.test.operand)
                                                  
                        self.debug(f"  linha: {node.lineno}, module: {mod[0]}, call: {parent.attr} -- Name, classe:{self.filename}, func:{self.funcao}, p: {self.p} plat: {self.platform}")
                        self.debug(f'atributo: {parent} -> {parent in self.atts}')
                        self.debug(f'- compare_temp: {self.compare_temp}')
                        if not parent in self.atts:
                            url = self.gerar_url(node.lineno)
                            method_type = self.gerar_tipo_metodo()
                            
                            if(len(self.compare_temp)>0): # sys.platform not in ("linux", "darwin")
                                for plat in self.compare_temp:
                                    self.package_os.append([self.project_name, self.project_hash, node.lineno, mod[0], 
                                                    parent.attr, plat.value, self.filename,self.funcao, 
                                                    method_type, url])
                                    # temp = self.razion.copy()
                                    # temp['platform'] = plat.value
                                    # self.razions.append(temp)
                                self.compare_temp = []
                            else:
                                self.package_os.append([self.project_name, self.project_hash, node.lineno, mod[0], 
                                                    parent.attr, self.platform, self.filename,self.funcao, 
                                                    method_type, url])
                                
                            
                            # self.package_os.append([self.project_name, self.project_hash, node.lineno, mod[0], 
                            #                         parent.attr, self.platform, self.filename,self.funcao, 
                            #                         method_type, url])
                            
                          
                            self.p = None
                            self.platform = ''
                            self.compare_temp = []
    def gerar_url(self, line):
          # https://github.com/ansible/ansible/blob/4ea50cef23c3dc941b2e8dc507f37a962af6e2c8
          # /test/support/integration/plugins/modules/timezone.py#L107
          return f'https://github.com/{self.project_name}/blob/{self.project_hash}{self.filename}#L{line}'  
    
    def gerar_tipo_metodo(self):
        method_type = 'support'
        if self.funcao.startswith("setUp") or self.funcao.startswith("tearDown"):
            method_type = 'configuration'
        elif self.funcao.startswith("test_"):
            method_type = 'method_test'    
        return method_type
        # print(f'{method_type} -> {row}')
        
    def debug(self, msg):
        if DEBUG:
            print(f'[debug] {self.classe} - {self.funcao}: {msg}')
            
    def modules(self):
        return self.modules
    
if __name__ == '__main__':
      
    libs_os =  dict()
    libs_os['sys'] = [ 'platform', 'getwindowsversion']
    libs_os['os'] = ['name', 'supports_bytes_environ', 'name']
    libs_os['platform'] = ['platform', 'system', 'version', 'uname','win32_edition','win32_ver','win32_is_iot','mac_ver','libc_ver', 'freedesktop_os_release']
    pacotes = []
    project_dir = "data1/salt"
    project_name = "saltstack/salt"
    decorators = ['pytest.mark.skipif', 'mark.skipif', 'skipif', 'pytest.mark.xfail', 'mark.xfail' ,'xfail', 'unittest.skipUnless','skipUnless', 'unittest.skipIf', 'skipIf']

    for python_file in all_files(project_dir):
        if python_file.is_dir(): continue
        filename = str(python_file).replace(project_dir,"")
        try:
            parser = ast.parse(open(python_file).read())
            monitor = CallVisitor(libs_os, project_name,"0b73c8008577eddba7ea8549e6f4fdc4ccba436d", filename,decorators)
            monitor.visit(parser)

            if len(monitor.package_os) > 0:
                pacotes.extend(monitor.package_os)
                print(10*'---', f'LISTANDO os packs: {filename}')
                for row in monitor.package_os:
                    print(f'{row[2]} -> {row[3]}.{row[4]}-{row[5]}')
                #     print(row)
            # if len(monitor.razions) > 0:
            #     print(10*'---', f'LISTANDO os razions: {filename}')
            #     for row in monitor.razions:
            #         print(f'{row["line"]}->{row["module"]}.{row["package"]} - {row["platform"]} {row["razion"]}')
                    # print(row)
        except SyntaxError as ex:
            print('erro', python_file) 
    # heads = ['linhas', 'module', 'package', 'file', 'function']
    # writer = WriterCSV(name=f'packages_os_{project_name.replace("/","_")}', path="analysis")
    # writer.write(head=heads, rows=pacotes) 
    