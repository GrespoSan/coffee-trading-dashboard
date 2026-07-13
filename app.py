import streamlit as st

st.set_page_config(page_title="Dashboard Protocollo COMM_COT_T1", layout="wide")

st.title("🛡️ Dashboard di Validazione: COMM_COT_T1")

# --- Sidebar per Input Dati ---
st.sidebar.header("Input Parametri")
cot_bias = st.sidebar.selectbox("Bias COT (Managed Money)", ["Bullish (Verde)", "Bearish (Rosso)", "Neutro"])
term_struct = st.sidebar.selectbox("Term Structure", ["Backwardation (Verde)", "Contango (Rosso)"])
oi_trend = st.sidebar.selectbox("Trend Open Interest", ["In Aumento", "In Calo", "Stabile"])
market_phase = st.sidebar.selectbox("Fase di Mercato", ["Trend Riposizionato", "Ritracciamento/Reload", "Distribuzione"])

# --- Logica del Semaforo ---
def get_status(cot, term, oi, phase):
    if cot == "Bullish (Verde)" and term == "Backwardation (Verde)" and oi == "In Calo" and phase == "Ritracciamento/Reload":
        return "🟢 RELOAD VALIDO (Bullish Accumulation)", "green"
    elif cot == "Bullish (Verde)" and term == "Backwardation (Verde)" and oi == "In Aumento" and phase == "Trend Riposizionato":
        return "🟢 TREND CONFERMATO (Accumulazione)", "green"
    elif term == "Contango (Rosso)":
        return "🔴 DISTRIBUZIONE / PERICOLO (No Trade)", "red"
    else:
        return "🟡 MONITORAGGIO / ATTESA", "orange"

status, color = get_status(cot_bias, term_struct, oi_trend, market_phase)

# --- Visualizzazione Risultato ---
st.subheader("Stato Operativo del Protocollo")
st.markdown(f"### <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)

# Spiegazione logica
st.info(f"""
**Analisi Sintetica:**
- **Bias:** {cot_bias}
- **Fase:** {phase}
Il sistema ha incrociato i dati macro. La configurazione attuale indica una condizione di mercato orientata alla {status.split(' ')[0]}.
""")
