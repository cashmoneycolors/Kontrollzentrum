#!/usr/bin/env python3
"""
Kontrollzentrum - PRODUCTION GRADE
===================================
Multi-Entry-Point System:
- CLI Mode: python main.py [module] [action]
- Team Mode: python main.py team
- API Gateway: python main.py api
- Health Check: python main.py health
- Streamlit UI: streamlit run main.py
"""

import sys
import os
import importlib
import argparse
import datetime
import asyncio
from core.database import db
from core.health_monitor import monitor
from core.rate_limiter import rate_limiter, cache

# Setup path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "modules"))
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)


def discover_modules():
    """Scannt modules/ nach Python-Dateien"""
    modules = []
    if not os.path.exists(modules_path):
        return modules

    for fname in os.listdir(modules_path):
        if (
            fname.endswith(".py")
            and not fname.startswith("__")
            and fname not in ["main.py", "api_server.py"]
        ):
            modules.append(fname[:-3])
    return modules


def get_capabilities(mod):
    """Ermittelt verfügbare Funktionen eines Moduls"""
    caps = []
    for cap in ["run", "install", "to_svg", "to_word", "describe"]:
        if hasattr(mod, cap):
            caps.append(cap)
    return caps


def run_streamlit_mode():
    """Startet Streamlit Zenith Controller"""
    import streamlit as st

    try:
        from core.zenith_controller import ZenithController
    except ModuleNotFoundError:
        st.error("Fehler: 'core/zenith_controller.py' nicht gefunden!")
        st.stop()
    except ImportError as e:
        st.error(f"Import-Fehler: {e}")
        st.stop()

    st.set_page_config(page_title="Zenith Kontrollzentrum", layout="wide")
    controller = ZenithController()
    controller.run()


def run_team_mode():
    """Team-Modus: Vollautomatische Installation & Ausführung aller Module"""
    log_lines = []
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_lines.append(f"[TEAM-MODUS] Autostart am {now}\n")

    module_names = discover_modules()
    modules = []

    # Module laden
    for module_name in module_names:
        try:
            mod = importlib.import_module(module_name)
            caps = get_capabilities(mod)
            modules.append({"name": module_name, "module": mod, "capabilities": caps})
        except Exception as e:
            print(f"[WARN] Modul {module_name} konnte nicht geladen werden: {e}")

    if not modules:
        print("Keine Module gefunden!")
        return

    # 1. Installation
    log_lines.append("[INSTALLATION]")
    install_results = []
    for m in modules:
        if "install" in m["capabilities"]:
            try:
                m["module"].install()
                msg = f"Modul: {m['name']:<20} Status: OK"
                print(msg)
                log_lines.append(msg)
                install_results.append((m["name"], "OK"))
            except Exception as e:
                msg = f"Modul: {m['name']:<20} Status: FEHLER ({e})"
                print(msg)
                log_lines.append(msg)
                install_results.append((m["name"], f"FEHLER: {e}"))

    ok_count = sum(1 for _, status in install_results if status == "OK")
    fail_count = len(install_results) - ok_count
    log_lines.append(
        f"[ZUSAMMENFASSUNG] Erfolgreich: {ok_count}  Fehlgeschlagen: {fail_count}\n"
    )

    # 2. Ausführung
    log_lines.append("[RUN]")
    run_results = []
    for m in modules:
        if "run" in m["capabilities"]:
            try:
                result = m["module"].run()
                if isinstance(result, str) and "demo" in result.lower():
                    msg = f"Modul: {m['name']:<20} Status: DEMO-MODUS"
                    run_results.append((m["name"], "DEMO"))
                else:
                    msg = f"Modul: {m['name']:<20} Status: OK"
                    run_results.append((m["name"], "OK"))
                print(msg)
                log_lines.append(msg)
            except Exception as e:
                msg = f"Modul: {m['name']:<20} Status: FEHLER ({e})"
                print(msg)
                log_lines.append(msg)
                run_results.append((m["name"], f"FEHLER: {e}"))

    ok_count = sum(1 for _, status in run_results if status == "OK")
    demo_count = sum(1 for _, status in run_results if status == "DEMO")
    fail_count = len(run_results) - ok_count - demo_count
    log_lines.append(
        f"[ZUSAMMENFASSUNG] OK: {ok_count}  Demo: {demo_count}  Fehler: {fail_count}\n"
    )

    # Log schreiben
    with open("team_log.txt", "a", encoding="utf-8") as f:
        for line in log_lines:
            f.write(line + "\n")

    print("\n[TEAM-MODUS] Abgeschlossen. Details: team_log.txt")


