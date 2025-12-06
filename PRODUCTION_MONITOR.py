#!/usr/bin/env python3
"""
🏥 KONTROLLZENTRUM - PRODUCTION MONITOR
Real-time System & Module Monitoring
"""

import sys
import os
import time
import psutil
import threading
from datetime import datetime
from collections import deque

class ProductionMonitor:
    def __init__(self):
        self.metrics = deque(maxlen=100)
        self.alerts = []
        self.running = True
        
    def get_system_metrics(self):
        """Sammelt System-Metriken"""
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/").percent,
            "processes": len(psutil.pids()),
        }
    
    def check_thresholds(self, metrics):
        """Prüft Schwellwerte"""
        alerts = []
        if metrics["cpu"] > 80:
            alerts.append(f"⚠️  CPU hoch: {metrics['cpu']:.1f}%")
        if metrics["memory"] > 80:
            alerts.append(f"⚠️  Memory hoch: {metrics['memory']:.1f}%")
        if metrics["disk"] > 90:
            alerts.append(f"⚠️  Disk voll: {metrics['disk']:.1f}%")
        return alerts
    
    def display_dashboard(self):
        """Zeigt Live-Dashboard"""
        os.system("cls" if os.name == "nt" else "clear")
        
        print("╔" + "═"*68 + "╗")
        print("║" + " "*15 + "🏥 PRODUCTION MONITOR - LIVE DASHBOARD" + " "*15 + "║")
        print("╚" + "═"*68 + "╝")
        print()
        
        if self.metrics:
            latest = self.metrics[-1]
            print(f"⏰ {latest['timestamp']}")
            print()
            print("📊 SYSTEM METRICS:")
            print(f"  CPU:       {latest['cpu']:>6.1f}% {'🟢' if latest['cpu'] < 80 else '🟡' if latest['cpu'] < 95 else '🔴'}")
            print(f"  Memory:    {latest['memory']:>6.1f}% {'🟢' if latest['memory'] < 80 else '🟡' if latest['memory'] < 95 else '🔴'}")
            print(f"  Disk:      {latest['disk']:>6.1f}% {'🟢' if latest['disk'] < 90 else '🟡' if latest['disk'] < 95 else '🔴'}")
            print(f"  Processes: {latest['processes']:>6} 🔵")
            print()
            
            # Trend
            if len(self.metrics) > 1:
                prev = self.metrics[-2]
                cpu_trend = "↑" if latest["cpu"] > prev["cpu"] else "↓" if latest["cpu"] < prev["cpu"] else "→"
                mem_trend = "↑" if latest["memory"] > prev["memory"] else "↓" if latest["memory"] < prev["memory"] else "→"
                print(f"📈 TREND: CPU {cpu_trend}  Memory {mem_trend}")
                print()
        
        # Alerts
        if self.alerts:
            print("🚨 ALERTS:")
            for alert in self.alerts[-5:]:
                print(f"  {alert}")
            print()
        else:
            print("✅ Keine Alerts")
            print()
        
        print("─" * 70)
        print("Drücke Ctrl+C zum Beenden | Aktualisiert alle 5 Sekunden")
    
    def monitor_loop(self):
        """Hauptüberwachungsschleife"""
        while self.running:
            try:
                metrics = self.get_system_metrics()
                self.metrics.append(metrics)
                
                alerts = self.check_thresholds(metrics)
                if alerts:
                    self.alerts.extend(alerts)
                
                self.display_dashboard()
                time.sleep(5)
                
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                print(f"❌ Fehler: {e}")
                time.sleep(5)
    
    def run(self):
        """Startet Monitor"""
        try:
            self.monitor_loop()
        except KeyboardInterrupt:
            pass
        finally:
            print("\n👋 Monitor beendet")

def main():
    monitor = ProductionMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
