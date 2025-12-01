import ast
import sys

files = [
    'core_amazon_api.py',
    'core_pricing_engine.py',
    'core_order_manager.py',
    'core_supplier_api.py',
    'main.py',
    'dashboard.py',
    'test_app.py'
]

print("=" * 60)
print("🔍 SYNTAX CHECK")
print("=" * 60)

errors = []
for filename in files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        print(f"✅ {filename}")
    except SyntaxError as e:
        print(f"❌ {filename}: {e}")
        errors.append((filename, e))
    except FileNotFoundError:
        print(f"⚠️  {filename}: Datei nicht gefunden")

print("\n" + "=" * 60)
if not errors:
    print("✅ ALLE DATEIEN SYNTAKTISCH KORREKT!")
    sys.exit(0)
else:
    print(f"❌ {len(errors)} Fehler gefunden")
    sys.exit(1)
