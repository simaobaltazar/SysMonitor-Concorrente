import logging
import time
import threading
from queue import Empty, Queue
from concurrent.futures import ThreadPoolExecutor
from resource_monitor_utils import get_available_disk_percentage, get_cpu_load, get_free_ram_percentage

class MonitoringManager:
    def __init__(self, gui):
        self.gui = gui
        
        self.queue_size = 20
        self.num_consumers = 3
        self.shared_queue = Queue(maxsize=self.queue_size)
        
        self.stop_event = threading.Event()
        
        self.last_cpu_time = time.time()
        self.last_ram_time = time.time()
        self.last_disk_time = time.time()
        self.last_consumer_time = time.time()

        self.producers_pool = ThreadPoolExecutor(max_workers=3)
        self.consumers_pool = ThreadPoolExecutor(max_workers=self.num_consumers)

    def _cpu_producer(self):
        while not self.stop_event.is_set():
            cpu_value = get_cpu_load()
            self.shared_queue.put(("cpu", cpu_value))
            self.last_cpu_time = time.time()
            time.sleep(0.1)

    def _ram_producer(self):
        while not self.stop_event.is_set():
            ram_value = get_free_ram_percentage()
            self.shared_queue.put(("free_ram", ram_value))
            self.last_ram_time = time.time()
            time.sleep(0.1)

    def _disk_producer(self):
        while not self.stop_event.is_set():
            disk_value = get_available_disk_percentage()
            self.shared_queue.put(("free_disk", disk_value))
            self.last_disk_time = time.time()
            time.sleep(0.1)

    def _consumer(self):
        while not self.stop_event.is_set():
            try:
                item_type, value = self.shared_queue.get(timeout=1)
                self.last_consumer_time = time.time()

                if item_type == "cpu":
                    self.gui.root.after(0, self.gui.update_cpu_graph, value)

                if item_type == "cpu" and value > 50:
                    self.gui.add_alert(f"HIGH CPU LOAD: {value:.2f}%")
                    logging.warning(f"High CPU threshold exceeded: {value:.2f}%")
                
                elif item_type == "free_ram" and value < 10:
                    self.gui.add_alert(f"LOW FREE RAM: {value:.2f}%")
                    logging.warning(f"Low RAM threshold exceeded: {value:.2f}%")
                
                elif item_type == "free_disk" and value < 20:
                    self.gui.add_alert(f"LOW DISK SPACE: {value:.2f}%")
                    logging.warning(f"Low Disk threshold exceeded: {value:.2f}%")
                    
            except Empty:

                pass

    def _watchdog(self):
        while not self.stop_event.is_set():
            time.sleep(1)
            now = time.time()

            if now - self.last_cpu_time > 10:
                self.gui.add_alert("RESTARTING CPU PRODUCER")
                self.producers_pool.submit(self._cpu_producer)
                self.last_cpu_time = now

            if now - self.last_ram_time > 10:
                self.gui.add_alert("RESTARTING RAM PRODUCER")
                self.producers_pool.submit(self._ram_producer)
                self.last_ram_time = now

            if now - self.last_disk_time > 10:
                self.gui.add_alert("RESTARTING DISK PRODUCER")
                self.producers_pool.submit(self._disk_producer)
                self.last_disk_time = now

            if now - self.last_consumer_time > 30:
                self.gui.add_alert("RESTARTING CONSUMER")
                self.consumers_pool.submit(self._consumer)
                self.last_consumer_time = now

    def start_monitoring(self):
        logging.info("Starting Monitoring System...")
        self.producers_pool.submit(self._cpu_producer)
        self.producers_pool.submit(self._ram_producer)
        self.producers_pool.submit(self._disk_producer)

        for _ in range(self.num_consumers):
            self.consumers_pool.submit(self._consumer)

        self.watchdog_thread = threading.Thread(target=self._watchdog, daemon=True)
        self.watchdog_thread.start()

    def stop_monitoring(self):
        logging.info("Shutting down system...")
        self.stop_event.set()
        
        self.producers_pool.shutdown(wait=False)
        self.consumers_pool.shutdown(wait=False)

        self.gui.root.quit()     
        self.gui.root.destroy()
        
        logging.info("System terminated successfully.")