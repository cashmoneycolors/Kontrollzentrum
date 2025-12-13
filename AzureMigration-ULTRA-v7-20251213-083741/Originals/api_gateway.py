"""
FastAPI Gateway - Zentrale API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Kontrollzentrum API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    """Health Check"""
    return {"status": "ok", "service": "kontrollzentrum"}

@app.get("/modules")
def list_modules():
    """Listet verfügbare Module"""
    from pathlib import Path
    modules = [f[:-3] for f in os.listdir("modules") 
               if f.endswith(".py") and not f.startswith("__")]
    return {"modules": sorted(modules)}

@app.post("/run/{module_name}")
def run_module(module_name: str):
    """Führt Modul aus"""
    try:
        import importlib
        mod = importlib.import_module(f"modules.{module_name}")
        if hasattr(mod, "run"):
            result = mod.run()
            return {"status": "ok", "result": result}
        else:
            raise HTTPException(status_code=400, detail="Modul hat keine run()-Funktion")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/config")
def get_config():
    """Zeigt Konfiguration (ohne Secrets)"""
    return {
        "api_host": os.getenv("API_HOST", "0.0.0.0"),
        "api_port": os.getenv("API_PORT", "8000"),
        "debug": os.getenv("API_DEBUG", "false").lower() == "true",
    }
