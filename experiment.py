import ast
from get_repo import Repo
from monitor import all_files
from writercsv import WriterCSV
# from pathlib import Path
from specific import CallVisitor
import csv

def flask():
    dir = '/Users/job/Documents/dev/doutorado/study/skip-platform/data/flask'
    url = 'https://github.com/pallets/flask/'
    # name = 'flask'
    repo = Repo('flask',url)
    local = repo.clone_at(dir)
    commit_hash= local.commit_head()
    return repo.name, commit_hash, dir

def dev():
    dir = "data/ansible2"
    name = 'ansible/ansible'
    commit_hash = 'bad8843124a50493141a3e3d7920353239021389'
    return name, commit_hash, dir

def dev2():
    dir = "data/django"
    name = 'django/django'
    commit_hash = '9d9ec0c79f52efad3a4d3f6ac4644d5c9fb1d22c'
    return name, commit_hash, dir

def local():
    # /home/ricardojob/dev/study-01-platform
    dir = './data/django'
    url = 'https://github.com/django/django'
    # name = 'django'
    repo = Repo('django',url)
    local = repo.clone_at(dir)
    commit_hash= local.commit_head()
    return repo.name, commit_hash, dir

def clone(repo_name):
    # dir = f'/Users/job/Documents/dev/doutorado/study/skip-platform/data/{repo_name}'
    dir = f'data/{repo_name}'

    url = f'https://github.com/{repo_name}'
    # name = 'django'
    repo = Repo(repo_name,url)
    local = repo.clone_at(dir)
    commit_hash= local.commit_head()
    return repo.name, commit_hash, local.path()

if __name__ == '__main__':
    # project_name, project_hash, project_dir = flask()
    # project_name, project_hash, project_dir = dev()
    # project_name, project_hash, project_dir = local()

    # heads = [
    #     'project_name', 'project_version', 'file_path', 'file_modules',
    #     'file_modules_excludes', 'file_with_tests'
    # ]
    # rows = []
    
    # libs = set()
    # libs.add('os')
    # libs.add('platform')
    # libs.add('sys')
    # libs.add('unittest')
    # projects_problems = []
    # head_problems = ['project_name','files_ok', 'files_erros']

    csv_filename = 'input-csv/projects_filted_local.csv'
    # csv_filename = 'input-csv/projects_filted.csv'
    has_head_readed = False
    
    libs_os =  dict()
    libs_os['sys'] = [ 'platform', 'getwindowsversion']
    libs_os['os'] = ['name', 'supports_bytes_environ', 'name']
    libs_os['platform'] = ['platform', 'system', 'version', 'uname','win32_edition','win32_ver','win32_is_iot','mac_ver','libc_ver', 'freedesktop_os_release']
    decorators = ['pytest.mark.skipif', 'mark.skipif', 'skipif', 'pytest.mark.xfail', 'mark.xfail' ,'xfail', 'unittest.skipUnless','skipUnless', 'unittest.skipIf', 'skipIf']

    
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not has_head_readed: #skip head
                has_head_readed = True
                continue  
            # print(row[0])
            # """
            count = 0
            # print(row[0])
            # project_name = row[0] 
            # project_hash = '1'
            # project_dir = '/Users/job/Documents/dev/doutorado/study/skip-platform/data/'+project_name
            # project_name, project_hash, project_dir = clone(row[0])
            # project_name, project_hash, project_dir = dev()
            project_name, project_hash, project_dir = dev2()
            
            pacotes = []

            for python_file in all_files(project_dir):
                # verification initial
                if python_file.is_dir(): continue #only files
                filename = str(python_file).replace(project_dir,"")
                # print(f'{project_name}: {filename}, {"test" in filename}')
                if not 'test' in filename: continue #only test files
                # fill data

                try:
                    # if 'test' in str(python_file): # verify file with test -> 'file_with_tests'
                    #     # print(f'has test: {python_file}')
                    #     pass
                    # else:
                    #     # print('no test')
                    #     pass
                    parser = ast.parse(open(python_file).read())
                    monitor = CallVisitor(libs_os, 
                                          project_name,
                                          project_hash,
                                          filename,
                                          decorators)                    
                    monitor.visit(parser)
                    if not monitor.modules:  continue
                        # print('no modules')
                    #     pass
                    # else:
                    #     # print(', '.join(list(monitor.modules)))  # -> 'file_modules'
                    #     # monitor.print_modules()
                    #     if set(libs_os.keys()).intersection(monitor.modules): # verify file with modules -> 'file_modules_excludes'
                    #         # print(f'has modules: {len(monitor.modules)}') # -> 'file_modules_excludes'
                    #         pass
                    #     else:
                    #         # print('no modules') # -> 'file_modules_excludes'
                    #         pass
                    # file_list.append(str(filename))
                    # monitor.print_chamadas()
                    # if len(monitor.package_os) > 0:
                        # row = []
                        # row.append(project_name)
                        # row.append(project_hash)
                    
                        # pacotes.extend(monitor.package_os)
                    if len(monitor.package_os) > 0:
                        pacotes.extend(monitor.package_os)
                        print(10*'---', f'LISTANDO os packs: {filename}')
                        for row in monitor.package_os:
                            print(f'{row[2]} -> {row[3]}.{row[4]}')
                            print(row)
                            
                    if len(monitor.razions) > 0:
                        print(10*'---', f'LISTANDO os razões: {filename}')
                        for row in monitor.razions:
                            print(f'{row["line"]} -> {row["module"]}.{row["package"]}')                
                            # print(row)
                except SyntaxError as ex:
                    print('erro', python_file) 
                    # self.package_os.append([node.lineno, mod[0], parent.attr,self.classe,self.funcao])
        # heads = ['project_name','project_hash','line', 'module', 'method', 'file', 'function']
        # writer = WriterCSV(name=f'experiment_{project_name.replace("/","_")}', path="analysis")
        # writer.write(head=heads, rows=pacotes)                 
"""
                try:
                    parser = ast.parse(open(python_file).read())
                    monitor = MonitorVisitor()
                    monitor.visit(parser)
                    if not monitor.modules: # continue
                        row.append('')
                        row.append(0)
                    else:
                        row.append(', '.join(list(monitor.modules)))  # -> 'file_modules'
                        if libs.intersection(monitor.modules): # verify file with modules -> 'file_modules_excludes'
                            row.append(1) # -> 'file_modules_excludes'
                        else:
                            row.append(0) # -> 'file_modules_excludes'

                    # if 'test' in filename: # verify file with test -> 'file_with_tests'
                    #     row.append(1)
                    # else:
                    #     row.append(0)
                    rows.append(row)
                except SyntaxError as ex:
                    # salvar os arquivos não processados
                    print('erro', python_file) 
                    count = count + 1
                # rows.append(row)
            
            projects_problems.append([project_name,  len(rows), count])
            print(f'{project_name}: finished, files: {len(rows)}; erros: {count}')
            # 
            # [print(a) for a in rows]
    writer = WriterCSV(name=f'test_excludes_{project_name.replace("/","_")}', path="analysis")
    writer.write(head=heads, rows=rows) 
    
    # writer = WriterCSV(name="problems_excludes", path="analysis")
    # writer.write(head=head_problems, rows=projects_problems) 
"""