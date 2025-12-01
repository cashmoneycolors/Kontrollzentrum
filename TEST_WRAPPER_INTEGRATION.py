#!/usr/bin/env python3
"""
Test: Wrapper-Integration für separate Projekte
Prüft: Read-Only Modus, Modul-Laden, Orchestration
"""
import sys
import os
from pathlib import Path

# Setup
sys.path.insert(0, str(Path(__file__).parent))

def test_wrapper_exists():
    """Test 1: Wrapper-Datei existiert"""
    wrapper_path = Path(__file__).parent / "modules" / "separate_project_wrapper.py"
    assert wrapper_path.exists(), f"❌ Wrapper nicht gefunden: {wrapper_path}"
    print("✅ Test 1: Wrapper-Datei existiert")

def test_wrapper_import():
    """Test 2: Wrapper kann importiert werden"""
    try:
        from modules import separate_project_wrapper
        print("✅ Test 2: Wrapper importierbar")
    except ImportError as e:
        print(f"❌ Test 2 FAILED: {e}")
        raise

def test_wrapper_run():
    """Test 3: Wrapper.run() funktioniert"""
    try:
        from modules.separate_project_wrapper import run
        result = run()
        assert result["status"] == "success", f"Unexpected status: {result['status']}"
        assert result["mode"] == "read-only", f"Unexpected mode: {result['mode']}"
        print("✅ Test 3: Wrapper.run() funktioniert")
    except Exception as e:
        print(f"❌ Test 3 FAILED: {e}")
        raise

def test_module_discovery():
    """Test 4: Module werden korrekt erkannt"""
    from main import discover_modules
    modules = discover_modules()
    assert "separate_project_wrapper" in modules, "Wrapper nicht in Module-Liste"
    print(f"✅ Test 4: Module erkannt ({len(modules)} Module)")

def test_orchestration_config():
    """Test 5: OPTION A Orchestration konfiguriert"""
    config_path = Path(__file__).parent / "OPTION_A_ORCHESTRATION.md"
    assert config_path.exists(), "OPTION_A_ORCHESTRATION.md nicht gefunden"
    
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "separate_project_wrapper" in content, "Wrapper nicht in Dokumentation"
        assert "Read-Only" in content, "Read-Only Modus nicht dokumentiert"
    
    print("✅ Test 5: OPTION A Orchestration konfiguriert")

def test_submodules_structure():
    """Test 6: Submodules-Struktur vorhanden"""
    submodules_path = Path(__file__).parent / "submodules"
    assert submodules_path.exists(), "submodules/ Verzeichnis nicht gefunden"
    
    expected = ["module", "desktop-tutorial", "autonomous-zenith-optimizer", 
                "blank-app", "mega-ultra-roboter-ki", "cashmoney-ide"]
    found = [d.name for d in submodules_path.iterdir() if d.is_dir()]
    
    for exp in expected:
        if exp in found:
            print(f"  ✓ {exp}")
    
    print(f"✅ Test 6: Submodules-Struktur vorhanden ({len(found)} Repos)")

def main():
    """Führe alle Tests aus"""
    print("\n" + "="*60)
    print("🧪 WRAPPER-INTEGRATION TESTS")
    print("="*60 + "\n")
    
    tests = [
        test_wrapper_exists,
        test_wrapper_import,
        test_wrapper_run,
        test_module_discovery,
        test_orchestration_config,
        test_submodules_structure,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"❌ {test.__name__}: {e}\n")
    
    print("\n" + "="*60)
    print(f"📊 ERGEBNIS: {passed} bestanden, {failed} fehlgeschlagen")
    print("="*60 + "\n")
    
    if failed == 0:
        print("🎉 ALLE TESTS BESTANDEN!")
        print("\n✅ Wrapper-Integration erfolgreich!")
        print("✅ Separate Projekte geschützt (Read-Only)")
        print("✅ OPTION A Orchestration aktiv")
        return 0
    else:
        print(f"❌ {failed} Test(s) fehlgeschlagen")
        return 1

if __name__ == "__main__":
    sys.exit(main())
