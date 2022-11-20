import ast
from pprint import pprint

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

    # def visit_Compare(self, node):
    #     print('Node type: Compare\nFields:', node._fields)
    #     ast.NodeVisitor.generic_visit(self, node)

    # def visit_Name(self, node):
    #     print('Node type: Name\nFields:', node._fields)
    #     ast.NodeVisitor.generic_visit(self, node)

    # def visit_Constant(self, node):
    #     print('Node type: Constant\nFields:', node._fields)
    #     ast.NodeVisitor.generic_visit(self, node)

    # def visit_Pass(self, node):
    #     print('Node type: Pass\nFields:', node._fields)
    #     ast.NodeVisitor.generic_visit(self, node)

    
    


# tree = ast.parse("""
# if x < 20:
#    pass
# elif y > 40:
#     pass
# else:
#     pass
# """)
# count = 0
# with open("input/sample-platform-if.py", "r") as source:
#     tree = ast.parse(source.read())
#     pprint(ast.dump(tree))
#     visitor = IfVisitor()
#     visitor.visit(tree)
#     print(visitor.count)


code = """
def get_conda_subdir():
    if config.parsed_args.platform:
        return config.parsed_args.platform

    sys_platform = sys.platform
    machine = platform.machine()
    if sys_platform.startswith("linux"):
        if machine == "aarch64":
            return "linux-aarch64"
        elif machine == "x86_64":
            return "linux-64"
        else:
            raise RuntimeError("Unknown machine!")
    elif sys_platform == "darwin":
        if machine == "arm64":
            return "osx-arm64"
        else:
            return "osx-64"
    elif sys_platform == "win32":
        return "win-64"
"""

count = 0
tree = ast.parse(code)
# pprint(ast.dump(tree))
visitor = IfVisitor()
visitor.visit(tree)
print(visitor.count)

("Module(body=[FunctionDef(name='get_conda_subdir', "
 'args=arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], '
 'kw_defaults=[], kwarg=None, defaults=[]), '
 "body=[If(test=Attribute(value=Attribute(value=Name(id='config', ctx=Load()), "
 "attr='parsed_args', ctx=Load()), attr='platform', ctx=Load()), "
 "body=[Return(value=Attribute(value=Attribute(value=Name(id='config', "
 "ctx=Load()), attr='parsed_args', ctx=Load()), attr='platform', "
 "ctx=Load()))], orelse=[]), Assign(targets=[Name(id='sys_platform', "
 "ctx=Store())], value=Attribute(value=Name(id='sys', ctx=Load()), "
 "attr='platform', ctx=Load()), type_comment=None), "
 "Assign(targets=[Name(id='machine', ctx=Store())], "
 "value=Call(func=Attribute(value=Name(id='platform', ctx=Load()), "
 "attr='machine', ctx=Load()), args=[], keywords=[]), type_comment=None), "
 "If(test=Call(func=Attribute(value=Name(id='sys_platform', ctx=Load()), "
 "attr='startswith', ctx=Load()), args=[Constant(value='linux', kind=None)], "
 "keywords=[]), body=[If(test=Compare(left=Name(id='machine', ctx=Load()), "
 "ops=[Eq()], comparators=[Constant(value='aarch64', kind=None)]), "
 "body=[Return(value=Constant(value='linux-aarch64', kind=None))], "
 "orelse=[If(test=Compare(left=Name(id='machine', ctx=Load()), ops=[Eq()], "
 "comparators=[Constant(value='x86_64', kind=None)]), "
 "body=[Return(value=Constant(value='linux-64', kind=None))], "
 "orelse=[Raise(exc=Call(func=Name(id='RuntimeError', ctx=Load()), "
 "args=[Constant(value='Unknown machine!', kind=None)], keywords=[]), "
 "cause=None)])])], orelse=[If(test=Compare(left=Name(id='sys_platform', "
 "ctx=Load()), ops=[Eq()], comparators=[Constant(value='darwin', kind=None)]), "
 "body=[If(test=Compare(left=Name(id='machine', ctx=Load()), ops=[Eq()], "
 "comparators=[Constant(value='arm64', kind=None)]), "
 "body=[Return(value=Constant(value='osx-arm64', kind=None))], "
 "orelse=[Return(value=Constant(value='osx-64', kind=None))])], "
 "orelse=[If(test=Compare(left=Name(id='sys_platform', ctx=Load()), "
 "ops=[Eq()], comparators=[Constant(value='win32', kind=None)]), "
 "body=[Return(value=Constant(value='win-64', kind=None))], orelse=[])])])], "
 'decorator_list=[], returns=None, type_comment=None)], type_ignores=[])')



#  def parse(d, c):
#   def parse_chain(d, c, p=[]):
#      if isinstance(d, ast.Name):
#         return [d.id]+p
#      if isinstance(d, ast.Call):
#         for i in d.args:
#            parse(i, c)
#         return parse_chain(d.func, c, p)
#      if isinstance(d, ast.Attribute):
#         return parse_chain(d.value, c, [d.attr]+p)
#   if isinstance(d, (ast.Call, ast.Attribute)):
#      c.append('.'.join(parse_chain(d, c)))
#   else:
#      for i in getattr(d, '_fields', []):
#        if isinstance(t:=getattr(d, i), list):
#           for i in t:
#              parse(i, c)
#        else:
#           parse(t, c)

