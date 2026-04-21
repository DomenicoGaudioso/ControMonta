import pandas as pd
import plotly.graph_objects as go

def elabora_report_configurabile(file_excel, node_min, node_max, coeff_dict, nodi_pila=[]):
    df_nodi = pd.read_excel(file_excel, sheet_name='Nodi')
    df_disp = pd.read_excel(file_excel, sheet_name='disp')
    
    for df in [df_nodi, df_disp]:
        df.columns = df.columns.str.strip()

    df_nodi_f = df_nodi[(df_nodi['Node'] >= node_min) & (df_nodi['Node'] <= node_max)]
    
    nodi_in_disp = df_disp[(df_disp['Node'] >= node_min) & (df_disp['Node'] <= node_max)]['Node'].unique().tolist()
    nodi_pila_validi = [n for n in nodi_pila if n in df_nodi_f['Node'].values]
    target_nodes = list(set(nodi_in_disp + nodi_pila_validi))
    
    carichi_scelti = list(coeff_dict.keys())
    df_disp_f = df_disp[df_disp['Node'].isin(target_nodes) & df_disp['Load'].isin(carichi_scelti)]
    
    if not df_disp_f.empty:
        df_pivot = df_disp_f.pivot(index='Node', columns='Load', values='DZ (mm)').reset_index()
    else:
        df_pivot = pd.DataFrame({'Node': target_nodes})
        
    for c in carichi_scelti:
        if c not in df_pivot.columns:
            df_pivot[c] = 0.0
    df_pivot.fillna(0, inplace=True)
    
    for carico, coeff in coeff_dict.items():
        if carico in df_pivot.columns:
            df_pivot[carico] = df_pivot[carico] * coeff

    # Calcolo Z mantenendo i decimali per precisione
    df_pivot['Z [mm]'] = df_pivot[carichi_scelti].sum(axis=1)
    
    # --- ARROTONDAMENTO MONTA PER L'OFFICINA ---
    # Invertiamo il segno, arrotondiamo all'intero più vicino e convertiamo in formato Integer
    df_pivot['MONTA [mm]'] = (-df_pivot['Z [mm]']).round(0).astype(int)
    
    mask_pila = df_pivot['Node'].isin(nodi_pila_validi)
    if mask_pila.any():
        df_pivot.loc[mask_pila, 'Z [mm]'] = 0.0
        df_pivot.loc[mask_pila, 'MONTA [mm]'] = 0 # Valore intero
        for c in carichi_scelti:
            df_pivot.loc[mask_pila, c] = 0.0
    
    df_report = pd.merge(df_pivot, df_nodi_f[['Node', 'X']], on='Node').sort_values('X')
    df_report['Concio'] = range(1, len(df_report) + 1)
    
    df_report['Note'] = ""
    df_report.loc[df_report['Node'].isin(nodi_pila_validi), 'Note'] = "PILA"
    
    col_order = ['Node', 'X'] + carichi_scelti + ['Z [mm]', 'MONTA [mm]', 'Concio', 'Note']
    return df_report[col_order], nodi_pila_validi

def crea_grafico(df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df['X'], y=df['MONTA [mm]'], mode='lines',
                             name='Profilo Monta', line=dict(color='blue', width=2)))
    
    df_norm = df[df['Note'] == ""]
    fig.add_trace(go.Scatter(x=df_norm['X'], y=df_norm['MONTA [mm]'], mode='markers+text',
                             text=df_norm['Node'], textposition="top center", name='Nodi Conci',
                             marker=dict(size=8, color='blue')))
    
    df_pila = df[df['Note'] == "PILA"]
    if not df_pila.empty:
        fig.add_trace(go.Scatter(x=df_pila['X'], y=df_pila['MONTA [mm]'], mode='markers+text',
                                 text=df_pila['Node'], textposition="bottom center", name='Appoggi (Pile)',
                                 marker=dict(size=12, color='red', symbol='square')))
                                 
    fig.update_layout(title="Profilo della Contromonta (Valori Arrotondati)", xaxis_title="X [m]", yaxis_title="Monta [mm]", template="plotly_white")
    return fig