import streamlit as st
import pandas as pd
import re
import src

st.set_page_config(page_title="Configuratore Contromonta", layout="wide")

st.title("🏗️ Bridge Builder: Calcolo Personalizzato")

uploaded_file = st.sidebar.file_uploader("1. Carica Excel", type="xlsx")

if uploaded_file:
    try:
        temp_disp = pd.read_excel(uploaded_file, sheet_name='disp')
        carichi_disponibili = temp_disp['Load'].unique().tolist()
        nodi_disponibili = temp_disp['Node'].unique()
        
        st.sidebar.header("2. Filtro Nodi")
        n_min_val = int(min(nodi_disponibili))
        n_max_val = int(max(nodi_disponibili))
        node_range = st.sidebar.slider("Seleziona Range", n_min_val, n_max_val, (n_min_val, n_max_val))
        
        st.sidebar.header("3. Nodi di Pila / Appoggi")
        st.sidebar.markdown("Forza a zero i risultati per le pile.")
        nodi_pila_input = st.sidebar.text_input("Es: 535, 742, 886", "")
        nodi_pila_list = [int(x) for x in re.findall(r'\d+', nodi_pila_input)]
        
        st.sidebar.header("4. Combinazione Carichi")
        selected_loads = st.sidebar.multiselect("Scegli i carichi", carichi_disponibili, default=carichi_disponibili[:2])
        
        user_coeffs = {}
        for load in selected_loads:
            user_coeffs[load] = st.sidebar.number_input(f"Coeff. per {load}", value=1.0, step=0.05)
        
        if st.sidebar.button("Calcola Monta"):
            df_res, pile_valide = src.elabora_report_configurabile(
                uploaded_file, node_range[0], node_range[1], user_coeffs, nodi_pila_list
            )
            
            pile_ignorate = set(nodi_pila_list) - set(pile_valide)
            if pile_ignorate:
                st.warning(f"⚠️ I nodi {list(pile_ignorate)} non sono nel range o non esistono e sono stati ignorati.")

            st.subheader(f"📊 Sintesi Nodi da {node_range[0]} a {node_range[1]}")
            
            # Formattazione per la tabella: 2 decimali per i calcoli, 0 decimali per Nodi, Concio e Monta
            formattazione = {col: "{:.2f}" for col in df_res.columns if col not in ['Node', 'Concio', 'MONTA [mm]', 'Note']}
            formattazione['Node'] = "{:.0f}"
            formattazione['Concio'] = "{:.0f}"
            formattazione['MONTA [mm]'] = "{:.0f}"

            def stile_tabella(row):
                if row['Note'] == 'PILA':
                    return ['color: #d9534f; font-weight: bold; background-color: #fdf2f2'] * len(row)
                return [''] * len(row)

            # Applichiamo la formattazione specifica
            st.dataframe(
                df_res.style.format(formattazione)
                .apply(stile_tabella, axis=1)
                .background_gradient(subset=['MONTA [mm]'], cmap='Greens'), 
                use_container_width=True
            )
            
            st.subheader("📈 Profilo Contromonta Risultante")
            st.plotly_chart(src.crea_grafico(df_res), use_container_width=True)
            
            # Durante l'esportazione CSV sarà già arrotondato correttamente
            csv = df_res.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Scarica Tabella in CSV", csv, "report_monta_officina.csv", "text/csv")
        else:
            st.info("Configura i parametri a sinistra e premi 'Calcola Monta'.")

    except Exception as e:
        st.error(f"Errore durante la lettura: {e}")
else:
    st.info("Carica il file Excel per attivare i comandi.")