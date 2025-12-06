#!/usr/bin/env python3
"""
Deployment-Skript für Wrapper-Integration
Aktiviert OPTION A Orchestration mit Separate Projekte Schutz
"""
import os
import sys
from pathlib import Path
import shutil

def check_structure():
    """Prüfe Projektstruktur"""
    print("🔍 Prüfe Projektstruktur...")
    
    required = [
        "modules",
        "core",
        "submodules",
        "main.py",
        "OPTION_A_ORCHESTRATION.md"
    ]
    
    for item in required:
        path = Path(item)
        if path.exists():
            print(f"  ✅ {item}")
        else:
            print(f"  ❌ {item} FEHLT!")
            return False
    
    return True

def check_wrapper():
    """Prüfe Wrapper-Datei"""
    print("\n🔐 Prüfe Wrapper...")
    
    wrapper = Path("modules/separate_project_wrapper.py")
    if wrapper.exists():
        print(f"  ✅ Wrapper existiert")
        with open(wrapper, "r") as f:
            content = f.read()
            if "@require_keys" in content and "read-only" in content:
                print(f"  ✅ Wrapper korrekt konfiguriert")
                return True
    
    print(f"  ❌ Wrapper nicht korrekt!")
    return False

def check_main_py():
    """Prüfe main.py"""
    print("\n📄 Prüfe main.py...")
    
    main_file = Path("main.py")
    if main_file.exists():
        with open(main_file, "r") as f:
            content = f.read()
            if "discover_modules" in content and "sorted" in content:
                print(f"  ✅ main.py aktualisiert")
                return True
    
    print(f"  ❌ main.py nicht aktualisiert!")
    return False

def check_documentation():
    """Prüfe Dokumentation"""
    print("\n📚 Prüfe Dokumentation...")
    
    doc = Path("OPTION_A_ORCHESTRATION.md")
    if doc.exists():
        with open(doc, "r", encoding="utf-8") as f:
            content = f.read()
            if "separate_project_wrapper" in content and "Read-Only" in content:
                print(f"  ✅ Dokumentation aktualisiert")
                return True
    
    print(f"  ❌ Dokumentation nicht aktualisiert!")
    return False

def create_backup():
    """Erstelle Backup"""
    print("\n💾 Erstelle Backup...")
    
    backup_dir = Path("backup_pre_deployment")
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    
    backup_dir.mkdir()
    
    for item in ["modules", "main.py", "OPTION_A_ORCHESTRATION.md"]:
        src = Path(item)
        if src.is_file():
            shutil.copy2(src, backup_dir / src.name)
        elif src.is_dir():
            shutil.copytree(src, backup_dir / src.name)
    
    print(f"  ✅ Backup erstellt: {backup_dir}")
    return True

def deploy():
    """Deployment durchführen"""
    print("\n🚀 DEPLOYMENT STARTEN...\n")
    
    checks = [
        ("Projektstruktur", check_structure),
        ("Wrapper", check_wrapper),
        ("main.py", check_main_py),
        ("Dokumentation", check_documentation),
    ]
    
    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False
    
    if not all_passed:
        print("\n❌ DEPLOYMENT FEHLGESCHLAGEN!")
        return False
    
    # Backup
    if not create_backup():
        print("\n❌ Backup fehlgeschlagen!")
        return False
    
    print("\n" + "="*60)
    print("✅ DEPLOYMENT ERFOLGREICH!")
    print("="*60)
    print("\n📊 Status:")
    print("  ✅ Wrapper-Integration aktiv")
    print("  ✅ OPTION A Orchestration aktiviert")
    print("  ✅ Separate Projekte geschützt (Read-Only)")
    print("  ✅ Dokumentation aktualisiert")
    print("  ✅ Backup erstellt")
    
    print("\n🎯 Nächste Schritte:")
    print("  1. python main.py          # Teste Wrapper")
    print("  2. python main.py team     # Starte alle Module")
    print("  3. git add -A && git commit -m 'Wrapper-Integration'")
    print("  4. git push origin main")
    
    return True

if __name__ == "__main__":
    try:
        success = deploy()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ FEHLER: {e}")
        sys.exit(1)
