# samples


```python
# method returns the result of the expression after evaluation, and store the result in tree
tree = ast.parse(source.read()) 
#method returns a formatted string of the tree structure in tree.
pprint(ast.dump(tree)) 
```

We have three cases: attribute, call e compare.


### If with Attibute (verify if value exists)


Grammar 

```
Attribute(expr value, identifier attr, expr_context ctx)
```

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

Grammar 

```
Call(expr func, expr* args, keyword* keywords)
```

original code:

```
if sys_platform.startswith("linux"):
    raise RuntimeError("Unknown machine!")
```

tree generated :

```
 If(
    test=Call(
        func=Attribute(value=Name(id='sys_platform', ctx=Load()), attr='startswith', ctx=Load()), 
        args=[Constant(value='linux', kind=None)], 
        keywords=[]), 
    body=[Raise(
        exc=Call(
            func=Name(id='RuntimeError', ctx=Load()), 
            args=[Constant(value='Unknown machine', kind=None)], 
            keywords=[]), 'cause=None)], 
    orelse=[])
 ```

 ### If with Compare ()

Grammar 

```
Compare(expr left, cmpop* ops, expr* comparators)
```


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
If(test=Compare(
        left=Name(id='machine', ctx=Load()), ops=[Eq()], comparators=[Constant(value='aarch64', kind=None)]
), 
    body=[Return(value=Constant(value='linux-aarch64', kind=None))], 
orelse=[
    If(test=Compare(
        left=Name(id='machine', ctx=Load()), ops=[Eq()], comparators=[Constant(value='x86_64', kind=None)]
    ), 
    body=[Return(value=Constant(value='linux-64', kind=None))], 
orelse=[
    Raise(exc=Call(
        func=Name(id='RuntimeError', ctx=Load()), args=[Constant(value='Unknown machine!', kind=None)], keywords=[]), cause=None)])
 )
 ```
