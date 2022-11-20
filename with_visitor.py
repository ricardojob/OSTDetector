import ast
from pprint import pprint

class IfVisitor(ast.NodeVisitor):
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
        # print('compare', compare)
        if isinstance(compare.left, ast.Name):
            print('left compare: ', compare.left.id)
        for comparator in compare.comparators:    
            if isinstance(comparator, ast.Constant):
                print('comparators compare: ', comparator.value)            
    
    # Call(expr func, expr* args, keyword* keywords)
    def parse_call(self, call):
        print('call func: ', call.func)
        if isinstance(call.func, ast.Name):
            # self.parse_attr(call.func.id)
            print('call func id: ', call.func.id)
        if isinstance(call.func, ast.Attribute):
            self.parse_attr(call.func)
        for arg in call.args:    
            if isinstance(arg, ast.Constant):
                print('call args: ', arg.value)
        # if isinstance(call.left, ast.Name):
        #     print('left compare: ', call.left.id)
        # for comparator in call.comparators:    
        #     if isinstance(comparator, ast.Constant):
        #         print('comparators compare: ', comparator.value)  

#  If(
#     test=Call(
#         func=Attribute(value=Name(id='sys_platform', ctx=Load()), attr='startswith', ctx=Load()), 
#         args=[Constant(value='linux', kind=None)], 
#         keywords=[]), 
#     body=[Raise(
#         exc=Call(
#             func=Name(id='RuntimeError', ctx=Load()), 
#             args=[Constant(value='Unknown machine', kind=None)], 
#             keywords=[]), 'cause=None)], 
#     orelse=[])

    def visit_If(self, node):
        self.count+=1
        # print(node.test)
        if isinstance(node.test, ast.Attribute):
            self.parse_attr(node.test)
        if isinstance(node.test, ast.Compare):
            self.parse_compare(node.test)
        if isinstance(node.test, ast.Call):
            self.parse_call(node.test)
        ast.NodeVisitor.generic_visit(self, node)    


count = 0
with open("input/sample-if.py", "r") as source:
    tree = ast.parse(source.read())
    # pprint(ast.dump(tree))
    visitor = IfVisitor()
    visitor.visit(tree)
    print(visitor.count)


# count = 0
# with open("input/sample-platform-if.py", "r") as source:
#     tree = ast.parse(source.read())
#     pprint(ast.dump(tree))
#     visitor = IfVisitor()
#     visitor.visit(tree)
#     print(visitor.count)


# code = """
# def get_conda_subdir():
#     if config.parsed_args.platform:
#         return config.parsed_args.platform

#     sys_platform = sys.platform
#     machine = platform.machine()
#     if sys_platform.startswith("linux"):
#         if machine == "aarch64":
#             return "linux-aarch64"
#         elif machine == "x86_64":
#             return "linux-64"
#         else:
#             raise RuntimeError("Unknown machine!")
#     elif sys_platform == "darwin":
#         if machine == "arm64":
#             return "osx-arm64"
#         else:
#             return "osx-64"
#     elif sys_platform == "win32":
#         return "win-64"
# """

# count = 0
# tree = ast.parse(code)
# # pprint(ast.dump(tree))
# visitor = IfVisitor()
# visitor.visit(tree)
# print(visitor.count)
