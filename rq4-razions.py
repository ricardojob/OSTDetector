import ast
from pathlib import Path

from monitor import all_files
from writercsv import WriterCSV

class DecoratorVisitor(ast.NodeVisitor):
    def __init__(self, decorator):   
        self.decorator = decorator
        self.razions = []
        self.razion = dict()
    
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
            # print('value attribute: ', attribute.value.id)
            self.razion['module'] = attribute.value.id
        if isinstance(attribute.value, ast.Attribute):
            self.parse_attr(attribute.value)
        # print('name attribute: ', attribute.attr)
        self.razion['package'] = attribute.attr

    # Compare(expr left, cmpop* ops, expr* comparators)
    def parse_compare(self, compare):
        if isinstance(compare.left, ast.Attribute):
            self.parse_attr(compare.left)
        if isinstance(compare.left, ast.Name):
            # print('left compare: ', compare.left.id)
            pass
        for comparator in compare.comparators:    
            if isinstance(comparator, ast.Constant):
                # print('comparators compare: ', comparator.value)
                self.razion['platform'] = comparator.value
                
    
    def parse_decorator(self, node):
        # d ('func', 'args', 'keywords')
        for d in node.decorator_list: 
            if not isinstance(d, ast.Call):
                continue
            decoratorAtt = self.flatten_attr(d.func)
            if not decoratorAtt in self.decorator:
                continue
            # print('Decorator: ', decoratorAtt)
            # @unittest.skipIf(condition, reason) Skip the decorated test if condition is true.   
            # @unittest.skipIf(sys.platform == 'win32', "Windows select() doesn't support file descriptors.")
            # print('[Function] ', node.name)
            for arg in d.args:
                if isinstance(arg, ast.Compare):
                    self.parse_compare(arg)
                if isinstance(arg, ast.Constant):
                    # print('[reason] call args: ', arg.value)
                    self.razion['razion'] = arg.value
                    self.razion['decorator'] = decoratorAtt
                    self.razions.append(self.razion)
                    self.razion = dict()

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
            return visitor.razions


if __name__ == '__main__':
    # libs_os =  dict()
    # libs_os['unittest'] = ['skipIf']
    # pacotes = []
    razions = []
    files = 0 # temp, only conference
    # project_dir = "data/django/django/tests/"
    project_dir = "data/cdp-backend"
    # project_dir = "input/"
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
            # parser = ast.parse(open(python_file).read())
            # monitor = CallVisitor(libs_os, filename)
            # monitor.visit(parser)
            
            # reader = DecoratorReader(python_file, ['unittest.skipIf', 'skipIf'])
            # reader = DecoratorReader(python_file, ['unittest.skipIf']) #18 ok, 13 files
            # reader = DecoratorReader(python_file, 'skipIf') #23 ok, 12 files
            # reader = DecoratorReader(python_file, ['unittest.skipUnless']) #116 ok, 54 files
            # reader = DecoratorReader(python_file, ['skipUnless']) # #49 ok, 25 files
            # reader = DecoratorReader(python_file, ['unittest.skipUnless','skipUnless', 'unittest.skipIf', 'skipIf']) # #49 ok, 25 files
            print(python_file)
            reader = DecoratorReader(python_file, ['pytest.mark.skipif'])
            all = reader.fetch()
            for row in all:
                if 'module' in row: #module (sys, os, platform) sem o module não importa
                    row['filename'] = filename
                    # razions.extend([row])
                    # razions.extend(row.values())
                    # razions.extend(list(row.values()))
                    # print(row.values())
                    row_temp = []    
                    [row_temp.extend([v]) for v in row.values()]
                    razions.append(row_temp)
            if all: 
                files = files + 1
        except SyntaxError as ex:
            print('erro', python_file) 
                    # self.package_os.append([node.lineno, mod[0], parent.attr,self.classe,self.funcao])
    # print(len(razions))
    print(len(razions), ' - ', files)
    # for row in razions:
    #     # if 'module' in row:
        # print(row)
    # heads = ['module','package', 'platform', 'razion', 'decorator', 'filename']
    # writer = WriterCSV(name="razions", path="analysis")
    # writer.write(head=heads, rows=razions) 

    