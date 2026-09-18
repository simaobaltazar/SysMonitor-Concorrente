import tkinter as tk
import queue

class ResourceMonitorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Monitor de Recursos - Alarmes")
        self.root.geometry("500x300")

        # Área de texto onde vão aparecer os alarmes
        self.text_area = tk.Text(self.root, state='disabled', bg='black', fg='red', font=('Consolas', 10))
        self.text_area.pack(expand=True, fill='both', padx=10, pady=10)

        # Fila thread-safe para receber mensagens das threads consumidoras
        self.message_queue = queue.Queue()

        # Inicia a verificação contínua de novas mensagens (a cada 100ms)
        self.root.after(100, self._process_messages)

    def add_alert(self, message):
        """
        Método chamado pelos Consumidores.
        Adiciona uma mensagem de alerta à interface gráfica.
        """
        self.message_queue.put(message)

    def _process_messages(self):
        """
        Método interno. Verifica a fila e atualiza o ecrã de forma segura.
        """
        while not self.message_queue.empty():
            msg = self.message_queue.get()
            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"[ALERTA] {msg}\n")
            self.text_area.see(tk.END) # Faz scroll automático para baixo
            self.text_area.config(state='disabled')

        # Volta a agendar a verificação para daqui a 100ms
        self.root.after(100, self._process_messages)

    def start(self):
        """
        Inicia o ciclo principal (mainloop) da interface gráfica.
        Atenção: este método é bloqueante.
        """
        self.root.mainloop()