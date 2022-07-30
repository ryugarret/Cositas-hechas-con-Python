import http.client
import time
import pathlib
import re

import pytube
from pytube.cli import on_progress

COMMANDS = ["cancion", "video", "lista", "canal", "salir", "exit", "ayuda"]
ERROR = "Se ha producido algún error al leer la fuente de la descarga, saltando descarga"
BANNER = """\n\n
     _     _                      _                  _                   _                 _             
    | |   | |           _        | |                | |                 | |               | |            
    | |___| | __  _   _| |_ _   _| | _   ____     _ | | ___  _ _ _ ____ | | ___   ____  _ | | ____  ____ 
    \__   __/ _ \| | | |  _) | | | || \ / _  )   / || |/ _ \| | | |  _ \| |/ _ \ / _  |/ || |/ _  )/ ___)
      _| |_| |_| | |_| | |_| |_| | |_) | (/ /   ( (_| | |_| | | | | | | | | |_| ( ( | ( (_| ( (/ /| |    
     (_____)\___/ \____|\___)____|____/ \____)   \____|\___/ \____|_| |_|_|\___/ \_||_|\____|\____)_|    

                             _              ______                                                                  
                            | |            (_____ \                                                                 
                            | | _  _   _    _____) )_   _ _   _                                                     
                            | || \( | | |  | ____  ( | | | | | |                                                    
                            | |_) ) |_| |  | |   | | |_| | |_| |                                                    
                            |____/ \__  |  |_|   |_|\__  |\____|                                                    
                                  (____/           (____/                                                           
    \n\n"""


def download_video(video: pytube.YouTube):
    try:
        print("Descargando:\n")
        video.streams.get_highest_resolution().download(str(pathlib.Path.cwd()))
        print("\n")
    except http.client.IncompleteRead:
        print(ERROR)


def is_yes(word: str) -> bool:
    return word in ["y", "s", "si", "sí", "yes"]


def main():
    downloading = True
    print(BANNER)
    accion = input(
        """Bienvenido a la descargadera de Ryu, ¿Qué necesitas hoy?:
    Cancion: descarga el audio de un video
    Video: descarga un único video
    Lista: descarga una lista de reproducción
    Canal: descarga todo un canal de youtube
    """
    ).lower()

    while downloading:
        if not accion:
            accion = input("\n¿Video, lista o canal?\n").lower()

        if accion not in COMMANDS:
            print("\nAcción incorrecta, escribe ayuda para más información")
        elif accion in ["salir", "exit"]:
            accion = input("¿Estás seguro de que quieres irte?\n").lower()
            if is_yes(accion):
                print("¡Nos vemos! ^-^")
                downloading = False
                time.sleep(3)
            else:
                print("Puedes quedarte el tiempo que quieras :)\n")
        elif accion in ["ayuda", "help"]:
            print(
                "Bienvenido a la descargadera de Ryu, ¿Qué necesitas hoy?:\n"
                "Cancion: descarga el audio de un video\n"
                "Video: descarga un único video\n"
                "Lista: descarga una lista de reproducción\n"
                "Canal: descarga todo un canal de youtube\n"
            )
        elif accion == "cancion":
            handle_song()
        elif accion == "video":
            handle_video()
        elif accion == "lista":
            handle_list()
        elif accion == "canal":
            handle_channel()
        accion = None


def handle_channel():
    link = input("escribe el link completo del canal que quieras descargar\n")
    canal = pytube.Channel(link)
    print("Título: ", canal.channel_name)
    confirmation = input("\n¿Este ese el canal cuyos videos que quieres descargar? Y/N\n").lower()

    if is_yes(confirmation):
        for url in canal.video_urls:
            print(url)
            video = pytube.YouTube(url, on_progress_callback=on_progress)
            print("\nEncontrado: ", video.title)
            confirmation = input("\n¿Descargar este video del canal? Y/N\n").lower()
            if is_yes(confirmation):
                download_video(video)


def handle_song():
    link = input("escribe el link completo al video que quieras descargar\n")
    video = pytube.YouTube(link, on_progress_callback=on_progress)
    video._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    print("Título: ", video.title)
    respuesta = input("\n¿Es este el video cuya canción quieres descargar? Y/N\n").lower()

    if is_yes(respuesta):
        try:
            print("Descargando:\n")
            cancion = video.streams.get_audio_only()
            audio = cancion.download(str(pathlib.Path.cwd()))
            audio = pathlib.Path.cwd().joinpath(audio)
            pathlib.Path(str(audio)).rename(audio.with_suffix('.mp3'))
            print("\n")
        except http.client.IncompleteRead:
            print(ERROR)


def handle_video():
    link = input("escribe el link completo al video que quieras descargar\n")
    video = pytube.YouTube(link, on_progress_callback=on_progress)
    video._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    print("Título: ", video.title)
    respuesta = input("\n¿Es este el video que quieres descargar? Y/N\n").lower()

    if is_yes(respuesta):
        download_video(video)


def handle_list():
    link = input("escribe el link completo a la lista que quieras descargar\n")
    lista = pytube.Playlist(link)
    print("Título: ", lista.title)
    lista._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    print("El número de videos en ésta lista es: ", len(lista.video_urls))
    respuesta = input("\n¿Esta ese la lista que quieres descargar? Y/N\n").lower()

    if is_yes(respuesta):
        for url in lista.video_urls:
            print(url)
            video = pytube.YouTube(url, on_progress_callback=on_progress)
            print("\nEncontrado: ", video.title)
            respuesta = input("\n¿Descargar este video de la lista? Y/N\n").lower()
            if is_yes(respuesta):
                download_video(video)


if __name__ == '__main__':
    main()