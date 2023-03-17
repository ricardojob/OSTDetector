import ast
from get_repo import Repo
from monitor import all_files
from writercsv import WriterCSV
from specific import CallVisitor
import csv

def dev():
    dir = "data/ansible2"
    name = 'ansible/ansible'
    commit_hash = 'bad8843124a50493141a3e3d7920353239021389'
    return name, commit_hash, dir

def clone(repo_name):
    dir = f'data/{repo_name}'
    url = f'https://github.com/{repo_name}'
    repo = Repo(repo_name,url)
    local = repo.clone_at(dir)
    print(f'clone: {repo.name}')
    commit_hash = local.commit_head()
    return repo.name, commit_hash, local.path()

if __name__ == '__main__':
    csv_filename = 'input-csv/projects_filted_local.csv'
    # csv_filename = 'input-csv/projects_filted.csv'
    has_head_readed = False
    
    libs_os =  dict()
    libs_os['sys'] = [ 'platform', 'getwindowsversion']
    libs_os['os'] = ['name', 'supports_bytes_environ', 'name']
    libs_os['platform'] = ['platform', 'system', 'version', 'uname','win32_edition','win32_ver','win32_is_iot','mac_ver','libc_ver', 'freedesktop_os_release']
    decorators = ['pytest.mark.skipif', 'mark.skipif', 'skipif', 'pytest.mark.xfail', 'mark.xfail' ,'xfail', 'unittest.skipUnless','skipUnless', 'unittest.skipIf', 'skipIf']

    heads_decorator = ['project_name','project_hash', 'line', 'module', 'package', 'platform', 'decorator', 'razion',  'filename','func_def', 'class_def']
    heads_compare = ['project_name','project_hash','line', 'module', 'package', 'platform', 'file', 'function']
    packages_all = []
    razions_all = []
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not has_head_readed: #skip head
                has_head_readed = True
                continue  
            # count = 0
            project_name, project_hash, project_dir = clone(row[0])
            # project_name, project_hash, project_dir = dev()
            
            packages = []
            razions = []
            
            for python_file in all_files(project_dir):
                # verification initial
                if python_file.is_dir(): continue #only files
                filename = str(python_file).replace(project_dir,"")
                if not 'test' in filename: continue #only test files
                # fill data

                try:
                    parser = ast.parse(open(python_file).read())
                    monitor = CallVisitor(libs_os, 
                                          project_name,
                                          project_hash,
                                          filename,
                                          decorators)                    
                    monitor.visit(parser)
                    if not monitor.modules:  continue #only files declare libs_os
                    
                    if len(monitor.package_os) > 0:
                        packages.extend(monitor.package_os)
                            
                    if len(monitor.razions) > 0:
                        for row in monitor.razions:
                            row_temp = []    
                            # [row_temp.extend([v]) for v in row.values()]
                            for v in heads_decorator:
                                row_temp.extend([row[v]])
                                # print(f'v: {v} -> r: {row[v]}, l: {len(row_temp)}')
                            razions.append(row_temp)
                except SyntaxError as ex:
                    print(f'SyntaxError: {ex} in {python_file}') 

            writer = WriterCSV(name=f'experiment_{project_name.replace("/","_")}_compare', path="analysis/experiment")
            writer.write(head=heads_compare, rows=packages)
            
            writer = WriterCSV(name=f'experiment_{project_name.replace("/","_")}_razions', path="analysis/experiment")
            writer.write(head=heads_decorator, rows=razions) 
            
            packages_all.extend(packages)
            razions_all.extend(razions) 
            print(f'finish: {project_name}')                 
        
    writer = WriterCSV(name=f'experiment_all_compare', path="analysis")
    writer.write(head=heads_compare, rows=packages_all)

    writer = WriterCSV(name=f'experiment_all_razions', path="analysis")
    writer.write(head=heads_decorator, rows=razions_all)