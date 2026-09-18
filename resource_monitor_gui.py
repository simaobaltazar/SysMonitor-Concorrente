import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

class ResourceMonitorGUI:
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("System Resource Monitor")
        self.root.geometry("800x650")

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.cpu_data = deque([0]*60, maxlen=60) 
        
        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("CPU Load (%)")
        self.ax.set_ylim(0, 100)
        
        self.line, = self.ax.plot(self.cpu_data, color="#1f538d", linewidth=2)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().pack(pady=10, padx=10, fill="x")

        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="System Alerts Log", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(pady=(10, 5))

        self.alert_box = ctk.CTkTextbox(self.main_frame, height=150, state="disabled")
        self.alert_box.pack(pady=10, padx=10, fill="both", expand=True)

    def update_cpu_graph(self, cpu_value):

        self.cpu_data.append(cpu_value)
        self.line.set_ydata(self.cpu_data)
        self.canvas.draw_idle() 

    def add_alert(self, message):
        self.alert_box.configure(state="normal")
        self.alert_box.insert("end", message + "\n")
        self.alert_box.see("end")
        self.alert_box.configure(state="disabled")

    def start(self):
        self.root.mainloop()