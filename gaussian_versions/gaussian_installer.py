from os import mkdir, path, system, chdir, getcwd, listdir
import tarfile
from shutil import copy2
import warnings

# Ignorar todas las advertencias
warnings.filterwarnings("ignore")

# Configuración inicial
system('clear')
print('*' * 44)
print('*** Iniciando la instalación de Gaussian ***')
print('*' * 44)

files = listdir('./versions')

print('Seleccione el archivo a instalar:')
for i, file in enumerate(files):
    print(f'{i}. {file}')

gaussian_file = int(input('>  '))
if gaussian_file >= len(files): 
    print('Selección inválida, cerrando instalador...')
    exit(1)
arch = files[gaussian_file]
print(f'\nSeleccionaste: {arch}')

selection = input('\nSeleccione la versión a instalar:\n1. Gaussian 09\n2. Gaussian 16\n3. Salir\n>  ')
if selection == '1':
    version = '09'
elif selection == '2':
    version = '16'
else:
    print('Saliendo del instalador...')
    exit(1)
    
installation_path = '/opt'  # Ruta de instalación
grp = f'gaussian{version}'          # Nombre del grupo
gaussian_path = f'{installation_path}/gaussian'
current_path = getcwd()
cwd = current_path.split('/')
home_dir = f"/{cwd[1]}/{cwd[2]}"
user = cwd[2]              # Usuario actual

try:
    print('Grupo: ', grp)
    # Cambiar a /etc y crear respaldos
    chdir('/etc')
    copy2('group', 'group.bk')
    copy2('gshadow', 'gshadow.bk')

    # Verificar si el GID ya existe
    for gid_generated in range(500, 1000):
        gid_exists = system(f'grep {gid_generated} group')
        if gid_exists == 256:
            gid = gid_generated
            break
        else:
            continue
    # Crear grupo y agregar usuarios
    system(f'groupadd -g {gid} {grp}')
    print(f'*** Grupo {grp} creado con GID {gid} ***\n')
    system(f'usermod -a -G {grp} {user}')
    print(f'Usuario {user} agregado al grupo {grp}')

    # Crear directorio de instalación si no existe
    chdir(current_path)
    if not path.exists(gaussian_path):
        mkdir(gaussian_path)

    # Extraer el archivo tar.gz
    try:
        print(f'*** Extrayendo archivo {arch} en {gaussian_path}... ***')
        if arch.split('.')[-1] == 'gz':
            with tarfile.open(f'./versions/{arch}', 'r:gz') as file_gz:
                file_gz.extractall(gaussian_path)
            print(f'*** Archivo {arch} extraído correctamente. ***')
        elif arch.split('.')[-1] == 'tbJ':
            with tarfile.open(f'./versions/{arch}', 'r:xz') as file_gz:
                file_gz.extractall(gaussian_path)
            print(f'*** Archivo {arch} extraído correctamente. ***')
        else:
            print('Formato no reconocido')
            exit(1)

    except Exception as e:
        print(f'Error al extraer el archivo: {e}')
        exit(1)

    # Ajustar permisos
    print('*** Configurando permisos para Gaussian ***')
    system(f'chown -R {user}:{grp} {gaussian_path}/g{version}')
    system(f'chmod -R 770 {gaussian_path}/g{version}')

    # Crear variables de entorno en .bashrc
    try:
        chdir(home_dir)
        with open('.bashrc', 'a') as bashrc:
            bashrc.write("\n# GAUSSIAN {version} VARIABLES\n")
            bashrc.write(f"export g{version}root={gaussian_path}\n")
            bashrc.write(f"export GAUSS_SCRDIR=/tmp\n")
            bashrc.write(f". $g{version}root/g{version}/bsd/g{version}.profile\n")
    except FileNotFoundError:
        print('No se encontró el archivo .bashrc en el directorio home.')
        exit(1)

    print('-' * 55)
    print('¡Instalación terminada! Ejecuta los siguientes comandos:')
    print('  cd\n  . .bashrc')

except Exception as e:
    print(f'Error inesperado: {e}')
    print('\n Uso: sudo python3 gaussian_installer.py gaussian.tar.gz...')
