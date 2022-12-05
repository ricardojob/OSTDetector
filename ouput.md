# saída do script check.py

```
__main__
 math
 sys
Módulos carregados com ModuleFinder:
__main__: sos,seno,unittest
sys: 
math: 
Módulos problemáticos:
Nome: unittest, mod: {'__main__': 1}
Módulos carregados com AST: 
{'math', 'unittest', 'sys'}
```

# saída do script monitor.py
```
sys -> sos
unittest -> None
linha: 9, Name:  print
linha: 10, Name:  print
linha: 10, Name:  seno
linha: 7, Attribute:  unittest, Attr: skipIf
linha: 15, Name:  print
linha: 15, Name:  cos
linha: 16, Name:  print
linha: 12, Attribute:  unittest, Attr: skipIf
Módulos carregados com AST: 
math, sys, unittest
```
