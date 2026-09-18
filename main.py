import threading

from monitoring_manager import MonitoringManager
from resource_monitor_gui import ResourceMonitorGUI


def graceful_shutdown(manager):

    while True:
        comando = input("Type 'stop' to terminate: ").strip().lower()
        if comando == "stop":
            break

    manager.stop_monitoring()

gui = ResourceMonitorGUI()

manager = MonitoringManager(gui)

manager.start_monitoring()

shutdown_thread = threading.Thread(target=graceful_shutdown, args=(manager,))
shutdown_thread.start()

gui.start()