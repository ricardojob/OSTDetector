from specific import CallVisitor
import ast

# python_file = "data/django/django/tests/asgi/tests.py"
# python_file = "data/django/django/tests/migrations/test_writer.py"
# python_file = "data/django/django/tests/shell/tests.py"
# python_file = "data/django/django/tests/admin_filters/tests.py"
# python_file = "data/django/django/tests/template_tests/test_loaders.py"
# python_file = "input/sys-sample.py"
# python_file = "input/import-sample.py"
# python_file = "data/django/django/tests/mail/tests.py"
python_file = "data/ansible2/test/support/integration/plugins/modules/timezone.py"
# python_file = "data/ansible2/test/units/utils/test_encrypt.py"

libs_os =  dict()
libs_os['sys'] = [ 'platform', 'getwindowsversion']
libs_os['os'] = ['name', 'supports_bytes_environ', 'name']
libs_os['platform'] = ['platform', 'system', 'version', 'uname','win32_edition','win32_ver','win32_is_iot','mac_ver','libc_ver', 'freedesktop_os_release']
decorators = ['pytest.mark.skipif', 'mark.skipif', 'skipif', 'pytest.mark.xfail', 'mark.xfail' ,'xfail', 'unittest.skipUnless','skipUnless', 'unittest.skipIf', 'skipIf']
pacotes = []
project_dir = "data/ansible2/test"
project_name = "ansible"
filename = str(python_file).replace(project_dir,"")
try:
    parser = ast.parse(open(python_file).read())
    monitor = CallVisitor(libs_os, project_name,
                          "bad8843124a50493141a3e3d7920353239021389", 
                          filename,
                          decorators)
    monitor.visit(parser)
    """if not monitor.modules:  #continue
        # print('no modules')
        pass
    else:
        # print(', '.join(list(monitor.modules)))  # -> 'file_modules'
        # monitor.print_modules()
        if set(libs_os.keys()).intersection(monitor.modules): # verify file with modules -> 'file_modules_excludes'
            # print(f'has modules: {len(monitor.modules)}') # -> 'file_modules_excludes'
            pass
        else:
            # print('no modules') # -> 'file_modules_excludes'
            pass """
    # file_list.append(str(filename))
    # monitor.print_chamadas()
    if len(monitor.package_os) > 0:
        pacotes.extend(monitor.package_os)
        
        print(50*'---', 'LISTANDO os packs:')
        for row in monitor.package_os:
            print(row)
            
    if len(monitor.razions) > 0:
        print(50*'---', 'LISTANDO os razões:')
        for row in monitor.razions:
            print(row)
            
except SyntaxError as ex:
    print('erro', python_file) 
                # self.package_os.append([node.lineno, mod[0], parent.attr,self.classe,self.funcao])
# heads = ['linhas', 'module', 'package', 'file', 'function']
# writer = WriterCSV(name=f'packages_os_{project_name.replace("/","_")}', path="analysis")
# writer.write(head=heads, rows=pacotes) 
