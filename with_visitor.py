import ast
# from pprint import pprint

class IfVisitor(ast.NodeVisitor):
    count = 0
    
    def parse_attr(self, attribute):
        if isinstance(attribute.value, ast.Name):
            print('value attribute: ', attribute.value.id)
        if isinstance(attribute.value, ast.Attribute):
            self.parse_attr(attribute.value)
        print('name attribute: ', attribute.attr)

    def visit_If(self, node):
        self.count+=1
        print(node.test)
        if isinstance(node.test, ast.Attribute):
            self.parse_attr(node.test)
        if isinstance(node.test, ast.Compare):
            print('compare')
        if isinstance(node.test, ast.Call):
            print('call')    
        ast.NodeVisitor.generic_visit(self, node)    

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

count = 0
with open("input/sample-if.py", "r") as source:
    tree = ast.parse(source.read())
    # pprint(ast.dump(tree))
    visitor = IfVisitor()
    visitor.visit(tree)
    print(visitor.count)


