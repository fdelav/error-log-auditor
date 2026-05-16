import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURACIÓN ---
# Usa la "Test URL" de tu nodo Webhook en n8n
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/8dd2d54a-3de8-4904-a053-42e0bbb89cf7"
# Ruta al log de XAMPP (usa 'r' antes de la comilla para evitar errores de backslash)
LOG_PATH = r"C:\xampp\apache\logs\error.log"

class LogHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_position = self.get_file_size()

    def get_file_size(self):
        try:
            with open(LOG_PATH, 'r') as f:
                f.seek(0, 2)
                return f.tell()
        except FileNotFoundError:
            return 0

    def on_modified(self, event):
        # Verificamos que el evento sea específicamente sobre nuestro archivo
        if event.src_path == LOG_PATH:
            self.process_new_lines()

    def process_new_lines(self):
        with open(LOG_PATH, 'r') as f:
            f.seek(self.last_position)
            lineas_nuevas = f.readlines()
            self.last_position = f.tell()

            for linea in lineas_nuevas:
                linea = linea.strip()
                if linea: # Evitar enviar líneas vacías
                    self.enviar_a_n8n(linea)

    def enviar_a_n8n(self, texto_log):
        import re

        # Parser para formato syslog: "Mon Day HH:MM:SS hostname process[pid]: [type] IP: X.X.X.X Port: YYYY - message"
        # Y para nmap simulado: "Mon Day HH:MM:SS nmap-simulator nmap[pid]: [scan] IP: X.X.X.X Ports: A,B,C Status: open - NMAP SIMULATED"
        scan_pattern = r'^(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(\S+)\[(\d+)\]:\s+\[(\w+)\]\s+IP:\s+([\d.]+)\s+Ports:\s+([\d,]+)\s+Status:\s+(\w+)\s+-\s+(.*)$'
        syslog_pattern = r'^(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(\S+)\[(\d+)\]:\s+\[(\w+)\]\s+IP:\s+([\d.]+)\s+Port:\s+(\d+)\s+-\s+(.*)$'

        scan_match = re.match(scan_pattern, texto_log)
        syslog_match = re.match(syslog_pattern, texto_log)

        if scan_match:
            timestamp, hostname, process, pid, log_type, ip, ports, status, message = scan_match.groups()
            payload = {
                "timestamp": timestamp,
                "hostname": hostname,
                "process": process,
                "pid": pid,
                "log_type": "scan",
                "ip": ip,
                "ports": ports,
                "status": status,
                "message": message,
                "log_raw": texto_log
            }
        elif syslog_match:
            timestamp, hostname, process, pid, log_type, ip, port, message = syslog_match.groups()
            payload = {
                "timestamp": timestamp,
                "hostname": hostname,
                "process": process,
                "pid": pid,
                "log_type": log_type,
                "ip": ip,
                "port": port,
                "message": message,
                "log_raw": texto_log
            }
        else:
            payload = {
                "log_raw": texto_log,
                "error": "No se pudo parsear el log"
            }

        try:
            res = requests.get(N8N_WEBHOOK_URL, json=payload)
            log_type = payload.get('log_type', '?')
            print(f" [OK] Enviado a n8n |Tipo: {log_type}|Status: {res.status_code}")
        except Exception as e:
            print(f" [X] Error conectando con n8n: {e}")

if __name__ == "__main__":
    print(f"--- Iniciando monitoreo en: {LOG_PATH} ---")
    event_handler = LogHandler()
    observer = Observer()
    
    # IMPORTANTE: Watchdog monitorea la CARPETA, no el archivo directamente
    import os
    folder_to_watch = os.path.dirname(LOG_PATH)
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()