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
    term_struct = st.radio("Stato attuale (inserimento manuale vedi indicatore in Tradingview):", ["Backwardation (verde)", "Contango (rosso)"])

# --- BLOCCO 2: Elaborazione Matematica ---
# Formule esatte del tuo protocollo
pct_delta_oi = (oi_var / (oi_tot - oi_var)) * 100 if (oi_tot - oi_var) != 0 else 0
flusso_netto_mm = mm_long - mm_short
flusso_netto_comm = comm_long - comm_short

st.header("2. Elaborazione Matematica")
calc1, calc2, calc3 = st.columns(3)
calc1.metric("Variazione % Open Interest", f"{pct_delta_oi:.2f}%")
calc2.metric("Flusso Netto Speculativo Managed Money (MM)", f"{flusso_netto_mm:+.0f}")
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

st.divider()

# --- BLOCCO EXTRA: Spiegazione Dinamica in Parole Semplici ---
st.header("4. Interpretazione Macro e Sequenza Temporale")

# Rilevamento automatico della divergenza/convergenza dei flussi
if flusso_netto_mm < 0 and flusso_netto_comm > 0:
    st.warning("⚠️ **Rilevata DIVERGENZA ISTITUZIONALE: SHORT ➔ LONG**")
    st.write(f"""
    **Cosa sta succedendo in parole semplici:**
    1. **OGGI / BREVE TERMINE:** I grandi fondi speculativi (Managed Money) stanno vendendo pesantemente o chiudendo i Long (Flusso Speculativo: `{flusso_netto_mm:+.0f}`). Questo significa che l'azione immediata del prezzo subisce una forte pressione ribassista. **Il coltello sta cadendo, quindi non forzare acquisti immediati.**
    2. **PROSSIME SETTIMANE / MEDIO TERMINE:** Sotto il cofano del mercato, i Commerciali (Smart Money) stanno comprando a mani basse (Flusso Commerciale: `{flusso_netto_comm:+.0f}`) assorbendo le vendite. Loro stanno preparando un pavimento di prezzo.
    
    **💡 Conclusione:** Il trend di brevissimo è Short, ma ci stiamo girando al rialzo. Tieni gli occhi aperti sul grafico di TradingView: non appena il Bias principale si girerà d'accordo con i commerciali, avrai un'eccellente opportunità di acquisto sul pavimento.
    """)

elif flusso_netto_mm > 0 and flusso_netto_comm < 0:
    st.warning("⚠️ **Rilevata DIVERGENZA ISTITUZIONALE: LONG ➔ SHORT**")
    st.write(f"""
    **Cosa sta succedendo in parole semplici:**
    1. **OGGI / BREVE TERMINE:** I grandi fondi speculativi stanno spingendo il mercato verso l'alto o ricoprendo le vendite (Flusso Speculativo: `{flusso_netto_mm:+.0f}`). Il prezzo attuale mostra ancora forza inerziale rialzista.
    2. **PROSSIME SETTIMANE / MEDIO TERMINE:** I Commerciali (i produttori reali) ritengono che questi prezzi siano ottimi per fare coperture e stanno vendendo massicciamente (Flusso Commerciale: `{flusso_netto_comm:+.0f}`). Stanno costruendo un tetto al mercato.
    
    **💡 Conclusione:** Il trend di brevissimo è ancora Long, ma la Smart Money si sta posizionando Short per un'inversione ribassista nelle prossime settimane. Proteggi i profitti dei tuoi Long e non inseguire i massimi.
    """)

elif flusso_netto_mm > 0 and flusso_netto_comm > 0:
    st.success("🟢 **CONVERGENZA RIALZISTA STRUTTURALE**")
    st.write(f"""
    **Cosa sta succedendo in parole semplici:**
    Sia gli speculatori (Managed Money) che i commerciali stanno immettendo flussi positivi nel mercato. Quando entrambe le categorie remano nella stessa direzione, c'è massima armonia sui volumi ed il trend rialzista gode di ottima salute istituzionale.
    """)

elif flusso_netto_mm < 0 and flusso_netto_comm < 0:
    st.error("🔴 **CONVERGENZA RIBASSISTA STRUTTURALE**")
    st.write(f"""
    **Cosa sta succedendo in parole semplici:**
    Sia i grandi fondi che i commerciali stanno togliendo liquidità o aumentando i contratti short. Il mercato è strutturalmente debole a tutti i livelli temporali, la pressione ribassista è totale.
    """)
else:
    st.info("⚪ **FLUSSI IN EQUILIBRIO NEUTRO**")
    st.write("I flussi non mostrano sbilanciamenti direzionali o divergenze macroscopiche. Il mercato si trova in una fase di attesa o lateralità tecnica.")
