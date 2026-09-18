import random

def get_cpu_load():
    """
    Retorna a percentagem simulada de carga do CPU (0.0 a 100.0).
    Alarme: > 50%
    """
    # Gera um valor na maioria das vezes normal, mas ocasionalmente alto
    return random.uniform(20.0, 95.0)

def get_free_ram_percentage():
    """
    Retorna a percentagem simulada de memória RAM livre (0.0 a 100.0).
    Alarme: < 10%
    """
    # Gera um valor na maioria das vezes normal, mas ocasionalmente muito baixo
    return random.uniform(5.0, 60.0)

def get_available_disk_percentage():
    """
    Retorna a percentagem simulada de espaço em disco disponível (0.0 a 100.0).
    Alarme: < 20%
    """
    # Gera um valor aleatório entre 10% e 50%
    return random.uniform(10.0, 50.0)

# Nota: Se mais tarde quiseres ler os valores reais do teu computador em vez 
# de simular, podes instalar a biblioteca 'psutil' (pip install psutil) e 
# substituir estas funções pelos métodos reais (ex: psutil.cpu_percent()).