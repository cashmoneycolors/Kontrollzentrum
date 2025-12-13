"""
Health Monitoring - System & Module Status
"""
import psutil
import time
from datetime import datetime

class HealthMonitor:
    def __init__(self):
        self.alerts = []
        self.module_times = {}
    
    def check_module_health(self, module_name):
        """Prüft Modul-Gesundheit"""
        start = time.time()
        try:
            import importlib
            mod = importlib.import_module(f"modules.{module_name}")
            elapsed = time.time() - start
            self.module_times[module_name] = elapsed
            
            status = "healthy" if elapsed < 5 else "slow" if elapsed < 10 else "dead"
            return {"status": status, "response_time": elapsed}
        except Exception as e:
            self.alerts.append(f"{module_name}: {e}")
            return {"status": "dead", "response_time": -1}
    
    def check_system_health(self):
        """Prüft System-Ressourcen"""
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        
        status = "healthy"
        if cpu > 80 or memory > 80 or disk > 90:
            status = "warning"
        if cpu > 95 or memory > 95 or disk > 95:
            status = "critical"
        
        return {
            "cpu": cpu,
            "memory": memory,
            "disk": disk,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }

monitor = HealthMonitor()
