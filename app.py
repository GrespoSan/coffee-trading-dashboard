import streamlit as st
import yfinance as yf
import pandas as pd

# Configurazione Pagina
st.set_page_config(page_title="Dashboard COMM_COT_T1", layout="wide")

st.title("🛡️ Dashboard di Validazione: COMM_COT_T1")

# --- Funzione per recuperare i dati ---
@st.cache_data(ttl=3600) # Aggiorna i dati ogni ora
def get_coffee_price():
    try:
        ticker = yf.Ticker("KC=F") # Future Caffè su Yahoo Finance
        data = ticker.history(period="1d")
        return data['Close'].iloc[-1]
    except:
        return None

# --- Sidebar: Input Dati ---
st.sidebar.header("Input Parametri Manuali")
cot_bias = st.sidebar.selectbox("Bias COT (Managed Money)", ["Bullish (Verde)", "Bearish (Rosso)", "Neutro"])
term_struct = st.sidebar.selectbox("Term Structure", ["Backwardation (Verde)", "Contango (Rosso)"])
oi_trend = st.sidebar.selectbox("Trend Open Interest", ["In Aumento", "In Calo", "Stabile"])
market_phase = st.sidebar.selectbox("Fase di Mercato", ["Trend Riposizionato", "Ritracciamento/Reload", "Distribuzione"])

# --- Recupero dati automatici ---
prezzo_caffe = get_coffee_price()

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

# --- Layout Dashboard ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Stato Operativo")
    st.markdown(f"### <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
    
    st.info(f"""
    **Analisi Sintetica:**
    - **Bias COT:** {cot_bias}
    - **Fase:** {market_phase}
    - **Term Structure:** {term_struct}
    - **Trend OI:** {oi_trend}
    """)

with col2:
    st.subheader("Mercato in Tempo Reale")
    if prezzo_caffe:
        st.metric(label="Prezzo Caffè (KC=F)", value=f"{prezzo_caffe:.2f} USD")
    else:
        st.warning("Dati di prezzo non disponibili al momento.")

# --- Spiegazione Logica ---
st.divider()
st.caption("Il sistema incrocia i dati macro. La configurazione attuale indica una condizione di mercato orientata alla " + status.split(' ')[0])
