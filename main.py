from queue import Queue
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from resource_monitor_utils import get_cpu_load, get_free_ram_percentage, get_available_disk_percentage
from resource_monitor_gui import ResourceMonitorGUI



TAMANHOFILA = 20
NUMCONSUMIDORES = 3

filaPartilhada = Queue(maxsize=TAMANHOFILA)

estado = True


# Tempo de atividade

ultimoCpu = time.time()
ultimoRam = time.time()
ultimoDisco = time.time()
ultimoConsumo = time.time()


gui = ResourceMonitorGUI()


# Produtores

def cpuProdutor(queue):

    global ultimoCpu

    while estado:

        valorCpu = get_cpu_load()

        queue.put(("cpu", valorCpu))

        ultimoCpu = time.time()

        time.sleep(0.1)


def ramLivreProdutor(queue):

    global ultimoRam

    while estado:

        valorRam = get_free_ram_percentage()

        queue.put(("ram livre", valorRam))

        ultimoRam = time.time()

        time.sleep(0.1)


def espacoDiscoProdutor(queue):

    global ultimoDisco

    while estado:

        valorDisco = get_available_disk_percentage()

        queue.put(("espaco livre no disco", valorDisco))

        ultimoDisco = time.time()

        time.sleep(0.1)


# Consumidores

def consumidores(queue, gui):

    global ultimoConsumo

    while estado:



        tipo, valor = queue.get(timeout=1)

        ultimoConsumo = time.time()

        if tipo == "cpu" and valor > 50:
            gui.add_alert(f"A carga da CPU está elevada: {valor:.2f}%")

        if tipo == "ram livre" and valor < 10:
            gui.add_alert(f"A quantidade de RAM livre está baixa: {valor:.2f}%")

        if tipo == "espaco livre no disco" and valor < 20:
            gui.add_alert(f"O espaço livre no disco está baixo: {valor:.2f}%")

        


# Therds Pools

produtoresThreadPool = ThreadPoolExecutor(max_workers=3)

consumidoresThreadPool = ThreadPoolExecutor(max_workers=NUMCONSUMIDORES)

# Iniciar


def iniciarProdutores():

    produtoresThreadPool.submit(cpuProdutor, filaPartilhada)

    produtoresThreadPool.submit(ramLivreProdutor, filaPartilhada)

    produtoresThreadPool.submit(espacoDiscoProdutor, filaPartilhada)


def iniciarConsumidores():

    for _ in range(NUMCONSUMIDORES):

        consumidoresThreadPool.submit(consumidores, filaPartilhada, gui)



def supervisao():

    global ultimoCpu
    global ultimoRam
    global ultimoDisco
    global ultimoConsumo

    while estado:

        time.sleep(1)

        agora = time.time()

        if agora - ultimoCpu > 10:
            gui.add_alert("Produtor CPU reiniciado")
            produtoresThreadPool.submit(cpuProdutor, filaPartilhada)
            ultimoCpu = agora

        if agora - ultimoRam > 10:
            gui.add_alert("Produtor RAM reiniciado")
            produtoresThreadPool.submit(ramLivreProdutor, filaPartilhada)
            ultimoRam = agora

        if agora - ultimoDisco > 10:
            gui.add_alert("Produtor DISCO reiniciado")
            produtoresThreadPool.submit(espacoDiscoProdutor, filaPartilhada)
            ultimoDisco = agora

        if agora - ultimoConsumo > 30:
            gui.add_alert("Consumidor reiniciado")
            consumidoresThreadPool.submit(consumidores, filaPartilhada, gui)
            ultimoConsumo = agora



def encerramentoGracioso():
    global estado

    while True:
        comando = input("Escreva 'chegadecpu' para terminar: ").strip().lower()
        
        if comando == "chegadecpu":
            break

    print("A encerrar sistema...")
    running = False

    time.sleep(1)

    produtoresThreadPool.shutdown(wait=False)
    consumidoresThreadPool.shutdown(wait=False)

    gui.root.after(0, gui.root.destroy) # fecha a gui

    print("Sistema terminado.")


iniciarProdutores()

iniciarConsumidores()


threadSupervisao = threading.Thread(target=supervisao, daemon=True)

threadSupervisao.start()


threadEncerramentoGracioso = threading.Thread(target=encerramentoGracioso)

threadEncerramentoGracioso.start()


gui.start()