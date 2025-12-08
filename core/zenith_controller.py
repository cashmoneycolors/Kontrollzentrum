"""
Streamlit Dashboard - Zenith Controller
"""
import streamlit as st
import os
import importlib
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class ZenithController:
    def __init__(self):
        st.set_page_config(page_title="Zenith Kontrollzentrum", layout="wide")
        self.modules = self._discover_modules()
    
    def _discover_modules(self):
        """Findet alle Module"""
        modules = []
        if Path("modules").exists():
            for fname in os.listdir("modules"):
                if fname.endswith(".py") and not fname.startswith("__"):
                    modules.append(fname[:-3])
        return sorted(modules)
    
    def run(self):
        """Hauptinterface"""
        st.title("🎛️ Zenith Kontrollzentrum")
        
        tab1, tab2, tab3 = st.tabs(["Dashboard", "Module", "System"])
        
        with tab1:
            st.header("📊 Dashboard")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Module", len(self.modules))
            with col2:
                st.metric("Status", "🟢 Online")
            with col3:
                st.metric("API", "✅ Ready")
        
        with tab2:
            st.header("🔧 Module")
            selected = st.selectbox("Wähle Modul:", self.modules)
            if st.button("▶ Ausführen"):
                try:
                    mod = importlib.import_module(f"modules.{selected}")
                    if hasattr(mod, "run"):
                        result = mod.run()
                        st.success(f"✅ {selected} erfolgreich ausgeführt")
                        st.json(result if isinstance(result, dict) else {"result": str(result)})
                    else:
                        st.error(f"❌ {selected} hat keine run()-Funktion")
                except Exception as e:
                    st.error(f"❌ Fehler: {e}")
        
        with tab3:
            st.header("⚙️ System")
            st.write(f"**Python Version:** {os.sys.version}")
            st.write(f"**Arbeitsverzeichnis:** {os.getcwd()}")
            st.write(f"**Module gefunden:** {len(self.modules)}")
            if st.button("🔄 Refresh"):
                st.rerun()
