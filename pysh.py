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
        prompt = custom_prompt
    else:
        if usar_colores:
            usuario_coloreado = '\033[0;31m' + obtener_usuario() + '\033[0m'
            equipo_coloreado = '\033[0;34m' + os.uname()[1] + '\033[0m'
            ruta_coloreada = '\033[0;32m' + obtener_directorio_actual() + '\033[0m'
            linea_inicio = '\033[0;36m┌─\033[0m'
            linea_fin = '\033[0;36m└\033[0m'
            if oneline:
                prompt = f"{usuario_coloreado}@{equipo_coloreado}:{ruta_coloreada} "
            else:
                prompt = f"{linea_inicio}{usuario_coloreado}@{equipo_coloreado}:{ruta_coloreada}\n{linea_fin}"
            prompt += '\033[0;32m$\033[0m '
        else:
            if oneline:
                prompt = f"{obtener_usuario()}@{os.uname()[1]}:{obtener_directorio_actual()}$ "
            else:
                prompt = f"{obtener_usuario()}@{os.uname()[1]}\n{obtener_directorio_actual()}\n$ "
    return prompt

def emular_shell(usar_colores, oneline, custom_prompt=None):
    history_file = os.path.join(os.path.expanduser("~"), ".shell_history")
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    while True:
        prompt = obtener_prompt(usar_colores, oneline, custom_prompt)
        comando = input(prompt)
        if not comando.strip():
            continue
        if comando == "!!":
            try:
                comando = readline.get_history_item(readline.get_current_history_length())
            except IndexError:
                print("No hay comandos en el historial")
                continue
        elif comando.startswith("!"):
            try:
                idx = int(comando[1:])
                comando = readline.get_history_item(idx)
            except (ValueError, IndexError):
                print("Índice de historial no válido")
                continue
        else:
            readline.add_history(comando)
        if comando.lower() == "cd":
            cambiar_directorio("")
        elif comando.lower().startswith("cd "):
            ruta = comando[3:]
            cambiar_directorio(ruta)
        elif comando.lower() == "exit":
            readline.write_history_file(history_file)
            break
        else:
            os.system(comando)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Shell Emulator')
    parser.add_argument('--nocolors', action='store_true', help='Deshabilitar los colores del prompt')
    parser.add_argument('--oneline', action='store_true', help='Usar el formato de una sola línea para el prompt')
    parser.add_argument('--customprompt', action='store_true', help='Usar el prompt personalizado')
    args = parser.parse_args()

    usar_colores = not args.nocolors
    oneline = args.oneline
    custom_prompt = None

    if args.customprompt:
        if os.path.exists('.pyshrc'):
            with open('.pyshrc', 'r') as file:
                custom_prompt = file.read()
        else:
            with open('.pyshrc', 'w') as file:
                custom_prompt = obtener_prompt(usar_colores, oneline)
                file.write(custom_prompt)

    if not any(vars(args).values()):
        oneline = False

    emular_shell(usar_colores, oneline, custom_prompt)
