import ast
import astunparse
from pprint import pprint


    # with open("input/sample-platform-if.py", "r") as source:
    #     tree = ast.parse(source.read())

    # analyzer = Analyzer()
    # analyzer.visit(tree)
    # analyzer.report()


# class Analyzer(ast.NodeVisitor):
#     def __init__(self):
#         self.stats = {"import": [], "from": []}
#     # IfExp(expr test, expr body, expr orelse)
#     def visit_IfExp(self, node):
#         print('test: ', node.test.value.id)
#         # print('orelse: ', node.orelse)
#         # print(astunparse.dump(node))
#         # self.generic_visit(node)
#     # def FunctionDef(self, node):    
#     #     print('FunctionDef: ', node.decorator_list)
#         # self.generic_visit(node)

def flatten_attr(node):
    if isinstance(node, ast.Attribute):
        return str(flatten_attr(node.value)) + '.' + node.attr
    elif isinstance(node, ast.Name):
        return str(node.id)
    else:
        pass


def extract_routes(file, decorator_name):
    routes = []
    # filename = file
    with open(file) as f:
        try:
            tree = ast.parse(f.read())
        except:
            return routes

    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            # if not isinstance(node, ast.Call):
            #     continue
            print(node)
        # if isinstance(node, ast.FunctionDef):
            # function_name = node.name
            # for d in node.decorator_list:
            #     if not isinstance(d, ast.Call):
            #         continue
            #     if not flatten_attr(d.func) == decorator_name:
            #         continue
            #     path = d.args[0].s
            #     description = None
            #     parameters = None
            #     status_codes = None
            #     for kw in d.keywords:
            #         if kw.arg == 'description':
            #             description = kw.value.s
            #         if kw.arg == 'parameters':
            #             parameters = ast.literal_eval(astunparse.unparse(kw.value))
            #         if kw.arg == 'status_codes':
            #             status_codes = ast.literal_eval(astunparse.unparse(kw.value))
                # r = Route(filename, decorator_name, function_name, path, description, parameters,
                #           status_codes)
                # routes.append(r)

    return routes
def main():
    extract_routes('input/sample-platform-if.py','')

if __name__ == "__main__":
    main()
# IfExp(
#   test=Attribute(
#     value=Name(
#       id='p',
#       ctx=Load()),
#     attr='email',
#     ctx=Load()),
#   body=BinOp(
#     left=BinOp(
#       left=BinOp(
#         left=Attribute(
#           value=Name(
#             id='p',
#             ctx=Load()),
#           attr='name',
#           ctx=Load()),
#         op=Add(),
#         right=Constant(
#           value=' (',
#           kind=None)),
#       op=Add(),
#       right=Attribute(
#         value=Name(
#           id='p',
#           ctx=Load()),
#         attr='email',
#         ctx=Load())),
#     op=Add(),
#     right=Constant(
#       value=')',
#       kind=None)),
#   orelse=Attribute(
#     value=Name(
#       id='p',
#       ctx=Load()),
#     attr='name',
#     ctx=Load()))