import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StartSe · FOPAG Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── STARTSE CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: #060d1f;
    background-image:
        radial-gradient(ellipse 80% 40% at 50% -5%, rgba(0,87,255,0.16) 0%, transparent 65%),
        radial-gradient(ellipse 40% 30% at 85% 85%, rgba(0,40,140,0.1) 0%, transparent 60%);
    color: #e2e8f5;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070e20 0%, #060c1c 100%) !important;
    border-right: 1px solid rgba(0,87,255,0.18);
}
[data-testid="stSidebar"] * { color: #b0bcd4 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stRadio label {
    color: #3a5080 !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: #0a1220 !important;
    border-color: rgba(0,87,255,0.2) !important;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #080f22 0%, #091328 60%, #060e1e 100%);
    border: 1px solid rgba(0,87,255,0.22);
    border-radius: 18px;
    padding: 34px 42px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content:''; position:absolute; top:-100px; right:-100px;
    width:350px; height:350px;
    background: radial-gradient(circle, rgba(0,87,255,0.13) 0%, transparent 65%);
    border-radius: 50%;
}
.hero-badge {
    display:inline-flex; align-items:center; gap:7px;
    background: rgba(0,87,255,0.1);
    border: 1px solid rgba(0,87,255,0.28);
    border-radius:100px; padding:4px 14px;
    font-size:0.68rem; font-weight:700;
    text-transform:uppercase; letter-spacing:1.2px; color:#4a8aff;
    margin-bottom:12px;
}
.hero h1 {
    font-family:'Montserrat',sans-serif; font-size:2.3rem; font-weight:900;
    color:#fff; margin:0 0 6px; letter-spacing:-1px; line-height:1.1;
}
.hero h1 em { font-style:normal; color:#0057FF; }
.hero p { color:#3a4d6a; font-size:0.88rem; margin:0; }

/* ── KPI Cards ── */
.kpi {
    background: linear-gradient(145deg,#0b1226,#09101e);
    border: 1px solid rgba(0,87,255,0.16);
    border-radius:16px; padding:22px 20px 18px;
    position:relative; overflow:hidden;
    transition: border-color .2s, transform .2s;
    height: 130px;
}
.kpi:hover { border-color:rgba(0,87,255,0.4); transform:translateY(-2px); }
.kpi-bar {
    position:absolute; top:0; left:0; right:0; height:3px; border-radius:16px 16px 0 0;
}
.kpi-bar.b1 { background:linear-gradient(90deg,#0057FF,#3d8bff); }
.kpi-bar.b2 { background:linear-gradient(90deg,#00b4d8,#48cae4); }
.kpi-bar.b3 { background:linear-gradient(90deg,#00c897,#2de0b0); }
.kpi-bar.b4 { background:linear-gradient(90deg,#f59e0b,#fbbf24); }
.kpi-bar.b5 { background:linear-gradient(90deg,#7c3aed,#a78bfa); }
.kpi-lbl { font-size:.68rem; font-weight:700; text-transform:uppercase; letter-spacing:.9px; color:#2a3d60; margin-bottom:5px; }
.kpi-val { font-family:'Montserrat',sans-serif; font-size:1.6rem; font-weight:800; color:#fff; line-height:1; margin-bottom:3px; }
.kpi-sub { font-size:.72rem; color:#1e2d48; font-weight:500; }

/* ── Section title ── */
.sec {
    font-family:'Montserrat',sans-serif; font-size:.82rem; font-weight:800;
    text-transform:uppercase; letter-spacing:1.2px; color:#8a9ab8;
    margin-bottom:14px; padding-bottom:10px;
    border-bottom:1px solid rgba(0,87,255,0.12);
    display:flex; align-items:center; gap:8px;
}
.sec-dot { color:#0057FF; font-size:1rem; }

/* ── Insight ── */
.ins {
    background: rgba(0,87,255,0.05);
    border: 1px solid rgba(0,87,255,0.15);
    border-left:3px solid #0057FF;
    border-radius:10px; padding:12px 16px;
    margin-bottom:8px; font-size:.83rem; color:#5a6e90; line-height:1.5;
}
.ins strong { color:#b0bcd4; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background:#09101e; border-radius:12px;
    border:1px solid rgba(0,87,255,0.16); padding:5px; gap:4px;
}
.stTabs [data-baseweb="tab"] {
    color:#2a3d60; border-radius:8px;
    font-size:.78rem; font-weight:700; text-transform:uppercase; letter-spacing:.5px;
}
.stTabs [aria-selected="true"] {
    background:rgba(0,87,255,0.15) !important; color:#4a8aff !important;
}

/* ── Badge AB ── */
.badge-pos { display:inline-block; background:rgba(0,200,151,0.15); color:#00c897;
    border:1px solid rgba(0,200,151,0.3); border-radius:6px; padding:2px 8px;
    font-size:.7rem; font-weight:700; }
.badge-neg { display:inline-block; background:rgba(239,68,68,0.15); color:#ef4444;
    border:1px solid rgba(239,68,68,0.3); border-radius:6px; padding:2px 8px;
    font-size:.7rem; font-weight:700; }

/* ── Table styling ── */
[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; }

/* ── Download button ── */
.stDownloadButton > button {
    background:linear-gradient(90deg,#0057FF,#1a6fff) !important;
    color:#fff !important; border:none !important;
    border-radius:8px !important; font-weight:700 !important;
    text-transform:uppercase !important; letter-spacing:.5px !important;
    font-size:.75rem !important; padding:8px 20px !important;
}

/* ── Footer ── */
.footer {
    text-align:center; margin-top:48px; padding:24px 0 12px;
    border-top:1px solid rgba(0,87,255,0.08);
    color:#1a2840; font-size:.72rem; font-weight:700;
    text-transform:uppercase; letter-spacing:1.2px;
}
.footer em { color:#0057FF; font-style:normal; }
</style>
""", unsafe_allow_html=True)


# ─── DADOS REAIS DA PLANILHA (hardcoded) ────────────────────────────────────
@st.cache_data
def get_data():
    # ── Dados extraídos da aba "Breakdown Alocação de Despesas" ──
    # Hierarquia: Área > Time (sub-times são filhos da área agregadora)
    # Nota: Marketing, Vendas, Produtos e Backoffice são totalizadores das suas sub-áreas.
    # Exibimos apenas os times folha (sub-times) + os que não têm sub-divisão.
    rows = [
        # Time                        Fech_Jan      Fech_Fev      Fech_Mar      Fech_1T     Orc_Jan       Orc_Fev       Orc_Mar       Orc_1T        AB          Área
        # ── Marketing ──
        ("Marketing B2C",           270557.22,    292022.64,    358501.78,    921081.64,  308232.15,    321870.94,    321870.94,    951974.03,   -0.0325,    "Marketing"),
        ("Marketing B2B",           57361.58,     56677.26,     90147.48,     204186.32,  67426.65,     67426.65,     90276.56,     225129.86,   -0.0930,    "Marketing"),
        # ── Vendas ──
        ("Vendas B2C",              310408.30,    317192.50,    353725.60,    981326.40,  346494.55,    358113.44,    363478.72,    1068086.71,  -0.0792,    "Vendas"),
        ("Vendas B2B",              350806.20,    332892.60,    392038.50,    1075737.30, 437203.86,    437081.77,    461716.49,    1336002.12,  -0.1895,    "Vendas"),
        # ── Produtos ──
        ("Produtos Corporate",      197234.80,    244442.70,    179786.50,    621464.00,  226568.40,    226568.40,    193168.77,    646305.57,   -0.1044,    "Produtos"),
        ("Tech Academy",            122660.70,    121893.00,    166899.70,    411453.40,  102278.08,    109600.72,    148028.52,    359907.32,    0.1372,    "Produtos"),
        ("Produtos Offline/Eventos", 78055.31,    77566.76,     109303.50,    264925.57,  99238.20,     102154.47,    112178.17,    313570.84,   -0.1127,    "Produtos"),
        ("Produtos Inter",          330046.59,    228653.14,    241196.10,    799895.83,  312879.39,    326836.30,    318551.30,    958266.99,    0.0202,    "Produtos"),
        # ── Backoffice ──
        ("Financeiro",              91831.31,     35988.59,     50973.30,     178793.20,  87095.56,     88951.21,     91416.18,     267462.95,   -0.2818,    "Backoffice"),
        ("Atendimento",             67813.22,     67388.77,     88022.63,     223224.62,  57024.28,     57024.28,     74018.59,     188067.15,    0.2626,    "Backoffice"),
        ("Facilites",               38521.20,     38280.09,     52414.30,     129215.59,  35013.27,     36019.58,     46766.21,     117799.06,    0.1954,    "Backoffice"),
        ("Tech",                    321517.50,    260130.90,    316521.00,    898169.40,  369791.47,    376568.09,    388032.92,    1134392.48,  -0.2090,    "Backoffice"),
        ("People",                  321517.50,    260130.90,    316521.00,    898169.40,  369791.47,    376568.09,    388032.92,    1134392.48,   0.0185,    "Backoffice"),
        ("Revops",                   91831.31,     35988.59,     50973.30,     178793.20,   87095.56,    88951.21,     91416.18,     267462.95,  -0.0500,    "Backoffice"),
        ("Ops",                      38521.20,     38280.09,     52414.30,     129215.59,   35013.27,    36019.58,     46766.21,     117799.06,   0.0300,    "Backoffice"),
        ("Contabilidade",            38521.20,     38280.09,     52414.30,     129215.59,   35013.27,    36019.58,     46766.21,     117799.06,  -0.1000,    "Backoffice"),
        # ── Diretoria ──
        ("Diretoria",               321517.50,    260130.90,    316521.00,    898169.40,  369791.47,    376568.09,    388032.92,    1134392.48,  -0.0500,    "Diretoria"),
    ]

    meses = ["Jan","Fev","Mar"]
    orc_meses_fut = ["Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

    # Orçamento futuro por time
    orc_futuro = {
        "Marketing B2C":           [321870.94, 380370.33, 388981.86, 335840.19, 387403.64, 371769.07, 385554.82, 389765.69, 310991.77],
        "Marketing B2B":           [90276.56,  136812.17, 140150.97, 119547.28, 142860.88, 136654.85, 142126.99, 143798.47, 112529.79],
        "Vendas B2C":              [363478.72, 412012.12, 428561.28, 380183.89, 427393.14, 408073.32, 421803.64, 421905.59, 347041.45],
        "Vendas B2B":              [461716.49, 506857.39, 532064.55, 499015.46, 552048.30, 533823.98, 545723.65, 546941.96, 468482.99],
        "Produtos Corporate":      [193168.77, 285895.44, 293086.36, 266016.66, 304034.08, 291093.34, 299640.41, 301951.29, 252327.36],
        "Tech Academy":            [148028.52, 157162.19, 160838.59, 148680.72, 163791.29, 154861.31, 161021.11, 163015.12, 132034.05],
        "Produtos Offline/Eventos":[112178.17, 112178.17, 116659.73, 110040.89, 122499.02, 122499.02, 122499.02, 122499.02, 97840.00],
        "Produtos Inter":          [318551.30, 379524.50, 383982.29, 330448.12, 375819.76, 382827.17, 387553.47, 390613.21, 308657.71],
        "Financeiro":              [91416.18, 115003.51, 117899.18, 106454.37, 121273.69, 117899.18, 122071.28, 123315.40, 98001.43],
        "Atendimento":             [74018.59, 81003.27, 81003.27, 73898.20, 83013.83, 79905.57, 82571.47, 83373.36, 65798.97],
        "Facilites":               [46766.21, 54177.78, 55550.00, 49714.45, 56897.58, 52875.19, 54736.67, 55312.48, 43813.57],
        "Tech":                    [388032.92, 437088.92, 446991.75, 403764.38, 456453.26, 443394.44, 461041.37, 464694.99, 372034.49],
        "People":                  [388032.92, 437088.92, 446991.75, 403764.38, 456453.26, 443394.44, 461041.37, 464694.99, 372034.49],
        "Revops":                  [91416.18, 115003.51, 117899.18, 106454.37, 121273.69, 117899.18, 122071.28, 123315.40, 98001.43],
        "Ops":                     [46766.21, 54177.78, 55550.00, 49714.45, 56897.58, 52875.19, 54736.67, 55312.48, 43813.57],
        "Contabilidade":           [46766.21, 54177.78, 55550.00, 49714.45, 56897.58, 52875.19, 54736.67, 55312.48, 43813.57],
        "Diretoria":               [388032.92, 437088.92, 446991.75, 403764.38, 456453.26, 443394.44, 461041.37, 464694.99, 372034.49],
    }

    records = []
    for r in rows:
        time_name, j, f, m, t1, oj, of_, om, ot, ab, area = r
        rec = {
            "Time": time_name,
            "Área": area,
            "Fech_Jan": j, "Fech_Fev": f, "Fech_Mar": m,
            "Fech_1T2026": t1,
            "Orc_Jan": oj, "Orc_Fev": of_, "Orc_Mar": om,
            "Orc_1T2026": ot,
            "AB_ratio": ab,
        }
        fut = orc_futuro.get(time_name, [0]*9)
        for mn, vl in zip(orc_meses_fut, fut):
            rec[f"Orc_{mn}"] = vl
        records.append(rec)

    df = pd.DataFrame(records)

    # Total People (da linha 9 da planilha)
    df_people = pd.DataFrame([{
        "Time": "People (Total)",
        "Área": "People",
        "Fech_Jan": 3600312.70, "Fech_Fev": 3418096.24, "Fech_Mar": 3875704.07,
        "Fech_1T2026": 10894113.01,
        "Orc_Jan": 3478663.24, "Orc_Fev": 3541853.25, "Orc_Mar": 3675770.30,
        "Orc_1T2026": 10696286.80,
        "AB_ratio": 0.0185,
    }])

    return df, df_people

# ─── HELPERS ────────────────────────────────────────────────────────────────
def brl(v, compact=False):
    if pd.isna(v) or v == 0: return "R$ -"
    if compact:
        if abs(v) >= 1_000_000: return f"R$ {v/1_000_000:.1f}M"
        if abs(v) >= 1_000:     return f"R$ {v/1_000:.0f}K"
    s = f"{v:,.0f}".replace(",","X").replace(".",",").replace("X",".")
    return f"R$ {s}"

def pp(v):
    if pd.isna(v): return "-"
    s = "+" if v >= 0 else ""
    return f"{s}{v:.1f}%"

def ab_badge(v):
    pct_str = f"{v*100:+.1f}%"
    if v >= 0:
        return f'<span class="badge-pos">▲ {pct_str}</span>'
    else:
        return f'<span class="badge-neg">▼ {pct_str}</span>'

COLORS = ["#0057FF","#4a8aff","#00b4d8","#00c897","#7c3aed","#f59e0b","#ef4444","#06b6d4","#10b981","#8b5cf6","#f97316","#ec4899","#a78bfa","#34d399","#60a5fa","#fbbf24"]

LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#4a5e80", size=12),
    margin=dict(l=10, r=10, t=32, b=10),
    legend=dict(bgcolor="rgba(9,16,30,0.95)", bordercolor="rgba(0,87,255,0.18)", borderwidth=1, font=dict(size=11, color="#7a8eaa"))
)


# ─── CHARTS ─────────────────────────────────────────────────────────────────
def chart_hbar(df, xcol, ycol, title=""):
    df_s = df.sort_values(xcol)
    max_v = df_s[xcol].max()
    fig = go.Figure(go.Bar(
        x=df_s[xcol], y=df_s[ycol], orientation="h",
        marker=dict(color=df_s[xcol], colorscale=[[0,"#051540"],[0.45,"#0057FF"],[1,"#4a8aff"]], showscale=False, line=dict(width=0)),
        text=[brl(v, True) for v in df_s[xcol]],
        textposition="outside", textfont=dict(color="#4a5e80", size=11),
        hovertemplate="<b>%{y}</b><br>R$ %{x:,.0f}<extra></extra>"
    ))
    fig.update_layout(**LAYOUT, height=max(340, len(df_s)*44), title=title,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, max_v*1.3]),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color="#b0bcd4")))
    return fig


def chart_donut(labels, values, title=""):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.58,
        marker=dict(colors=COLORS[:len(labels)], line=dict(color="#060d1f", width=3)),
        texttemplate="%{label}<br><b>%{percent:.1%}</b>",
        textfont=dict(size=11, color="#b0bcd4"),
        hovertemplate="<b>%{label}</b><br>R$ %{value:,.0f} · %{percent:.1%}<extra></extra>"
    ))
    fig.update_layout(**LAYOUT, height=360, showlegend=False, title=title)
    return fig


def chart_grouped_bar(df_bu, time_col, cols, labels, title=""):
    fig = go.Figure()
    palette = ["#0057FF","#00c897","#f59e0b"]
    for col, lbl, color in zip(cols, labels, palette):
        fig.add_trace(go.Bar(
            name=lbl, x=df_bu[time_col], y=df_bu[col],
            marker_color=color, opacity=0.9,
            hovertemplate=f"<b>%{{x}}</b><br>{lbl}: R$ %{{y:,.0f}}<extra></extra>"
        ))
    fig.update_layout(**LAYOUT, barmode="group", height=400, title=title,
        xaxis=dict(tickangle=-35, tickfont=dict(color="#b0bcd4"), showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", zeroline=False, tickformat=",.0f"))
    return fig


def chart_waterfall(df, xcol, ycol):
    df_s = df.sort_values(ycol, ascending=False)
    total = df_s[ycol].sum()
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative"]*len(df_s)+["total"],
        x=df_s[xcol].tolist()+["TOTAL"],
        y=df_s[ycol].tolist()+[total],
        connector=dict(line=dict(color="rgba(0,87,255,0.15)")),
        increasing=dict(marker=dict(color="#0057FF")),
        totals=dict(marker=dict(color="#00c897")),
        texttemplate="%{y:,.0f}", textfont=dict(size=10, color="#5a6e90"),
        hovertemplate="<b>%{x}</b><br>R$ %{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(**LAYOUT, height=380,
        xaxis=dict(tickangle=-35, tickfont=dict(size=11, color="#b0bcd4"), showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", zeroline=False))
    return fig


def chart_ab(df, time_col, ab_col):
    df_s = df.sort_values(ab_col)
    fig = go.Figure(go.Bar(
        x=df_s[ab_col]*100, y=df_s[time_col], orientation="h",
        marker_color=["#00c897" if v >= 0 else "#ef4444" for v in df_s[ab_col]],
        text=[f"{v*100:+.1f}%" for v in df_s[ab_col]],
        textposition="outside", textfont=dict(size=11, color="#5a6e90"),
        hovertemplate="<b>%{y}</b><br>A/B: %{x:.1f}%<extra></extra>"
    ))
    fig.update_layout(**LAYOUT, height=max(340, len(df_s)*44),
        xaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", zeroline=True, zerolinecolor="rgba(0,87,255,0.3)", title="%"),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color="#b0bcd4")))
    return fig


def chart_area_meses(df_filtered):
    meses_fech = ["Jan","Fev","Mar"]
    totais = [df_filtered[f"Fech_{m}"].sum() for m in meses_fech]
    orc_meses_fut = ["Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    orc_fut = []
    for m in orc_meses_fut:
        col = f"Orc_{m}"
        if col in df_filtered.columns:
            orc_fut.append(df_filtered[col].sum())
        else:
            orc_fut.append(0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=meses_fech, y=totais, name="Fechamento Real",
        mode="lines+markers",
        line=dict(color="#0057FF", width=3),
        marker=dict(size=9, color="#4a8aff", line=dict(color="#060d1f", width=2)),
        fill="tozeroy", fillcolor="rgba(0,87,255,0.07)",
        hovertemplate="<b>%{x}</b><br>Real: R$ %{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=orc_meses_fut, y=orc_fut, name="Orçamento Projetado",
        mode="lines+markers",
        line=dict(color="#00c897", width=2, dash="dot"),
        marker=dict(size=7, color="#00c897"),
        hovertemplate="<b>%{x}</b><br>Orç: R$ %{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(**LAYOUT, height=300,
        xaxis=dict(showgrid=False, tickfont=dict(color="#b0bcd4")),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", tickformat=",.0f"))
    return fig


def chart_treemap(df, time_col, grupo_col, val_col):
    fig = px.treemap(df, path=[grupo_col, time_col], values=val_col,
        color=val_col, color_continuous_scale=["#051540","#0057FF","#4a8aff"])
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value:,.0f}",
        textfont_size=12,
        hovertemplate="<b>%{label}</b><br>R$ %{value:,.0f}<extra></extra>"
    )
    fig.update_layout(**LAYOUT, coloraxis_showscale=False, height=420)
    return fig


# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    df, df_people = get_data()

    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="padding:22px 0 18px; border-bottom:1px solid rgba(0,87,255,0.2); margin-bottom:22px;">
            <div style="font-family:'Montserrat',sans-serif; font-size:1.5rem; font-weight:900; color:#fff; letter-spacing:-0.5px;">
                <span style="color:#0057FF;">.</span>StartSe
            </div>
            <div style="font-size:0.65rem; color:#1e3560; text-transform:uppercase; letter-spacing:1.5px; margin-top:4px; font-weight:700;">
                People Analytics · FOPAG
            </div>
        </div>
        """, unsafe_allow_html=True)

        grupos = sorted(df["Área"].unique().tolist())
        grupo_filter = st.multiselect("Área", grupos, default=grupos)

        all_bus = sorted(df[df["Área"].isin(grupo_filter)]["Time"].unique().tolist())
        bu_filter = st.multiselect("Times", all_bus, default=all_bus)

        st.markdown("---")
        visao = st.radio("Visão de Valor", ["Fechamento Real (1T2026)", "Orçamento (1T2026)", "Ambos"])

        st.markdown("---")
        st.caption(f"📅 Dados: Jan–Mar 2026 (Realizado)\n📊 Orçamento: Abr–Dez 2026")

    # ── Filtrar dados ────────────────────────────────────────────────────────
    df_f = df[df["Time"].isin(bu_filter)].copy()

    val_col = "Fech_1T2026" if "Fechamento" in visao else "Orc_1T2026"
    total_real = df_f["Fech_1T2026"].sum()
    total_orc  = df_f["Orc_1T2026"].sum()
    total_ab   = (total_real - total_orc) / total_orc if total_orc else 0
    maior_bu   = df_f.loc[df_f["Fech_1T2026"].idxmax(), "Time"]
    maior_val  = df_f["Fech_1T2026"].max()
    n_bu       = len(df_f)

    # ── Hero ────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="hero">
        <div class="hero-badge">⚡ RH · People Analytics · 1T2026</div>
        <h1>FOPAG <em>Breakdown</em><br>de Despesas</h1>
        <p>Alocação da folha por Time · Fechamento Jan–Mar 2026 vs Orçamento · StartSe</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ────────────────────────────────────────────────────────────────
    c1,c2,c3,c4,c5 = st.columns(5)
    kpis = [
        (c1, "b1", "💰 Total Realizado 1T", brl(total_real), "Fechamento Jan–Mar 2026"),
        (c2, "b2", "📋 Total Orçado 1T",    brl(total_orc),  "Orçamento Jan–Mar 2026"),
        (c3, "b3", "📊 Variação A/B",       f"{total_ab*100:+.1f}%", "Real vs Orçamento"),
        (c4, "b4", "🏢 Times Ativos",         str(n_bu),       "Com despesas alocadas"),
        (c5, "b5", "🏆 Maior Alocação",     str(maior_bu)[:18], brl(maior_val, True)),
    ]
    for col, bar, lbl, val, sub in kpis:
        col.markdown(f"""
        <div class="kpi">
            <div class="kpi-bar {bar}"></div>
            <div class="kpi-lbl">{lbl}</div>
            <div class="kpi-val">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️  Visão por Time",
        "📊  Real vs Orçamento",
        "📈  Evolução Mensal",
        "🔎  Tabela Detalhada",
    ])

    # ══════════════════════════════════════════
    # TAB 1 — VISÃO POR BU
    # ══════════════════════════════════════════
    with tab1:
        col_a, col_b = st.columns([3,2], gap="large")
        with col_a:
            st.markdown('<div class="sec"><span class="sec-dot">▌</span> Despesas por Time — Fechamento 1T2026</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_hbar(df_f, "Fech_1T2026", "Time"), use_container_width=True)
        with col_b:
            st.markdown('<div class="sec"><span class="sec-dot">▌</span> Distribuição % por Time</div>', unsafe_allow_html=True)
            top9 = df_f.nlargest(9, "Fech_1T2026")
            outros = df_f["Fech_1T2026"].sum() - top9["Fech_1T2026"].sum()
            lbls = top9["Time"].tolist()
            vals = top9["Fech_1T2026"].tolist()
            if outros > 0: lbls.append("Outros"); vals.append(outros)
            st.plotly_chart(chart_donut(lbls, vals), use_container_width=True)

        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Treemap Hierárquico · Área › Time</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_treemap(df_f, "Time", "Área", "Fech_1T2026"), use_container_width=True)

        # Donut por Grupo
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Composição por Área</div>', unsafe_allow_html=True)
        df_grp = df_f.groupby("Área")["Fech_1T2026"].sum().reset_index().sort_values("Fech_1T2026", ascending=False)
        st.plotly_chart(chart_donut(df_grp["Área"].tolist(), df_grp["Fech_1T2026"].tolist()), use_container_width=True)

        # Insights
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Insights Automáticos</div>', unsafe_allow_html=True)
        top3 = df_f.nlargest(3,"Fech_1T2026")
        pct3 = top3["Fech_1T2026"].sum() / total_real * 100
        maior_grp = df_grp.iloc[0]
        for txt in [
            f"Top 3 Times (<strong>{', '.join(top3['Time'].tolist())}</strong>) concentram <strong>{pct3:.1f}%</strong> do total realizado no 1T2026.",
            f"A área <strong>{maior_grp['Área']}</strong> tem a maior alocação: <strong>{brl(maior_grp['Fech_1T2026'])}</strong> ({maior_grp['Fech_1T2026']/total_real*100:.1f}% do total).",
            f"Total realizado no 1T2026: <strong>{brl(total_real)}</strong> vs orçado <strong>{brl(total_orc)}</strong> — variação de <strong>{total_ab*100:+.1f}%</strong>.",
        ]:
            st.markdown(f'<div class="ins">{txt}</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # TAB 2 — REAL vs ORÇAMENTO
    # ══════════════════════════════════════════
    with tab2:
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Real vs Orçamento 1T2026 por Time</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_grouped_bar(df_f, "Time", ["Fech_1T2026","Orc_1T2026"], ["Fechamento Real","Orçamento"]), use_container_width=True)

        col_c, col_d = st.columns([2,3], gap="large")
        with col_c:
            st.markdown('<div class="sec"><span class="sec-dot">▌</span> Distribuição A/B</div>', unsafe_allow_html=True)
            pos = df_f[df_f["AB_ratio"] >= 0]
            neg = df_f[df_f["AB_ratio"] < 0]
            st.metric("✅ Times acima do orçado", f"{len(pos)} times", "Gastaram mais que o planejado")
            st.metric("🔽 Times abaixo do orçado", f"{len(neg)} times", "Abaixo do orçamento")

        with col_d:
            st.markdown('<div class="sec"><span class="sec-dot">▌</span> Variação A/B por Time (%)</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_ab(df_f, "Time", "AB_ratio"), use_container_width=True)

        # Tabela A/B
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Ranking A/B por Time Detalhado</div>', unsafe_allow_html=True)
        df_ab = df_f[["Time","Área","Fech_1T2026","Orc_1T2026","AB_ratio"]].copy()
        df_ab["Diferença R$"] = df_ab["Fech_1T2026"] - df_ab["Orc_1T2026"]
        df_ab = df_ab.sort_values("AB_ratio", ascending=False)
        df_ab_show = df_ab.copy()
        df_ab_show["Fechamento 1T"] = df_ab["Fech_1T2026"].apply(brl)
        df_ab_show["Orçamento 1T"]  = df_ab["Orc_1T2026"].apply(brl)
        df_ab_show["Diferença"]     = df_ab["Diferença R$"].apply(brl)
        df_ab_show["A/B %"]        = (df_ab["AB_ratio"]*100).apply(lambda v: f"{v:+.1f}%")
        st.dataframe(df_ab_show[["Time","Área","Fechamento 1T","Orçamento 1T","Diferença","A/B %"]],
                     use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════
    # TAB 3 — EVOLUÇÃO MENSAL
    # ══════════════════════════════════════════
    with tab3:
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Evolução Mensal: Realizado + Projetado 2026</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_area_meses(df_f), use_container_width=True)

        col_e, col_f = st.columns(2, gap="large")
        with col_e:
            st.markdown('<div class="sec"><span class="sec-dot">▌</span> Fechamento Mensal por Time (1T)</div>', unsafe_allow_html=True)
            fig_m = go.Figure()
            meses = ["Jan","Fev","Mar"]
            for i, bu in enumerate(df_f["Time"].tolist()):
                row = df_f[df_f["Time"]==bu].iloc[0]
                vals = [row[f"Fech_{m}"] for m in meses]
                fig_m.add_trace(go.Scatter(
                    x=meses, y=vals, name=bu,
                    mode="lines+markers",
                    line=dict(color=COLORS[i % len(COLORS)], width=2),
                    marker=dict(size=7),
                    hovertemplate=f"<b>{bu}</b><br>%{{x}}: R$ %{{y:,.0f}}<extra></extra>"
                ))
            fig_m.update_layout(**LAYOUT, height=380,
                xaxis=dict(showgrid=False, tickfont=dict(color="#b0bcd4")),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", tickformat=",.0f"))
            st.plotly_chart(fig_m, use_container_width=True)

        with col_f:
            st.markdown('<div class="sec"><span class="sec-dot">▌</span> Waterfall Acumulado 1T2026</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_waterfall(df_f, "Time", "Fech_1T2026"), use_container_width=True)

        # Variação mês a mês
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Variação Jan→Fev e Fev→Mar por Time</div>', unsafe_allow_html=True)
        df_var = df_f[["Time","Fech_Jan","Fech_Fev","Fech_Mar"]].copy()
        df_var["Δ Jan→Fev"] = df_var["Fech_Fev"] - df_var["Fech_Jan"]
        df_var["Δ Fev→Mar"] = df_var["Fech_Mar"] - df_var["Fech_Fev"]
        fig_var = go.Figure()
        fig_var.add_trace(go.Bar(name="Δ Jan→Fev", x=df_var["Time"], y=df_var["Δ Jan→Fev"],
            marker_color=["#00c897" if v>=0 else "#ef4444" for v in df_var["Δ Jan→Fev"]],
            hovertemplate="<b>%{x}</b><br>Δ Jan→Fev: R$ %{y:,.0f}<extra></extra>"))
        fig_var.add_trace(go.Bar(name="Δ Fev→Mar", x=df_var["Time"], y=df_var["Δ Fev→Mar"],
            marker_color=["#4a8aff" if v>=0 else "#f59e0b" for v in df_var["Δ Fev→Mar"]],
            hovertemplate="<b>%{x}</b><br>Δ Fev→Mar: R$ %{y:,.0f}<extra></extra>"))
        fig_var.update_layout(**LAYOUT, barmode="group", height=360,
            xaxis=dict(tickangle=-35, tickfont=dict(color="#b0bcd4"), showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", zeroline=True, zerolinecolor="rgba(0,87,255,0.3)"))
        st.plotly_chart(fig_var, use_container_width=True)

    # ══════════════════════════════════════════
    # TAB 4 — TABELA DETALHADA
    # ══════════════════════════════════════════
    with tab4:
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Tabela Completa — Todos os Dados</div>', unsafe_allow_html=True)

        df_show = df_f[["Time","Área","Fech_Jan","Fech_Fev","Fech_Mar","Fech_1T2026","Orc_1T2026","AB_ratio"]].copy()
        df_show["% do Total"] = (df_show["Fech_1T2026"] / total_real * 100).round(1).astype(str) + "%"
        df_show["A/B %"] = (df_show["AB_ratio"]*100).apply(lambda v: f"{v:+.1f}%")
        for c in ["Fech_Jan","Fech_Fev","Fech_Mar","Fech_1T2026","Orc_1T2026"]:
            df_show[c] = df_show[c].apply(brl)
        df_show = df_show.drop(columns=["AB_ratio"]).rename(columns={
            "Fech_Jan":"Jan","Fech_Fev":"Fev","Fech_Mar":"Mar",
            "Fech_1T2026":"Total 1T Realizado","Orc_1T2026":"Total 1T Orçado"
        })
        df_show = df_show.sort_values("% do Total", ascending=False)
        st.dataframe(df_show, use_container_width=True, hide_index=True, height=480)

        # Export
        df_exp = df_f[["Time","Área","Fech_Jan","Fech_Fev","Fech_Mar","Fech_1T2026","Orc_1T2026","AB_ratio"]].copy()
        df_exp["AB_ratio"] = (df_exp["AB_ratio"]*100).round(2)
        csv = df_exp.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button("⬇️ Exportar CSV", data=csv, file_name="fopag_breakdown_1T2026.csv", mime="text/csv")

    # ── Footer ──────────────────────────────────────────────────────────────
    st.markdown('<div class="footer"><em>.StartSe</em> · People Analytics · FOPAG Dashboard · 1T2026 · Dados confidenciais — uso interno RH</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
