import ast
import astunparse
# from pprint import pprint

def main():
    with open("input/sample-platform-if.py", "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.visit(tree)
    # analyzer.report()


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}
    # IfExp(expr test, expr body, expr orelse)
    def visit_IfExp(self, node):
        print('test: ', node.test.value.id)
        # print('orelse: ', node.orelse)
        # print(astunparse.dump(node))
        # self.generic_visit(node)
    # def FunctionDef(self, node):    
    #     print('FunctionDef: ', node.decorator_list)
        # self.generic_visit(node)

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