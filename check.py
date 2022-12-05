# Verifying the use of lib in python source code

def with_ast(file_name):
    import ast
    modules = set()
    def visit_Import(node):
        for name in node.names:
            modules.add(name.name.split(".")[0])
    def visit_ImportFrom(node):
        # if node.module is missing it's a "from . import ..." statement
        # if level > 0 it's a "from .submodule import ..." statement
        if node.module is not None and node.level == 0:
            modules.add(node.module.split(".")[0])
     
    node_iter = ast.NodeVisitor()
    node_iter.visit_Import = visit_Import
    node_iter.visit_ImportFrom = visit_ImportFrom

    with open(file_name) as file:
        node_iter.visit(ast.parse(file.read()))
    print('Módulos carregados com AST: ')
    print(modules)
    

def with_finder(file_name):
    from modulefinder import ModuleFinder 
    # finder = ModuleFinder()
    finder = ModuleFinder(path=file_name)
    finder.run_script(file_name)
    basemods = sorted(set([name.split('.')[0] for name in list(finder.modules.keys())]))
    print("\n ".join(basemods))

    print('Módulos carregados com ModuleFinder:')
    for name, mod in finder.modules.items():
        print('%s: ' % name, end='')
        print(','.join(list(mod.globalnames.keys())[:3]))

    print('Módulos problemáticos:')
    for name, mod in finder.badmodules.items():
        print (f'Nome: {name}, mod: {mod}')

if __name__ == '__main__':
    python_file = 'input/import-sample.py'
    with_finder(python_file)    
    with_ast(python_file)    


# https://stackoverflow.com/questions/2572582/return-a-list-of-imported-python-modules-used-in-a-script    
# Nome: __main__, mod: {
#     '__name__': '__main__', 
#     '__file__': '/Users/job/Documents/dev/doutorado/study/skip-platform/input/decorator-sample.py', 
#     '__path__': None, 
#     '__code__': <code object <module> at 0x7fd6d69fec90, 
#     file "/Users/job/Documents/dev/doutorado/study/skip-platform/input/decorator-sample.py", line 2>, 
#     'globalnames': {
#         'sys': 1, 
#         'unittest': 1, 
#         'ShellCommandTestCase': 1, 
#         '__module__': 1, 
#         '__qualname__': 1, 
#         'test_function': 1, 
#         'test_function_async': 1
#     }, 'starimports': {}}
# Nome: sys, mod: {
#     '__name__': 'sys', 
#     '__file__': None, 
#     '__path__': None, 
#     '__code__': None, 
#     'globalnames': {}, 
#     'starimports': {}
#     }