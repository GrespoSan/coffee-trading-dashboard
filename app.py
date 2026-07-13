import streamlit as st
import yfinance as yf

# --- Configurazione Pagina ---
st.set_page_config(page_title="Dashboard COMM_COT_T1", layout="wide")
st.title("🛡️ Dashboard di Validazione")

# --- BLOCCO 1: Inserimento Dati (Rapporto COT) ---
st.header("1. Inserimento Dati")
st.caption("Trascrivi i dati dal blocco base del terminale")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Open Interest")
    oi_tot = st.number_input("Open Interest Totale", value=174440)
    oi_var = st.number_input("Change in Open Interest", value=-9288)

with col2:
    st.subheader("Managed Money (MM)")
    mm_long = st.number_input("MM Change Long", value=1261)
    mm_short = st.number_input("MM Change Short", value=-3831)

with col3:
    st.subheader("Commercials")
    comm_long = st.number_input("Comm Change Long", value=-5748)
    comm_short = st.number_input("Comm Change Short", value=1044)

with col4:
    st.subheader("Term Structure")
    term_struct = st.radio("Stato attuale (inserimento manuale vedi indicatore in Tradingview):", ["Backwardation", "Contango"])

# --- BLOCCO 2: Elaborazione Matematica ---
# Formule esatte del tuo protocollo
pct_delta_oi = (oi_var / (oi_tot - oi_var)) * 100 if (oi_tot - oi_var) != 0 else 0
flusso_netto_mm = mm_long - mm_short
flusso_netto_comm = comm_long - comm_short

st.header("2. Elaborazione Matematica (Algoritmo)")
calc1, calc2, calc3 = st.columns(3)
calc1.metric("Variazione % Open Interest", f"{pct_delta_oi:.2f}%")
calc2.metric("Flusso Netto Speculativo (MM)", f"{flusso_netto_mm:+.0f}")
calc3.metric("Flusso Netto Commerciale", f"{flusso_netto_comm:+.0f}")

st.divider()

# --- BLOCCO 3 e 4: Matrice di Diagnosi e Azione Strategica ---
st.header("3. Matrice di Diagnosi Microstrutturale: Il Verdetto")

# Logica di assegnazione degli stati basata sul tuo documento
if pct_delta_oi <= -0.5 and flusso_netto_mm > 0 and term_struct == "Backwardation":
    stato_colore = "green"
    stato_testo = "HOLD AGGRESSIVO / PIRAMIDARE SULLA FORZA"
    verdetto = "Short Covering Squeeze di continuazione strutturale [STADIO 3-B]"
    diag_oi = f"L'Open Interest subisce una contrazione massiccia ({pct_delta_oi:.2f}%), indicando una forte fuga di contratti complessivi dal mercato."
    diag_mm = f"I grandi fondi speculativi hanno immesso un flusso netto nettamente rialzista ({flusso_netto_mm:+.0f}). La diminuzione drastica degli Short unita a nuovi Long conferma che la pressione ribassista è venuta meno."
    diag_comm = f"L'industria fisica ha ridotto in modo drastico le coperture Long e ha aumentato gli Short (Flusso: {flusso_netto_comm:+.0f})."
    azione = "Mantieni l'acquisto effettuato sul pavimento.\nImposta lo stop-loss rigido sotto i minimi intraday registrati sul pavimento volumetrico."

elif pct_delta_oi > 0.5 and flusso_netto_mm < 0:
    stato_colore = "red"
    stato_testo = "DISTRIBUZIONE / PERICOLO"
    verdetto = "Fase di Distribuzione Istituzionale e Accumulo Short"
    diag_oi = f"L'Open Interest è in espansione ({pct_delta_oi:.2f}%), indicando ingresso di nuovo capitale direzionale."
    diag_mm = f"I fondi speculativi stanno immettendo flussi ribassisti ({flusso_netto_mm:+.0f}), aprendo posizioni Short."
    diag_comm = f"I Commercials stanno riassorbendo la liquidità (Flusso: {flusso_netto_comm:+.0f})."
    azione = "Valuta la chiusura delle posizioni Long.\nNon cercare ingressi in contro-trend. Stringi gli stop-loss al breakeven."

else:
    stato_colore = "orange"
    stato_testo = "FASE DI TRANSIZIONE / INCERTEZZA"
    verdetto = "Nessuna confluenza macro-quantitativa rilevata"
    diag_oi = f"La variazione dell'OI ({pct_delta_oi:.2f}%) non è sufficientemente anomala da indicare uno svuotamento o un accumulo chiaro."
    diag_mm = f"Flusso Managed Money ({flusso_netto_mm:+.0f}) senza direzionalità estrema."
    diag_comm = f"Flusso Commercials ({flusso_netto_comm:+.0f}) all'interno dei parametri di copertura standard."
    azione = "Resta in attesa. Non forzare il mercato e mantieni il piano di trading attuale senza piramidare."

# Renderizzazione del Verdetto
st.markdown(f"#### **Il Verdetto:** {verdetto}")
st.info(f"""
- **Diagnosi OI:** {diag_oi}
- **Diagnosi MM:** {diag_mm}
- **Diagnosi Commercials:** {diag_comm}
""")

st.markdown(f"### Stato Operativo Ricalibrato: <span style='color:{stato_colore}'>{stato_testo}</span>", unsafe_allow_html=True)

st.success(f"""
**Azione Strategica:**
- {azione}
""")
