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