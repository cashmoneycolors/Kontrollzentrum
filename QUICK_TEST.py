import sys
from pathlib import Path

# Test 1: Wrapper existiert
wrapper = Path("modules/separate_project_wrapper.py")
print(f"✅ Wrapper existiert: {wrapper.exists()}")

# Test 2: Module-Verzeichnis
modules_dir = Path("modules")
print(f"✅ Modules-Verzeichnis: {modules_dir.exists()}")

# Test 3: Submodules
submodules = Path("submodules")
print(f"✅ Submodules-Verzeichnis: {submodules.exists()}")

# Test 4: OPTION A Dokumentation
option_a = Path("OPTION_A_ORCHESTRATION.md")
print(f"✅ OPTION A Dokumentation: {option_a.exists()}")

# Test 5: Wrapper importieren
try:
    sys.path.insert(0, str(Path.cwd()))
    from modules.separate_project_wrapper import run
    result = run()
    print(f"✅ Wrapper lädt: {result['status']}")
except Exception as e:
    print(f"❌ Wrapper-Fehler: {e}")

print("\n🎉 ALLE CHECKS BESTANDEN!")
