import ast
from pathlib import Path

from monitor import all_files
from writercsv import WriterCSV

DEBUG = False

class DecoratorVisitor(ast.NodeVisitor):
    def __init__(self, decorator):   
        self.decorator = decorator
        self.razions = []
        self.razion = dict()
        self.classe = ""
        self.funcao = ""
        # self.count = 0
    
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
        # print(f'def attribute: {attribute.attr}, {attribute.value}' )
        if not 'package' in self.razion:
            self.razion['package'] = attribute.attr
            # print(f'[p] - {self.razion}')

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
                self.debug(f'[p] call platform: {arg.value} ')
                # print(f'[r] razion: {self.razion}') #sys.platform.startswith("win")
                # print('---', self.razion)
                # self.razions.append(self.razion)
                # self.razion = dict()
        # pass
    # def parse_call(self, call):
    #     # print('call func: ', call.func)
    #     if isinstance(call.func, ast.Name):
    #         print('call func id: ', call.func.id)
    #     if isinstance(call.func, ast.Attribute):
    #         self.parse_attr(call.func)
    #     for arg in call.args:    
    #         if isinstance(arg, ast.Constant):
    #             print('call args: ', arg.value)

    # def parse_decorator(self, node):
    #     # d ('func', 'args', 'keywords')
        
    #     for d in node.decorator_list: 
    #         # print(self.count)
    #         # if isinstance(d, ast.Name):
    #         #     print('call func id: ', d.id)
    #         # if isinstance(d, ast.Attribute):
    #         #     print('att: ',d)
    #         # if isinstance(d, ast.Constant):
    #         #     print('Constant: ',d.value.id)
    #         if not isinstance(d, ast.Call):
    #             # print('Call continue func id: ', d.id)
    #             continue
    #         decoratorAtt = self.flatten_attr(d.func)
    #         if not decoratorAtt in self.decorator:
    #             continue
    #         self.count+=1
    #         # print(f'({self.count})[---decorator---] {d.keywords[0].value.value}')
    #         print(f'({self.count})[parse_decorator] razion args: {self.razion}')
    #         # node.lineno linha que define a funcão ou classe
    #         print(f'({self.count})Decorator: [ {decoratorAtt} ]linha: {node.lineno} - {node.name} ')#, ' ', self.razion)
    #         # @pytest.mark.skipif(condition, reason) If the condition evaluates to True during collection, 
    #         # the test function will be skipped, with the specified reason appearing in the summary when using -rs.
    #         # @pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python3.10 or higher")
    #         # print('[Function] ', node.name)
            
    #         for a in d.keywords:
    #             if isinstance(a.value, ast.Constant):
    #                 print(f'({self.count})[keywords] call args: ', a.value.lineno, ' - ', a.value.value, d)
    #                 self.razion['razion'] = a.value.value
    #                 print(f'({self.count})[reason] call args: ', self.razion)
    #                 # self.razions.append(self.razion)
    #                 # self.razion = dict()
    #                 # print(a.value.value)

    #         for arg in d.args:
    #             # _ast.UnaryOp
    #             # _ast.Call
    #             print(f'({self.count}) \targ: { arg} - {arg.lineno} ')
    #             self.razion['decorator'] = decoratorAtt
    #             # if isinstance(arg, ast.UnaryOp):
    #             #     self.parse_call(arg.operand)
    #             if isinstance(arg, ast.Call):
    #                 self.parse_call(arg)
    #             if isinstance(arg, ast.Compare):
    #                 self.parse_compare(arg)
    #             if isinstance(arg, ast.Constant):
    #                 # print('[ddd] call args: ', self.razion)
    #                 # print('[reason] call args: ', arg.value)
    #                 self.razion['razion'] = arg.value
    #                 self.razions.append(self.razion)
    #                 self.razion = dict()
    #         print(f'({self.count})[razion final] razion args: {self.razion}')

    def parse_decorator(self, node):
        
        for d in node.decorator_list:
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
            self.razions.append(self.razion)
            self.razion = dict()
            self.debug(f'')


    # FunctionDef(identifier name, arguments args,stmt* body, expr* decorator_list, expr? returns, string? type_comment)
    def visit_FunctionDef(self, node):
        # print('visit_FunctionDef', node.name)
        self.funcao = node.name
        # self.razion ['func_def'] = node.name
        self.parse_decorator(node)
        ast.NodeVisitor.generic_visit(self, node)    
                    
    # AsyncFunctionDef(identifier name, arguments args,stmt* body, expr* decorator_list, expr? returns,string? type_comment)
    def visit_AsyncFunctionDef(self, node):
        # print('visit_AsyncFunctionDef', node.name)
        self.funcao = node.name
        # self.razion ['func_def'] = node.name
        self.parse_decorator(node)
        ast.NodeVisitor.generic_visit(self, node)    

    # ClassDef(identifier name,expr* bases,keyword* keywords,stmt* body,expr* decorator_list)
    def visit_ClassDef(self, node):
        # print('visit_ClassDef', node.name)
        self.classe = node.name
        self.funcao = ""
        # self.razion ['class_def'] = node.name
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
            return visitor.razions


