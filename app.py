import streamlit as st
import yfinance as yf

# Configurazione Pagina
st.set_page_config(page_title="Dashboard COMM_COT_T1", layout="wide")

st.title("🛡️ Dashboard di Validazione: COMM_COT_T1")

# --- Funzione Prezzo Automatico ---
@st.cache_data(ttl=3600)
def get_coffee_price():
    try:
        ticker = yf.Ticker("KC=F")
        data = ticker.history(period="1d")
        return data['Close'].iloc[-1]
    except:
        return None

# --- Layout Principale ---
col_head1, col_head2 = st.columns([2, 1])
with col_head2:
    prezzo = get_coffee_price()
    st.metric(label="Prezzo Caffè (KC=F)", value=f"{prezzo:.2f} USD" if prezzo else "N/A")

st.divider()

# --- Blocco Motore di Diagnosi Automatica ---
st.subheader("⚙️ Motore di Diagnosi: Inserimento Dati Quantitativi")
st.caption("Inserisci i dati estratti dal tuo terminale (Rapporto COT)")

c1, c2, c3, c4 = st.columns(4)
with c1:
    oi_tot = st.number_input("Open Interest Totale", value=174440)
with c2:
    oi_var = st.number_input("Variazione OI (es. -9288)", value=-9288)
with c3:
    long_mm = st.number_input("Change Long (MM)", value=1261)
with c4:
    short_mm = st.number_input("Change Short (MM)", value=-3831)

# Calcoli
pct_delta_oi = (oi_var / (oi_tot - oi_var)) * 100
flusso_netto_mm = long_mm - abs(short_mm)

# --- Risultati e Diagnosi ---
st.divider()
res1, res2 = st.columns(2)

with res1:
    st.metric("Variazione % OI", f"{pct_delta_oi:.2f}%")
    st.metric("Flusso Netto Managed Money", f"{flusso_netto_mm}")

with res2:
    st.subheader("Verdetto di Mercato")
    if pct_delta_oi < -0.5 and flusso_netto_mm > 0:
        st.success("DIAGNOSI: Short Covering Squeeze di continuazione strutturale. HOLD AGGRESSIVO / PIRAMIDARE.")
    elif pct_delta_oi > 0.5 and flusso_netto_mm < 0:
        st.error("DIAGNOSI: Distribuzione in corso. Valutare uscita.")
    else:
        st.warning("DIAGNOSI: Fase di transizione / Incerta.")

st.info("""
**Logica del protocollo:**
- Se OI cala > 0,5% e il Flusso Netto MM è positivo, il mercato sta scaricando i deboli per ripartire.
- Il sistema incrocia la matematica del COT con la volatilità dell'OI.
""")