def run_api_mode():
    """Start API Gateway"""
    print("🚀 Starting API Gateway on http://0.0.0.0:8000")
    from core.api_gateway import app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_health_check():
    """Run health check on all modules"""
    print("🏥 Running health checks...\n")
    modules = discover_modules()
    
    for module_name in modules:
        health = monitor.check_module_health(module_name)
        status_icon = "✅" if health["status"] == "healthy" else "⚠️" if health["status"] == "slow" else "💀"
        print(f"{status_icon} {module_name}: {health['status']} ({health.get('response_time', 0):.2f}s)")
    
    print("\n📊 System Health:")
    sys_health = monitor.check_system_health()
    print(f"  CPU: {sys_health['cpu']:.1f}%")
    print(f"  Memory: {sys_health['memory']:.1f}%")
    print(f"  Disk: {sys_health['disk']:.1f}%")
    print(f"  Status: {sys_health['status']}")
    
    if monitor.alerts:
        print(f"\n⚠️  Alerts ({len(monitor.alerts)}):")
        for alert in monitor.alerts[-5:]:
            print(f"  - {alert}")

def run_cli_mode():
    """CLI-Modus mit interaktiver Modul-Auswahl"""
    print("=== Autonomes Kontrollzentrum ===")

    module_names = discover_modules()
    mods = []

    for module_name in module_names:
        try:
            mod = importlib.import_module(module_name)
            mods.append((module_name, mod, get_capabilities(mod)))
        except Exception as e:
            print(f"[WARN] Modul {module_name}: {e}")

    if not mods:
        print("Keine Module gefunden!")
        return

    args = sys.argv[1:]

    # Team-Modus Check
    if args and args[0].lower() == "team":
        run_team_mode()
        return

    # Alle Module mit Aktion
    if args and args[0] == "alle" and len(args) > 1:
        action = args[1]
        ok, fail = [], []
        for name, mod, caps in mods:
            if action in caps:
                print(f"[INFO] {name}.{action}() ...")
                try:
                    getattr(mod, action)()
                    ok.append(name)
                except Exception as e:
                    print(f"[ERROR] {name}.{action}: {e}")
                    fail.append(name)
        print(f"\n[OK] Erfolgreich: {len(ok)}  [FEHLER] Fehler: {len(fail)}")
        return

    # Interaktives CLI
    print("\nGefundene Module:")
    for i, (name, mod, caps) in enumerate(mods):
        print(f"  {i+1}. {name}: {', '.join(caps) if caps else 'keine Capabilities'}")

    print("\nVerwendung:")
    print("  [nummer] [aktion] [parameter...]")
    print("  Beispiel: 2 to_svg output.svg")
    print("  Oder: alle install")

    inp = input("\n> ").strip()

    if inp.startswith("alle "):
        _, action = inp.split(" ", 1)
        for name, mod, caps in mods:
            if action in caps:
                print(f"[INFO] {name}.{action}()")
                getattr(mod, action)()
        return

    parts = inp.split()
    if not parts or not parts[0].isdigit():
        print("[FEHLER] Ungültige Eingabe")
        return

    idx = int(parts[0]) - 1
    if idx < 0 or idx >= len(mods):
        print("[FEHLER] Ungültige Modulnummer")
        return

    action = parts[1] if len(parts) > 1 else "run"
    params = parts[2:] if len(parts) > 2 else []

    name, mod, caps = mods[idx]
    if action not in caps:
        print(f"[FEHLER] {name} unterstützt '{action}' nicht")
        return

    print(f"[INFO] {name}.{action}({', '.join(params)})")
    func = getattr(mod, action)
    func(*params)


def main():
    """Haupt-Entry-Point"""
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "api":
            run_api_mode()
            return
        elif cmd == "health":
            run_health_check()
            return
        elif cmd == "team":
            run_team_mode()
            return
    
    # Streamlit Detection
    try:
        import streamlit.web.cli as stcli
        if len(sys.argv) > 1 and "streamlit" in sys.argv[0].lower():
            run_streamlit_mode()
            return
    except:
        pass

    # Check for Streamlit run
    if "streamlit" in " ".join(sys.argv):
        run_streamlit_mode()
    else:
        run_cli_mode()


if __name__ == "__main__":
    main()
