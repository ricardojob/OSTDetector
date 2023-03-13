import ast
from get_repo import Repo
from monitor import MonitorVisitor, all_files
from writercsv import WriterCSV
from pathlib import Path
from call_module import CallVisitor
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
    dir = '/Users/job/Documents/dev/doutorado/study/skip-platform/input'
    name = 'input'
    commit_hash = 'HEAD'
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
    dir = f'./data/{repo_name}'

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

    heads = [
        'project_name', 'project_version', 'file_path', 'file_modules',
        'file_modules_excludes', 'file_with_tests'
    ]
    rows = []
    
    libs = set()
    # libs.add('os')
    libs.add('platform')
    # libs.add('sys')
    # libs.add('unittest')
    projects_problems = []
    head_problems = ['project_name','files_ok', 'files_erros']

    csv_filename = 'input-csv/projects_filted_local.csv'
    # csv_filename = 'input-csv/projects_filted.csv'
    has_head_readed = False
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
            project_name, project_hash, project_dir = clone(row[0])
            # project_name, project_hash, project_dir = local()
    
            for python_file in all_files(project_dir):
                if python_file.is_dir(): continue
                row = []
                row.append(project_name)
                row.append(project_hash)
                filename = str(python_file).replace(project_dir,"")
                
                if not 'test' in filename: continue #only test files
                
                row.append(filename)
                # print(f'{project_name}: {filename}')
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

                    if 'test' in filename: # verify file with test -> 'file_with_tests'
                        row.append(1)
                    else:
                        row.append(0)
                    rows.append(row)
                except SyntaxError as ex:
                    # salvar os arquivos não processados
                    print('erro', python_file) 
                    count = count + 1
                # rows.append(row)
            
            projects_problems.append([project_name,  len(rows), count])
            print(f'{project_name}: finished, files: {len(rows)}; erros: {count}')
            # """
            # [print(a) for a in rows]
    writer = WriterCSV(name=f'test_excludes_{project_name.replace("/","_")}', path="analysis")
    writer.write(head=heads, rows=rows) 
    
    # writer = WriterCSV(name="problems_excludes", path="analysis")
    # writer.write(head=head_problems, rows=projects_problems) 