from os import chdir, getcwd, path, system
from datetime import datetime


def create_log(file_used):
    home = path.expanduser("~")
    today = datetime.now().strftime('%Y-%m-%d')    
    chdir(home)
    if path.exists('.gaussian_files_used'):
        print('El archivo ya existe')
        with open('.gaussian_files_used', 'a') as f:
            f.write(f"{file_used} - {today} \n")
    else:
        with open('.gaussian_files_used', 'w') as f:
            f.write(f"{file_used} - {today} \n")
