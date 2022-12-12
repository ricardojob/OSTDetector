import ast
from get_repo import Repo
from monitor import MonitorVisitor, all_files
from writercsv import WriterCSV
from pathlib import Path
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
    dir = '/Users/job/Documents/dev/doutorado/study/skip-platform/data/django/django'
    url = 'https://github.com/django/django'
    # name = 'django'
    repo = Repo('django',url)
    local = repo.clone_at(dir)
    commit_hash= local.commit_head()
    return repo.name, commit_hash, dir

def clone(repo_name):
    dir = f'/Users/job/Documents/dev/doutorado/study/skip-platform/data/{repo_name}'
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
    libs.add('os')
    libs.add('platform')
    libs.add('sys')
    
    csv_filename = 'input-csv/projects_filted_dev.csv'
    # csv_filename = 'input-csv/projects_filted.csv'
    has_head_readed = False
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not has_head_readed: #skip head
                has_head_readed = True
                continue  
            
            # print(row[0])
            # project_name = row[0] 
            # project_hash = '1'
            # project_dir = '/Users/job/Documents/dev/doutorado/study/skip-platform/data/'+project_name
            project_name, project_hash, project_dir = clone(row[0])
    
            for python_file in all_files(project_dir):
                # if python_file.
                row = []
                row.append(project_name)
                row.append(project_hash)
                filename = str(python_file).replace(project_dir,"")
                row.append(filename)
                print(f'{project_name}: {filename}')
                
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
                # rows.append(row)
    writer = WriterCSV("test_excludes")
    writer.write(head=heads, rows=rows) 