if __name__ == '__main__':
    heads = ['decorator','razion', 'module', 'package', 'platform', 'filename','func_def', 'class_def','project_name','project_hash']
    # libs_os =  dict()
    # libs_os['unittest'] = ['skipIf']
    # pacotes = []
    razions = []
    project_name = 'django'
    project_hash = '19867c612c898d3075a922e74db8e105adae89c6'
    files = 0 # temp, only conference
    project_dir = "data/django/django/tests/"
    # project_dir = "data/cdp-backend"
    # project_dir = "data/flask/tests"
    # python_file = "data/cdp-backend/cdp_backend/tests/pipeline/test_event_gather_pipeline.py"
    # project_dir = "input/"
    for python_file in all_files(project_dir):
        if python_file.is_dir(): continue
        try:
            # if 'test' in str(python_file): # verify file with test -> 'file_with_tests'
            #     # print(f'has test: {python_file}')
            #     pass
            # else:
            #     # print('no test')
            #     pass
            
            filename = str(python_file).replace(project_dir,"")
            # parser = ast.parse(open(python_file).read())
            # monitor = CallVisitor(libs_os, filename)
            # monitor.visit(parser)
            
            # reader = DecoratorReader(python_file, ['unittest.skipIf', 'skipIf'])
            # reader = DecoratorReader(python_file, ['unittest.skipIf']) #18 ok, 13 files
            # reader = DecoratorReader(python_file, 'skipIf') #23 ok, 12 files
            # reader = DecoratorReader(python_file, ['unittest.skipUnless']) #116 ok, 54 files
            # reader = DecoratorReader(python_file, ['skipUnless']) # #49 ok, 25 files
            # reader = DecoratorReader(python_file, ['unittest.skipUnless','skipUnless', 'unittest.skipIf', 'skipIf']) # #49 ok, 25 files
            # print(python_file)
            # reader = DecoratorReader(python_file, ['pytest.mark.skipif']) # 08 ok, 03 files
            # reader = DecoratorReader(python_file, ['mark.skipif']) # 00 ok, 00 files
            # reader = DecoratorReader(python_file, ['skipif']) # 00 ok, 00 files
            # reader = DecoratorReader(python_file, ['pytest.mark.xfail']) # 00 ok, 00 files
            # reader = DecoratorReader(python_file, ['mark.xfail']) # 00 ok, 00 files
            # reader = DecoratorReader(python_file, ['xfail']) # 00 ok, 00 files
            # reader = DecoratorReader(python_file, ['pytest.mark.skipif', 'mark.skipif', 'skipif', 'pytest.mark.xfail', 'mark.xfail' ,'xfail']) # 08 ok, 03 files
            reader = DecoratorReader(python_file, ['pytest.mark.skipif', 'mark.skipif', 'skipif', 'pytest.mark.xfail', 'mark.xfail' ,'xfail', 'unittest.skipUnless','skipUnless', 'unittest.skipIf', 'skipIf']) # 08 ok, 03 files
            all = reader.fetch()
            for row in all:
                if 'module' in row: #module (sys, os, platform) sem o module não importa
                    row['filename'] = filename
                    row['project_name'] = project_name
                    row['project_hash'] = project_hash
                    # razions.append(project_hash)
                    # razions.extend([row])
                    # razions.extend(row.values())
                    # razions.extend(list(row.values()))
                    # print(row.values())
                    row_temp = []    
                    # [row_temp.extend([v]) for v in row.values()]
                    for v in heads:
                        row_temp.extend([row[v]])
                        # print(f'v: {v} -> r: {row[v]}, l: {len(row_temp)}')
                    razions.append(row_temp)
                # else:
                #     print(f' {filename} -> {row}')    
            if all: 
                files = files + 1
        except SyntaxError as ex:
            print('erro', python_file) 
                    # self.package_os.append([node.lineno, mod[0], parent.attr,self.classe,self.funcao])
    
    # print(len(razions), ' - ', files)
    # for row in razions:
    # #     # if 'module' in row:
        # print(row)
    
    # heads = ['module','package', 'platform', 'razion', 'decorator', 'filename','project_name','project_hash']
    # heads = ['decorator','razion', 'module', 'package', 'platform', 'filename','project_name','project_hash']
    # heads = ['decorator','razion', 'module', 'package', 'platform', 'filename']
    
    writer = WriterCSV(name="razions_django", path="analysis")
    writer.write(head=heads, rows=razions) 

    