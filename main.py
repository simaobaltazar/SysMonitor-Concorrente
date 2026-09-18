import logging
import threading

from monitoring_manager import MonitoringManager
from resource_monitor_gui import ResourceMonitorGUI

logging.basicConfig(
    filename='system_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(threadName)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def graceful_shutdown(manager):

    while True:
        comando = input("Type 'stop' to terminate: ").strip().lower()
        if comando == "stop":
            break

    manager.stop_monitoring()

gui = ResourceMonitorGUI()

manager = MonitoringManager(gui)

gui.root.protocol("WM_DELETE_WINDOW", manager.stop_monitoring)

manager.start_monitoring()

gui.start()