# System Resource Monitor

[![NPM](https://img.shields.io/github/license/simaobaltazar/SysMonitor-Concorrente)](https://github.com/simaobaltazar/SysMonitor-Concorrente/blob/main/LICENSE) 

## Sobre o projeto

O System Resource Monitor é uma aplicação desktop desenvolvida em Python para a monitorização de hardware (CPU, RAM e Disco) em tempo real. O foco principal deste projeto não é apenas a exibição de dados, mas sim a aplicação de princípios avançados de **Sistemas Distribuídos e Programação Concorrente**.

O sistema foi desenhado para substituir os ciclos síncronos tradicionais por um padrão robusto de **Produtor-Consumidor**, garantindo segurança de memória (*thread-safety*), uma interface que não bloqueia e um sistema de tolerância a falhas capaz de recuperar *threads* automaticamente.

## Modelo Conceitual

O modelo foca-se na descentralização:
* **Produtores:** Recolhem as métricas de hardware de forma independente.
* **Fila Partilhada (Queue):** Atua como o canal único e seguro de comunicação entre as *threads*.
* **Consumidores:** Processam os dados da fila e delegam a atualização visual para a *thread* principal da GUI.
* **Watchdog:** Uma *daemon thread* que funciona como vigilante, detetando e reiniciando processos bloqueados através de *timeouts*.

## Tecnologias utilizadas
* **Python 3**
* **CustomTkinter** 
* **Matplotlib** 
* **psutil** 
* **Módulos Nativos:** `threading`, `concurrent.futures`, `queue`, `logging`

## Competências aplicadas
* Arquitetura Produtor-Consumidor
* Sincronização Segura de Threads (`threading.Event` e `queue.Queue`)
* Desenvolvimento de Interface Gráfica (CustomTkinter)
* Visualização de Dados em Tempo Real (Matplotlib)
* Implementação de Tolerância a Falhas e Recuperação (Watchdog)
* Persistência de Dados Thread-Safe (Logging)
* Encerramento Seguro de Processos (*Graceful Shutdown*)

## Como executar o projeto

### Pré-requisitos
* Python 3 instalado no teu sistema.

### Passos de execução

```bash
# clonar repositório
git clone [https://github.com/simaobaltazar/SysMonitor-Concorrente.git](https://github.com/simaobaltazar/SysMonitor-Concorrente.git)

# entrar na pasta do projeto
cd SysMonitor-Concorrente

# instalar as dependências necessárias
pip install customtkinter matplotlib psutil

# executar a aplicação
python main.py
```
### Autor
Simão Baltazar

Estudante de Engenharia Informática no Instituto Politécnico de Santarém.
