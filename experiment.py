import ast
from get_repo import Repo
from monitor import all_files
from writercsv import WriterCSV
from specific import CallVisitor
import csv

def dev():

    dir = "data1/sanic"
    name = 'sanic/sanic'
    commit_hash = "6e1c787e5d92edffc59432d772209e49dccf7969"
    
    # dir = "data1/ansible2"
    # name = 'ansible/ansible'
    # commit_hash = 'b63812bc08fd00fd772c28a2604f77f487d23104'
    
    # dir = "data1/flask"
    # name = 'data1/flask'
    # commit_hash = 'bad8843124a50493141a3e3d7920353239021389'
    
    
    #     project_dir = "data1/ansible2"
    # project_name = "ansible/ansible"
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
    # csv_filename = 'input-csv/projects_filted_dev.csv'
    csv_filename = 'input-csv/projects_filted_local.csv'
    # csv_filename = 'input-csv/projects_filted.csv'
    has_head_readed = False
    
    libs_os =  dict()
    libs_os['sys'] = [ 'platform', 'getwindowsversion']
    libs_os['os'] = ['name', 'supports_bytes_environ', 'name']
    libs_os['platform'] = ['platform', 'system', 'version', 'uname','win32_edition','win32_ver','win32_is_iot','mac_ver','libc_ver', 'freedesktop_os_release']
    decorators = ['pytest.mark.skipif', 'mark.skipif', 'skipif', 'pytest.mark.xfail', 'mark.xfail' ,'xfail', 'unittest.skipUnless','skipUnless', 'unittest.skipIf', 'skipIf']

    heads_decorator = ['project_name','project_hash', 'line', 'module', 'package', 'platform', 'decorator', 'razion',  'filename','func_def', 'class_def', 'url']
    heads_compare = ['project_name','project_hash','line', 'module', 'package', 'platform', 'file', 'function', 'method_type','url']
    heads_project_metadata = ['project_name','project_hash', 'libos_use', 'tests_files', 'tests_files_libos_use', 'tests_files_libos_use_and_call',
                              'count_calls_libos_in_code', 'count_calls_libos_in_decorator', 'count_class_decorator', 'count_method_decorator']
    packages_all = []
    razions_all = []
    projects_metadata = []
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not has_head_readed: #skip head
                has_head_readed = True
                continue  
            
            project_libos_use = 0 # number of projects using os-libs 
            count_tests_files = 0 # number of tests files 
            count_tests_files_libos_use = 0 # number of tests files that declare and use the os-libs 
            count_tests_files_libos_use_and_call = 0 # number of different tests files that declare, use the os-libs and call specifics methods
            count_calls_libos_in_code = 0 # number of calls to os-libs in code
            count_calls_libos_in_decorator = 0 # number of calls to os-libs in decorator
            count_class_decorator = 0 
            count_method_decorator = 0
            
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
                    #all tests
                    count_tests_files = count_tests_files + 1
                    
                    #only files declare libs_os
                    if not monitor.modules:  continue 
                    if not set(libs_os.keys()).intersection(monitor.modules): continue
                                        
                    if len(monitor.package_os) > 0:
                        packages.extend(monitor.package_os)
                            
                    if len(monitor.razions) > 0:
                        for row in monitor.razions:
                            row_temp = []    
                            for v in heads_decorator:
                                # print(f"arquivo:{filename} {row['line']} -> {row['module']}.{row['platform']} ")
                                row_temp.extend([row[v]])
                                if v == "func_def" and str(row[v]).strip() == "": 
                                    count_class_decorator = count_class_decorator + 1
                                    
                            razions.append(row_temp)
                    
                    project_libos_use = 1 #project uses libos
                    count_tests_files_libos_use = count_tests_files_libos_use + 1 #only tests use libos
                    count_calls_libos_in_code = count_calls_libos_in_code + len(monitor.package_os) 
                    count_calls_libos_in_decorator = count_calls_libos_in_decorator+ len(monitor.razions)
                    
                    if (len(monitor.package_os) > 0 or len(monitor.razions) > 0):
                        count_tests_files_libos_use_and_call = count_tests_files_libos_use_and_call +1
                        
                except SyntaxError as ex:
                    print(f'SyntaxError: {ex} in {python_file}') 
            # ['project_name','project_hash', 'libos_use', 
            # 'tests_files', 'tests_files_libos_use',
            # 'count_calls_libos_in_code', 'count_calls_libos_in_decorator'
            # 'count_class_decorator', 'count_method_decorator']
            
            count_method_decorator = count_calls_libos_in_decorator - count_class_decorator # method = all - class
            
            projects_metadata.append([
                project_name, project_hash,project_libos_use,
                count_tests_files, count_tests_files_libos_use, count_tests_files_libos_use_and_call, 
                count_calls_libos_in_code,count_calls_libos_in_decorator,
                count_class_decorator, count_method_decorator
            ])
            
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
    
    writer = WriterCSV(name=f'experiment_all_metadata', path="analysis")
    writer.write(head=heads_project_metadata, rows=projects_metadata)
    
