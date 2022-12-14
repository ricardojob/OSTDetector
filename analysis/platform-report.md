### Busca no Github

Quando realizamos a busca por arquivos Python no projeto [Django](https://github.com/search?l=Python&p=3&q=platform+repo%3Adjango%2Fdjango+extension%3Apy+language%3APython+language%3APython&ref=advsearch&type=Code), encontramos:

* `platform`: 30 ocorrências dessa palavra-chave.
* `os`: 183 ocorrências dessa palavra-chave.
* `sys`: 126 ocorrências dessa palavra-chave.
* `unittest`: 226 ocorrências dessa palavra-chave.

### Requisitos básicos

Código sintaticamente válido (sem erros de sintaxe)

### Executando a ferramenta 

Arquivo com problemas no parse: `django/django/tests/test_runner_apps/tagged/tests_syntax_error.py`


Ao executarmos a ferramenta com as três bibliotecas (os, sys, platform) e filtramos por arquivos:
- (A) possuem `test` no nome qualificado (path do arquivo)
- (B) arquivos que declaram alguma das bibliotecas de interesse 

Encontramos 1895 ocorrências de A, 213 ocorrências de B, e 133 ocorrências de A e B.

-------
Ao executarmos a ferramenta com a  biblioteca (sys) e filtramos por arquivos:
- (A) possuem `test` no nome qualificado (path do arquivo)
- (B) arquivos que declaram uso da biblioteca de interesse 
Encontramos 1895 ocorrências de A, 98 ocorrências de B, e 57 ocorrências de A e B.

-------
Ao executarmos a ferramenta com a  biblioteca (os) e filtramos por arquivos:
- (A) possuem `test` no nome qualificado (path do arquivo)
- (B) arquivos que declaram uso da biblioteca de interesse 
Encontramos 1895 ocorrências de A, 163 ocorrências de B, e 103 ocorrências de A e B.

-------
Ao executarmos a ferramenta com a  biblioteca (platform) e filtramos por arquivos:
- (A) possuem `test` no nome qualificado (path do arquivo)
- (B) arquivos que declaram uso da biblioteca de interesse 
Encontramos 1895 ocorrências de A, 4 ocorrências de B, e 2 ocorrências de A e B.

-------
Ao executarmos a ferramenta com a  biblioteca (unittest) e filtramos por arquivos:
- (A) possuem `test` no nome qualificado (path do arquivo)
- (B) arquivos que declaram uso da biblioteca de interesse 
Encontramos 1895 ocorrências de A, 224 ocorrências de B, e 223 ocorrências de A e B.

### Resultados

Linha 90, no arquivo `/tests/asgi/tests.py`:

```
# Windows registry may not be configured with correct
# mimetypes.
if sys.platform == "win32" and key == b"Content-Type":
    self.assertEqual(value, b"text/plain")
```

Linha 521, no arquivo `/tests/migrations/test_writer.py`:

```
if sys.platform == "win32":
    self.assertSerializedEqual(pathlib.WindowsPath.cwd())
    path = pathlib.WindowsPath("A:\\File.txt")
    expected = ("pathlib.PureWindowsPath('A:/File.txt')", {"import pathlib"})
    self.assertSerializedResultEqual(path, expected)
```

Linha 550, no arquivo `/tests/admin_filters/tests.py`:

```
@unittest.skipIf(
    sys.platform == "win32",
    "Windows doesn't support setting a timezone that differs from the "
    "system timezone.",
)
@override_settings(USE_TZ=True)
def test_datefieldlistfilter_with_time_zone_support(self):
    # Regression for #17830
    self.test_datefieldlistfilter()
```

Linha 216, no arquivo `/tests/template_tests/test_loaders.py`:

```
@unittest.skipIf(
    sys.platform == "win32",
    "Python on Windows doesn't have working os.chmod().",
)
def test_permissions_error(self):
    with tempfile.NamedTemporaryFile() as tmpfile:
        tmpdir = os.path.dirname(tmpfile.name)
        tmppath = os.path.join(tmpdir, tmpfile.name)
        os.chmod(tmppath, 0o0222)
        with self.set_dirs([tmpdir]):
            with self.assertRaisesMessage(PermissionError, "Permission denied"):
                self.engine.get_template(tmpfile.name)
```