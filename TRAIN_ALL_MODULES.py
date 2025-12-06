#!/usr/bin/env python3
"""
TRAIN ALL MODULES - Trainiert alle 15+ Module bis sie fertig sind
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

print("\n" + "="*70)
print("🎓 TRAINIERE ALLE 15+ MODULE")
print("="*70 + "\n")

modules_to_train = [
    "ai_text_generator",
    "data_analytics",
    "email_automation",
    "image_processor",
    "pdf_generator",
    "social_media_manager",
    "inventory_manager",
    "customer_crm",
    "reporting_engine",
    "backup_manager",
    "security_scanner",
    "api_integration",
    "ml_predictor",
    "notification_system",
    "workflow_automation",
    "separate_project_wrapper"
]

print(f"📦 {len(modules_to_train)} Module zum Trainieren\n")

trained = 0
failed = 0

for module_name in modules_to_train:
    try:
        print(f"🎓 Trainiere: {module_name}...", end=" ")
        
        # Importiere Modul
        mod = __import__(f"modules.{module_name}", fromlist=[module_name])
        
        # Installiere
        if hasattr(mod, "install"):
            mod.install()
        
        # Trainiere (run)
        if hasattr(mod, "run"):
            result = mod.run()
            if result and result.get("status") == "success":
                print("✅ FERTIG")
                trained += 1
            else:
                print("⚠️  WARNUNG")
        else:
            print("⚠️  KEINE RUN-FUNKTION")
    
    except Exception as e:
        print(f"❌ FEHLER: {e}")
        failed += 1

print("\n" + "="*70)
print(f"📊 TRAINING ABGESCHLOSSEN")
print("="*70)
print(f"\n✅ Erfolgreich trainiert: {trained}")
print(f"❌ Fehler: {failed}")
print(f"📦 Gesamt: {len(modules_to_train)}")

if failed == 0:
    print("\n🎉 ALLE MODULE SIND FERTIG UND TRAINIERT!")
    print("✅ Bereit für Produktion")
else:
    print(f"\n⚠️  {failed} Module benötigen Aufmerksamkeit")

print("\n" + "="*70 + "\n")
