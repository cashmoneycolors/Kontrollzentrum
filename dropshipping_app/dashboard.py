import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Amazon Dropshipping Dashboard", layout="wide")

API_URL = "http://localhost:8000"

st.title("🛍️ Amazon Dropshipping Dashboard")

tabs = st.tabs(["🔍 Produktsuche", "📊 Statistiken", "📦 Bestellungen", "💰 Profitrechner"])

with tabs[0]:
    st.header("Produktsuche & Analyse")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("Produkt suchen:", placeholder="z.B. Wireless Headphones")
    with col2:
        category = st.selectbox("Kategorie:", ["Alle", "Elektronik", "Mode", "Sport"])
    
    if st.button("🔍 Suchen", use_container_width=True):
        if search_query:
            try:
                response = requests.post(f"{API_URL}/search", json={
                    "query": search_query,
                    "category": None if category == "Alle" else category
                })
                
                if response.status_code == 200:
                    data = response.json()
                    products = data.get("products", [])
                    
                    if products:
                        df = pd.DataFrame([{
                            "Titel": p.get("title", "N/A")[:50],
                            "Amazon Preis": f"${p.get('price', 0):.2f}",
                            "Lieferant": p.get("supplier", "N/A"),
                            "Lieferantenpreis": f"${p.get('supplier_price', 0):.2f}",
                            "Verkaufspreis": f"${p.get('selling_price', 0):.2f}",
                            "Gewinn": f"${p.get('profit', 0):.2f}",
                            "Margin": f"{p.get('margin', 0):.1f}%",
                            "Rating": f"⭐ {p.get('rating', 0)}"
                        } for p in products])
                        
                        st.dataframe(df, use_container_width=True)
                        
                        st.success(f"✅ {len(products)} Produkte gefunden")
                    else:
                        st.warning("Keine Produkte gefunden")
            except Exception as e:
                st.error(f"❌ Fehler: {str(e)}")

with tabs[1]:
    st.header("Dashboard Statistiken")
    
    try:
        response = requests.get(f"{API_URL}/stats")
        if response.status_code == 200:
            stats = response.json()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📋 Gesamt Bestellungen", stats.get("total_orders", 0))
            with col2:
                st.metric("⏳ Ausstehend", stats.get("pending_orders", 0))
            with col3:
                st.metric("🚚 Versendet", stats.get("shipped_orders", 0))
            with col4:
                st.metric("✅ Zugestellt", stats.get("delivered_orders", 0))
            
            st.info("📈 Live-Daten vom API aktualisiert")
    except Exception as e:
        st.error(f"Fehler beim Laden der Statistiken: {e}")

with tabs[2]:
    st.header("Bestellverwaltung")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Neue Bestellung erstellen")
        customer_email = st.text_input("Kundenmail:")
        items_json = st.text_area("Items (JSON):", value='[{"asin": "B001", "qty": 1}]')
        total = st.number_input("Gesamtbetrag:", min_value=0.0, step=0.01)
        
        if st.button("✅ Bestellung erstellen"):
            try:
                import json
                items = json.loads(items_json)
                response = requests.post(f"{API_URL}/orders", json={
                    "customer_email": customer_email,
                    "items": items,
                    "total": total
                })
                if response.status_code == 200:
                    order = response.json()
                    st.success(f"✅ Bestellung erstellt: {order.get('order_id')}")
                    st.json(order)
            except Exception as e:
                st.error(f"Fehler: {e}")
    
    with col2:
        st.subheader("Bestellung nachschlagen")
        order_id = st.text_input("Bestellnummer:")
        
        if st.button("🔍 Nachschlagen"):
            try:
                response = requests.get(f"{API_URL}/orders/{order_id}")
                if response.status_code == 200:
                    order = response.json()
                    st.json(order)
                else:
                    st.warning("Bestellung nicht gefunden")
            except Exception as e:
                st.error(f"Fehler: {e}")

with tabs[3]:
    st.header("💰 Profitrechner")
    
    col1, col2 = st.columns(2)
    
    with col1:
        cost = st.number_input("Lieferantenpreis ($):", min_value=0.0, step=0.01)
        margin = st.slider("Zielgewinnmarge (%):", 10, 60, 35)
    
    with col2:
        shipping = st.number_input("Versandkosten ($):", min_value=0.0, step=0.01, value=2.50)
        platform_fee = st.number_input("Plattformgebühr ($):", min_value=0.0, step=0.01, value=0.15)
    
    if cost > 0:
        total_cost = cost + shipping + platform_fee
        selling_price = total_cost / (1 - margin/100)
        profit = selling_price - total_cost
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Gesamtkosten", f"${total_cost:.2f}")
        with col2:
            st.metric("Verkaufspreis", f"${selling_price:.2f}")
        with col3:
            st.metric("Gewinn", f"${profit:.2f}")
        with col4:
            st.metric("Margin", f"{margin:.1f}%")

st.divider()
st.caption("🚀 Amazon Dropshipping App v1.0 | Starten Sie den API mit: python main.py")
