import os
import sys
import argparse
import readline
import shutil

def obtener_usuario():
    return os.getenv('USER')

def obtener_directorio_actual():
    return os.getcwd()

def cambiar_directorio(ruta):
    if ruta == "":
        ruta = "/home/" + obtener_usuario()
    os.chdir(ruta)

def obtener_prompt(usar_colores, oneline, custom_prompt=None):
    if custom_prompt:
        return custom_prompt
    else:
        if usar_colores:
            usuario_coloreado = '\033[0;31m' + obtener_usuario() + '\033[0m'
            equipo_coloreado = '\033[0;34m' + os.uname()[1] + '\033[0m'
            ruta_coloreada = '\033[0;32m' + obtener_directorio_actual() + '\033[0m'
            linea_inicio = '\033[0;36m┌─\033[0m'
            linea_fin = '\033[0;36m└\033[0m'
            if oneline:
                return f"{usuario_coloreado}@{equipo_coloreado}:{ruta_coloreada} "
            else:
                return f"{linea_inicio}{usuario_coloreado}@{equipo_coloreado}:{ruta_coloreada}\n{linea_fin}\033[0;32m$\033[0m "
        else:
            if oneline:
                return f"{obtener_usuario()}@{os.uname()[1]}:{obtener_directorio_actual()}$ "
            else:
                return f"{obtener_usuario()}@{os.uname()[1]}\n{obtener_directorio_actual()}\n$ "

def emular_shell(usar_colores, oneline, custom_prompt=None):
    if custom_prompt is None:
        pyshrc_path = os.path.join(os.path.expanduser("~"), ".pyshrc")
        if os.path.exists(pyshrc_path):
            with open(pyshrc_path, "r") as file:
                custom_prompt = file.read()

    while True:
        prompt = obtener_prompt(usar_colores, oneline, custom_prompt)
        comando = input(prompt)
        if not comando.strip():
            continue
        if comando.lower() == "cd":
            cambiar_directorio("")
        elif comando.lower().startswith("cd "):
            ruta = comando[3:]
            cambiar_directorio(ruta)
        elif comando.lower() == "exit":
            break
        else:
            os.system(comando)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shell Emulator')
    parser.add_argument('--nocolors', action='store_true', help='Deshabilitar los colores del prompt')
    parser.add_argument('--oneline', action='store_true', help='Usar el formato de una sola línea para el prompt')
    args = parser.parse_args()

    usar_colores = not args.nocolors
    oneline = args.oneline

    emular_shell(usar_colores, oneline)
