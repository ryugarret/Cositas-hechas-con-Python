import pytube
from pytube.cli import on_progress
import http.client
import time
import os
import re

inicio = True
descargando = True
comandos = ["cancion", "video", "lista", "canal", "salir", "exit", "ayuda"]
error = "Se ha producido algún error al leer la fuente de la descarga, saltando descarga"

def descargavideo(video):
    print("Descargando:\n")
    video.streams.get_highest_resolution().download(os.getcwd())
    print("\n")

print("""\n\n
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
\n\n""")
accion = input(
    """Bienvenido a la descargadera de Ryu, ¿Qué necesitas hoy?:
Cancion: descarga el audio de un video
Video: descarga un único video
Lista: descarga una lista de reproducción
Canal: descarga todo un canal de youtube
"""
).lower()

while descargando:

    link = ""

    if inicio == True:
        inicio = False
    else:
        accion = input("\n¿Video, lista o canal?\n").lower()

    if accion not in comandos:
        print("\nAcción incorrecta, escribe ayuda para más información")
    elif accion == "salir" or accion == "exit":
        accion = input("¿Estás seguro de que quieres irte?\n").lower()
        if accion == "si" or accion == "sí" or accion == "yes":
            print("¡Nos vemos! ^-^")
            descargando = False
            time.sleep(3)
        else:
            print("Puedes quedarte el tiempo que quieras :)\n")
    elif accion == "ayuda" or accion == "help":
        print(
            "Bienvenido a la descargadera de Ryu, ¿Qué necesitas hoy?:\nCancion: descarga el audio de un video\nVideo: descarga un único video\nLista: descarga una lista de reproducción\nCanal: descarga todo un canal de youtube\n"
        )

    while accion == "cancion":

        link = input("escribe el link completo al video que quieras descargar\n")
        video = pytube.YouTube(link, on_progress_callback=on_progress)
        video._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        print("Título: ", video.title)
        respuesta = input("\n¿Es este el video cuya canción quieres descargar? Y/N\n").lower()

        if respuesta == "y" or respuesta == "s" or respuesta == "si" or respuesta == "sí" or respuesta == "yes":
            try:
                print("Descargando:\n")
                cancion = video.streams.get_audio_only()
                audio = cancion.download(os.getcwd())
                base, ext = os.path.splitext(audio)
                amp3 = base + ".mp3"
                os.rename(audio, amp3)
                print("\n")
            except http.client.IncompleteRead:
                print(error)
                pass
        accion = ""

    while accion == "video":

        link = input("escribe el link completo al video que quieras descargar\n")
        video = pytube.YouTube(link, on_progress_callback=on_progress)
        video._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        print("Título: ", video.title)
        respuesta = input("\n¿Es este el video que quieres descargar? Y/N\n").lower()

        if respuesta == "y" or respuesta == "s" or respuesta == "si" or respuesta == "sí" or respuesta == "yes":
            try:
                descargavideo(video)
            except http.client.IncompleteRead:
                print(error)
                pass
        accion = ""

    while accion == "lista":

        link = input("escribe el link completo a la lista que quieras descargar\n")
        lista = pytube.Playlist(link)
        print("Título: ", lista.title)
        lista._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        print("El número de videos en ésta lista es: ", len(lista.video_urls))
        respuesta = input("\n¿Esta ese la lista que quieres descargar? Y/N\n").lower()

        if respuesta == "y" or respuesta == "s" or respuesta == "si" or respuesta == "sí" or respuesta == "yes":
            for url in lista.video_urls:
                print(url)
                video = pytube.YouTube(url, on_progress_callback=on_progress)
                print("\nEncontrado: ", video.title)
                respuesta = input("\n¿Descargar este video de la lista? Y/N\n").lower()
                if respuesta == "y" or respuesta == "s" or respuesta == "si" or respuesta == "sí" or respuesta == "yes":
                    try:
                        descargavideo(video)
                    except http.client.IncompleteRead:
                        print(error)
                        pass
        accion = ""

    while accion == "canal":


        link = input("escribe el link completo del canal que quieras descargar\n")
        canal = pytube.Channel(link)
        print("Título: ", canal.channel_name)
        respuesta = input("\n¿Este ese el canal cuyos videos que quieres descargar? Y/N\n").lower()

        if respuesta == "y" or respuesta == "s" or respuesta == "si" or respuesta == "sí" or respuesta == "yes":
            for url in canal.video_urls:
                print(url)
                video = pytube.YouTube(url, on_progress_callback=on_progress)
                print("\nEncontrado: ", video.title)
                respuesta = input("\n¿Descargar este video del canal? Y/N\n").lower()
                if respuesta == "y" or respuesta == "s" or respuesta == "si" or respuesta == "sí" or respuesta == "yes":
                    try:
                        descargavideo(video)
                    except http.client.IncompleteRead:
                        print(error)
                        pass
        accion = ""