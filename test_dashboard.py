#!/usr/bin/env python3
"""Test-Script für Streamlit Dashboard"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from core.zenith_controller import ZenithController
from core.key_check import check_all_keys

print("[INFO] Prüfe API-Keys...")
check_all_keys()
print("[OK] Alle API-Keys vorhanden!")

print("[INFO] Initialisiere Zenith Controller...")
controller = ZenithController()
print("[OK] Zenith Controller initialisiert!")

print("[INFO] Teste System-Status...")
status = controller.get_system_status()
print(f"[OK] System-Status: {status}")

print("[INFO] Teste Audit-Funktion...")
controller.audit("Test-Audit")
print("[OK] Audit funktioniert!")

print("\n[SUCCESS] Dashboard-Komponenten funktionieren!")
print("\nUm das Streamlit-Dashboard zu starten:")
print("  streamlit run main.py")
