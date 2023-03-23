import ast
from pathlib import Path

from monitor import all_files
from writercsv import WriterCSV

DEBUG = True
# DEBUG = False

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
        
    def flatten_attr(self, node):
        if isinstance(node, ast.Attribute):
            return str(self.flatten_attr(node.value)) + '.' + node.attr
        elif isinstance(node, ast.Name):
            return str(node.id)
        else:
            pass    
    def debug(self, msg):
        if DEBUG:
            print(f'[debug] {self.classe} - {self.funcao}: {msg}')
    # Attribute(expr value, identifier attr, expr_context ctx)
    def parse_attr(self, attribute):
        # if isinstance(attribute, ast.Name):
        #     print('NAME: ', attribute.id)
        if isinstance(attribute.value, ast.Attribute):
            # print('value Attribute: ', attribute.value)
            # print('modules: ', self.parse_attr(attribute.value))
            self.parse_attr(attribute.value)
            # self.razion['module'] = valor
        if isinstance(attribute.value, ast.Name):
            # print('value attribute id: ', attribute.value.id)
            self.razion['module'] = attribute.value.id
            self.razion['line'] = attribute.lineno

            # print(f'def attribute: {attribute.attr}, {attribute.value} {attribute}' )
        if not 'package' in self.razion:
            self.razion['package'] = attribute.attr
            # print(f'[p] - {self.razion}')
        self.atts.append(attribute)
    # Compare(expr left, cmpop* ops, expr* comparators)
    def parse_compare(self, compare):
        self.debug(f'[compare] {compare.comparators}, left: {compare.left}')
        if isinstance(compare.left, ast.Attribute):
            self.parse_attr(compare.left)
        # if isinstance(compare.left, ast.Name):
        #     print('left compare: ', compare.left.id)
            # pass
        for comparator in compare.comparators:    
            if isinstance(comparator, ast.Constant):
                self.debug(f'comparators compare: {comparator.value}')
                self.razion['platform'] = comparator.value
                self.platform = comparator.value
        self.debug(comparator.ops)
    # Call(expr func, expr* args, keyword* keywords)
    def parse_call(self, node):
        self.debug(f'[c] {node.func}')    
        # print(f'[c] - {node.func.value.value.id} , {node.keywords}, {node.lineno}')
        if isinstance(node.func, ast.Attribute):
            self.parse_attr(node.func)
        # self.parse_attr(node.func)
        for arg in node.args:    
            # if isinstance(arg, ast.Compare):
            #     print('oiiiiaaa')
            if isinstance(arg, ast.Constant):
                self.razion['platform'] = arg.value
                self.platform = arg.value
                self.debug(f'[p] call platform: {arg.value} ')

    def parse_decorator(self, node):
        
        for d in node.decorator_list:
            # self.debug(f'[decor] {d}')
            if not isinstance(d, ast.Call):
                continue
            decoratorAtt = self.flatten_attr(d.func)
            if not decoratorAtt in self.decorator:
                continue
            # self.count+=1
            # print(f'({self.count})Decorator: [ {decoratorAtt} ]linha: {node.lineno} - {node.name} ')#, ' ', self.razion)
            self.debug(f'[d]: {decoratorAtt}, func line: {node.lineno}, func name: {node.name} , (d): {d}')
            self.razion = dict()
            self.razion['decorator'] = decoratorAtt
            for a in d.keywords:
                if isinstance(a.value, ast.Constant):
                    self.debug(f'[k] line: {a.value.lineno}, val: {a.value.value}, arg: {a.arg}')
                    if 'reason' == a.arg:
                        self.razion['razion'] = a.value.value
                        self.razion['line'] = a.value.lineno

                    # arg: {a.arg} ,value: {a.value}, type: {a} 
            
            for arg in d.args:
                # print(f'ARGS: {arg}')
                if isinstance(arg, ast.Call):
                    self.parse_call(arg)
                if isinstance(arg, ast.Compare):
                    self.parse_compare(arg)
                if isinstance(arg, ast.Constant): # when not definier a reason at annotation
                    self.razion['razion'] = arg.value
                #     print(f'[a]{arg.value}')
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
                    self.razions.append(self.razion)
                    
                    # print(f'{mod}.{pack} -> {lib_and_module}')
                    
            self.razion = dict()
            self.debug(f'')
                     
    def tratar_modulos(self, node, module, package):
        key = node.name
        if node.asname:
            key = node.asname
        # print(f'package:{node.name}, as: {node.asname} -> key: {key}, module:{module}')   
        # print(f'module:{module}, package: {node.name}, name: {key}')   
        self.chamadas[key] = [module, package] # package_name -> [package, module]
        # print(f'module:{module}, package: {package}, name: {key}, cham: {self.chamadas}')   
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

