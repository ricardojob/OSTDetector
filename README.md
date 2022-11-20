# samples

We have three cases: attribute, call e compare.

### If with Attibute (verify if value exists)

original code:

```
if config.parsed_args.platform:
    return config.parsed_args.platform

```

tree generated :

```
If(
test=Attribute(
    value=Attribute(value=Name(id='config', ctx=Load()), 
 attr='parsed_args', ctx=Load()), attr='platform', ctx=Load()),
 
 body=[Return(value=Attribute(value=Attribute(value=Name(id='config', 
 ctx=Load()), attr='parsed_args', ctx=Load()), attr='platform', 
 ctx=Load()))],
 
 orelse=[]
 )
 ```


 ### If with Call (call a function for verification)

original code:

```
if sys_platform.startswith("linux"):
    raise RuntimeError("Unknown machine!")
```

tree generated :

```
If(test=Compare(left=Name(id='sys_platform', ctx=Load()), "
 "ops=[Eq()], comparators=[Constant(value='win32', kind=None)]), "
 "body=[Return(value=Constant(value='win-64', kind=None))], orelse=[])])])]
 ```

 ### If with Compare ()

original code:

```
if machine == "aarch64":
    return "linux-aarch64"
elif machine == "x86_64":
    return "linux-64"
else:
    raise RuntimeError("Unknown machine!")
```

tree generated :

```
body=[
    If(test=Compare(left=Name(id='machine', ctx=Load()), "
 "ops=[Eq()], comparators=[Constant(value='aarch64', kind=None)]), "
 "body=[Return(value=Constant(value='linux-aarch64', kind=None))], "
 "orelse=[If(test=Compare(left=Name(id='machine', ctx=Load()), ops=[Eq()], "
 "comparators=[Constant(value='x86_64', kind=None)]), "
 "body=[Return(value=Constant(value='linux-64', kind=None))], "
 "orelse=[Raise(exc=Call(func=Name(id='RuntimeError', ctx=Load()), "
 "args=[Constant(value='Unknown machine!', kind=None)], keywords=[]), "
 "cause=None)])])
 ],
 ```


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