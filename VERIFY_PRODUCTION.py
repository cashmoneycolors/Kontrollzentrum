#!/usr/bin/env python3
"""
✅ KONTROLLZENTRUM - PRODUCTION VERIFICATION
Verifies all systems are ready for production
"""

import sys
import os
import subprocess
from datetime import datetime

class ProductionVerifier:
    def __init__(self):
        self.checks = []
        self.passed = 0
        self.failed = 0
        
    def check(self, name, condition, details=""):
        """Führt einen Check durch"""
        status = "✅" if condition else "❌"
        self.checks.append((name, condition, details))
        if condition:
            self.passed += 1
        else:
            self.failed += 1
        print(f"{status} {name}")
        if details and not condition:
            print(f"   → {details}")
    
    def verify_system(self):
        """Prüft System-Anforderungen"""
        print("\n" + "="*60)
        print("🖥️  SYSTEM REQUIREMENTS")
        print("="*60)
        
        # Python Version
        py_version = sys.version_info
        self.check(
            "Python 3.9+",
            py_version.major >= 3 and py_version.minor >= 9,
            f"Aktuell: {py_version.major}.{py_version.minor}"
        )
        
        # Disk Space
        import shutil
        disk = shutil.disk_usage("/")
        self.check(
            "Disk Space (>1GB)",
            disk.free > 1e9,
            f"Verfügbar: {disk.free / 1e9:.1f}GB"
        )
        
        # RAM
        import psutil
        memory = psutil.virtual_memory()
        self.check(
            "RAM (>512MB)",
            memory.available > 512e6,
            f"Verfügbar: {memory.available / 1e6:.0f}MB"
        )
    
    def verify_dependencies(self):
        """Prüft Dependencies"""
        print("\n" + "="*60)
        print("📦 DEPENDENCIES")
        print("="*60)
        
        deps = {
            "streamlit": "Web UI",
            "uvicorn": "API Server",
            "sqlalchemy": "Database ORM",
            "pandas": "Data Processing",
            "psutil": "System Monitoring",
            "fastapi": "API Framework",
        }
        
        for dep, desc in deps.items():
            try:
                __import__(dep)
                self.check(f"{dep} ({desc})", True)
            except ImportError:
                self.check(f"{dep} ({desc})", False, "pip install -r requirements.txt")
    
    def verify_files(self):
        """Prüft erforderliche Dateien"""
        print("\n" + "="*60)
        print("📁 REQUIRED FILES")
        print("="*60)
        
        files = {
            "main.py": "Main entry point",
            ".env": "Configuration",
            "requirements.txt": "Dependencies",
            "modules/": "Modules directory",
            "core/": "Core systems",
            "tests/": "Tests directory",
        }
        
        for file, desc in files.items():
            exists = os.path.exists(file)
            self.check(f"{file} ({desc})", exists)
    
    def verify_modules(self):
        """Prüft Module"""
        print("\n" + "="*60)
        print("📦 MODULES")
        print("="*60)
        
        modules_path = "modules"
        if os.path.exists(modules_path):
            modules = [f[:-3] for f in os.listdir(modules_path) 
                      if f.endswith(".py") and not f.startswith("__")]
            self.check(f"Modules found ({len(modules)})", len(modules) > 0)
            
            # Check key modules
            key_modules = [
                "ai_assistant",
                "data_analytics",
                "email_automation",
                "customer_crm",
                "api_integration",
            ]
            
            for mod in key_modules:
                exists = mod in modules
                self.check(f"  → {mod}", exists)
        else:
            self.check("Modules directory", False)
    
    def verify_core_systems(self):
        """Prüft Core-Systeme"""
        print("\n" + "="*60)
        print("⚙️  CORE SYSTEMS")
        print("="*60)
        
        core_files = {
            "core/database.py": "Database",
            "core/auth.py": "Authentication",
            "core/health_monitor.py": "Health Monitor",
            "core/api_gateway.py": "API Gateway",
            "core/logging.py": "Logging",
        }
        
        for file, name in core_files.items():
            exists = os.path.exists(file)
            self.check(f"{name} ({file})", exists)
    
    def verify_configuration(self):
        """Prüft Konfiguration"""
        print("\n" + "="*60)
        print("⚙️  CONFIGURATION")
        print("="*60)
        
        # .env file
        env_exists = os.path.exists(".env")
        self.check(".env file", env_exists)
        
        if env_exists:
            with open(".env", "r") as f:
                content = f.read()
                self.check("  → ENVIRONMENT set", "ENVIRONMENT" in content)
                self.check("  → DEBUG set", "DEBUG" in content)
    
    def verify_database(self):
        """Prüft Database"""
        print("\n" + "="*60)
        print("🗄️  DATABASE")
        print("="*60)
        
        db_file = "kontrollzentrum.db"
        db_exists = os.path.exists(db_file)
        self.check("Database file", db_exists, "Will be created on first run")
        
        if db_exists:
            import sqlite3
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                self.check(f"  → Tables ({len(tables)})", len(tables) > 0)
                conn.close()
            except Exception as e:
                self.check("Database integrity", False, str(e))
    
    def verify_scripts(self):
        """Prüft Deployment-Scripts"""
        print("\n" + "="*60)
        print("🚀 DEPLOYMENT SCRIPTS")
        print("="*60)
        
        scripts = {
            "PRODUCTION_START.py": "Launcher",
            "PRODUCTION_MONITOR.py": "Monitor",
            "PRODUCTION_DEPLOY.bat": "Windows Batch",
            "VERIFY_PRODUCTION.py": "Verification",
        }
        
        for script, desc in scripts.items():
            exists = os.path.exists(script)
            self.check(f"{script} ({desc})", exists)
    
    def verify_documentation(self):
        """Prüft Dokumentation"""
        print("\n" + "="*60)
        print("📖 DOCUMENTATION")
        print("="*60)
        
        docs = {
            "README.md": "Project Overview",
            "PRODUCTION_STATUS.md": "Status",
            "PRODUCTION_CHECKLIST.md": "Checklist",
            "PRODUCTION_OPERATIONS.md": "Operations",
        }
        
        for doc, desc in docs.items():
            exists = os.path.exists(doc)
            self.check(f"{doc} ({desc})", exists)
    
    def print_summary(self):
        """Zeigt Zusammenfassung"""
        print("\n" + "="*60)
        print("📊 VERIFICATION SUMMARY")
        print("="*60)
        
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        print(f"✅ Passed:  {self.passed}/{total}")
        print(f"❌ Failed:  {self.failed}/{total}")
        print(f"📊 Score:   {percentage:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 ALL CHECKS PASSED - READY FOR PRODUCTION!")
            return True
        else:
            print(f"\n⚠️  {self.failed} check(s) failed - Please fix before deployment")
            return False
    
    def run(self):
        """Führt alle Checks durch"""
        print("\n" + "="*60)
        print("✅ KONTROLLZENTRUM - PRODUCTION VERIFICATION")
        print("="*60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        
        self.verify_system()
        self.verify_dependencies()
        self.verify_files()
        self.verify_modules()
        self.verify_core_systems()
        self.verify_configuration()
        self.verify_database()
        self.verify_scripts()
        self.verify_documentation()
        
        ready = self.print_summary()
        
        print("\n" + "="*60)
        if ready:
            print("🚀 Next: python PRODUCTION_START.py")
        else:
            print("🔧 Fix issues and run again: python VERIFY_PRODUCTION.py")
        print("="*60 + "\n")
        
        return 0 if ready else 1

def main():
    verifier = ProductionVerifier()
    sys.exit(verifier.run())

if __name__ == "__main__":
    main()