# FunctionDef(identifier name, arguments args,stmt* body, expr* decorator_list, expr? returns, string? type_comment)
    def visit_FunctionDef(self, node):
        # print('visit_FunctionDef', node.name)
        self.funcao = node.name
        # self.razion ['func_def'] = node.name
        self.parse_decorator(node)
        self.generic_visit(node)                    
        
    # AsyncFunctionDef(identifier name, arguments args,stmt* body, expr* decorator_list, expr? returns,string? type_comment)
    def visit_AsyncFunctionDef(self, node):
        # print('visit_AsyncFunctionDef', node.name)
        self.funcao = node.name
        # self.razion ['func_def'] = node.name
        self.parse_decorator(node)
        self.generic_visit(node)    

    # ClassDef(identifier name,expr* bases,keyword* keywords,stmt* body,expr* decorator_list)
    def visit_ClassDef(self, node):
        # print('visit_ClassDef', node.name)
        self.classe = node.name
        self.funcao = ""
        # self.razion ['class_def'] = node.name
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

# BoolOp(boolop op, expr* values)
# UnaryOp(unaryop op, expr operand)        
    
    def visit_Attribute(self, node):
        # print(f"file:{self.filename}, func:{self.funcao}, linha: {node.lineno}, contexto: att, Attribute:  {node._attributes}, Attr: {node.attr}")
        # print(node.lineno, ' ', node.value.__class__)
        att = node.value
        # self.p = node
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
        if isinstance(att, ast.UnaryOp):    
            # print(f"linha: {node.lineno}, module: CALL, call: {node.attr}, att: {att.func}")
            self.tratar_unary(att)
        
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
                    if (parent.attr in self.libs_os[mod[0]] or len(self.libs_os[mod[0]])==0) and (self.p):
                        if isinstance(self.p, ast.Compare):
                            for comparator in self.p.comparators:    
                                if isinstance(comparator, ast.Constant):
                                    self.platform = comparator.value
                                    # print(f'plat: {self.platform} - compare')
                            self.debug(f'ops: {self.p.ops} ea: {ast.Eq}')
                        if isinstance(self.p, ast.If):
                            # print(f'{self.p.test} - {self.p.}')
                            # for comparator in self.p.test.comparators:    
                            #     if isinstance(comparator, ast.Constant):
                            #         self.platform = comparator.value
                            #         print(f'plat: {self.platform} -if')
                            if isinstance(self.p.test, ast.Call):
                                for arg in self.p.test.args:    
                                    if isinstance(arg, ast.Constant):
                                        self.platform = arg.value
                        #                 print(f'plat: {self.platform} - call')
                            if isinstance(self.p.test, ast.UnaryOp):
                                self.tratar_unary(self.p.test)
                        self.debug(f"  linha: {node.lineno}, module: {mod[0]}, call: {parent.attr} -- Name, classe:{self.filename}, func:{self.funcao}, p: {self.p} plat: {self.platform}")
                        self.debug(f'atributo: {parent} -> {parent in self.atts}')
                        if not parent in self.atts:
                            self.package_os.append([self.project_name, self.project_hash, node.lineno, mod[0], parent.attr, self.platform, self.filename,self.funcao])
                            self.p = None
                            self.platform = ''
    def tratar_unary(self, node):
        if not isinstance(node, ast.UnaryOp): return
        
        print(f'op: {node.op} operand: {node.operand}')
        
    def modules(self):
        return self.modules
    