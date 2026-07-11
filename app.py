import streamlit as st
import pandas as pd
import requests
import yfinance as yf

# Configurazione Pagina
st.set_page_config(page_title="Dashboard Protocollo COMM_COT_T1", layout="wide")

# --- FUNZIONI DI ESTRAZIONE DATI ---

def get_cot_data(ticker, api_key):
    """Estrae i dati COT e OI tramite EOD Historical Data API"""
    # Nota: L'endpoint è esemplificativo, usa quello specifico della documentazione EOD
    url = f"https://eodhistoricaldata.com/api/cot/{ticker}?api_token={api_key}&fmt=json"
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data).iloc[:2] # Ultime 2 settimane per il confronto [2], [5]
        return df
    except Exception as e:
        st.error(f"Errore nel recupero dati per {ticker}: {e}")
        return None

def get_realtime_price(ticker_yf):
    """Recupera il prezzo in tempo reale da Yahoo Finance [6], [4]"""
    try:
        asset = yf.Ticker(ticker_yf)
        price = asset.history(period="1d")['Close'].iloc[-1]
        return round(price, 2)
    except:
        return 0.0

# --- LOGICA DEL PROTOCOLLO ---

def calcola_semaforo(df):
    """Applica le formule matematiche del protocollo [2], [5]"""
    # 1. Net Position Managed Money (Mani Forti)
    long_mm = df['managed_money_long'].iloc
    short_mm = df['managed_money_short'].iloc
    net_attuale = long_mm - short_mm
    
    long_mm_prev = df['managed_money_long'].iloc[1]
    short_mm_prev = df['managed_money_short'].iloc[1]
    net_precedente = long_mm_prev - short_mm_prev

    # 2. Variazione Open Interest (% Delta OI) [2]
    oi_attuale = df['open_interest'].iloc
    oi_prec = df['open_interest'].iloc[1]
    delta_oi = ((oi_attuale - oi_prec) / oi_prec) * 100

    # 3. Flusso Netto Commerciale [2]
    net_comm = df['commercial_long'].iloc - df['commercial_short'].iloc

    # Determinazione Output Operativo [7], [5]
    if net_attuale > net_precedente and net_attuale > 0:
        status = "🟢 BULLISH (Accumulo)"
        color = "green"
    elif net_attuale < net_precedente and net_attuale < 0:
        status = "🔴 BEARISH (Distribuzione)"
        color = "red"
    else:
        status = "🟡 NEUTRALE / HOLD"
        color = "gray"

    return {
        "Status": status,
        "Color": color,
        "Net MM": net_attuale,
        "Change MM": net_attuale - net_precedente,
        "Delta OI %": round(delta_oi, 2),
        "Net Commercials": net_comm
    }

# --- INTERFACCIA DASHBOARD ---

st.title("🛡️ Protocollo COMM_COT_T1: Dashboard Automatica")
st.sidebar.header("Impostazioni API")
api_key = st.sidebar.text_input("Inserisci EOD API Key", type="password")

# Selezione Multi-Asset [3]
st.sidebar.header("Selezione Future")
ticker_list = st.sidebar.multiselect(
    "Scegli i Future da analizzare",
    ["KC.COMM", "SB.COMM", "CL.COMM", "GC.COMM", "NG.COMM"],
    default=["KC.COMM"]
)

if api_key:
    for ticker in ticker_list:
        with st.expander(f"Analisi Asset: {ticker}", expanded=True):
            df_cot = get_cot_data(ticker, api_key)
            
            if df_cot is not None:
                risultati = calcola_semaforo(df_cot)
                prezzo = get_realtime_price(ticker.replace(".COMM", "=F")) # Proxy per Yahoo Finance

                # Visualizzazione Layout [4]
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Prezzo Real-Time", f"{prezzo}")
                with col2:
                    st.metric("Net Position MM", f"{risultati['Net MM']}", f"{risultati['Change MM']}")
                with col3:
                    st.metric("Delta Open Interest", f"{risultati['Delta OI %']}%")
                with col4:
                    st.markdown(f"### Semaforo\n**{risultati['Status']}**")

                # Diagnosi specifica del Protocollo [2], [8]
                if risultati['Delta OI %'] < -0.5 and risultati['Color'] == "green":
                    st.success("✅ **DIAGNOSI: HEALTHY RELOAD.** Il calo dell'OI conferma una pulizia tecnica dei contratti [2], [8].")
                elif risultati['Delta OI %'] > 0.5 and risultati['Color'] == "red":
                    st.error("⚠️ **DIAGNOSI: DISTRIBUZIONE AGGRESSIVA.** Nuovi short istituzionali in ingresso [8].")

else:
    st.warning("Inserisci la tua API Key nella sidebar per iniziare l'estrazione automatica.")

st.divider()
st.caption("Dati estratti via EOD Historical Data. Logica basata sul modello di validazione integrato COMM_COT_T1 [7].")
