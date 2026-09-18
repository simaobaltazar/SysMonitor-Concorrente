import psutil
import os

def get_cpu_load():
    return psutil.cpu_percent(interval=None)

def get_free_ram_percentage():
    mem = psutil.virtual_memory()
    return 100.0 - mem.percent

def get_available_disk_percentage():
    caminho_raiz = os.path.abspath(os.sep)
    disco = psutil.disk_usage(caminho_raiz)
    
    return 100.0 - disco.percent