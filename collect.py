import ast
from get_repo import Repo
from monitor import MonitorVisitor, all_files
from writercsv import WriterCSV
from pathlib import Path


if __name__ == '__main__':
    # dir = '/Users/job/Documents/dev/doutorado/study/skip-platform/data/django/django'
    dir = '/Users/job/Documents/dev/doutorado/study/skip-platform/input'
    url = 'https://github.com/django/django'
    name = 'django'
    # repo = Repo('django',url)
    # local = repo.clone_at(dir)
    # print(local.commit_head())
    heads = [
        'project_name', 'project_version', 'file_path', 'file_modules',
        'file_modules_excludes'
    
    ]
    rows = []
    # row = []
    # row.append(repo.repo_name())
    # row.append(local.commit_head())
    
    # modules = set()
    libs = set()
    libs.add('os')
    libs.add('platform')
    libs.add('sys')
    for python_file in all_files(dir):
        row = []
        row.append('input')
        row.append('HEAD')
        # row.append(repo.repo_name())
        # row.append(local.commit_head())
        row.append(str(python_file).replace(dir,""))
        # print(file.replace(dir,""))
        print('processing: ', python_file)
        try:
            parser = ast.parse(open(python_file).read())
            monitor = MonitorVisitor()
            monitor.visit(parser)
            if not monitor.modules:
                row.append('')
                row.append(0)
                # continue
            else:
                # print('Módulos carregados com AST: ', python_file, ', '.join(list(monitor.modules)))
                row.append(', '.join(list(monitor.modules)))
                if libs.intersection(monitor.modules):
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