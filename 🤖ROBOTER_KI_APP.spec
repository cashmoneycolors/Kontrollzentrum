# -*- mode: python ; coding: utf-8 -*-
# MEGA ULTRA ROBOTER KI APP - QUANTUM PRODUCTION EDITION
# Vollständig integriert: OpenAI + Stripe + PayPal + AWS + NFT + Complete System

a = Analysis(
    ['mega_roboter_ki.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('modules', 'modules'),
        ('core', 'core'),
        ('.env.example', '.'),
    ],
    hiddenimports=[
        'streamlit',
        'fastapi',
        'uvicorn',
        'openai',
        'stripe',
        'paypalcheckoutsdk',
        'boto3',
        'web3',
        'anthropic',
        'google.generativeai',
        'pandas',
        'numpy',
        'requests',
        'dotenv',
        'jwt',
        'psutil',
        'cryptography',
        'pillow',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='🤖ROBOTER_KI_APP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
