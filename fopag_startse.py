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
    # Colunas fechamento: Jan(3), Fev(4), Mar(5), 1T(6)
    # Colunas orçamento:  Jan(8), Fev(9), Mar(10), 1T(11)
    rows = [
        # Time                         Fech_Jan    Fech_Fev    Fech_Mar    Fech_1T      OrcJan     OrcFev     OrcMar     Orc_1T       AB         Área
        ("Marketing B2C",           270557.22,  292022.64,  358501.78,   921081.64,  308232.15, 321870.94, 321870.94,  951974.03,  -0.0325,  "Marketing"),
        ("Marketing B2B",            57361.58,   56677.26,   90147.48,   204186.32,   67426.65,  67426.65,  90276.56,  225129.86,  -0.0930,  "Marketing"),
        ("Vendas B2C",              310408.30,  317192.50,  353725.60,   981326.40,  344958.00, 344958.00, 375790.00, 1065707.00,  -0.0792,  "Vendas"),
        ("Vendas B2B",              350806.20,  332892.60,  392038.50,  1075737.30,  427684.00, 427684.00, 471952.00, 1327319.00,  -0.1895,  "Vendas"),
        ("Produtos Corporate",      197234.80,  244442.70,  179786.50,   621464.00,  212292.00, 240827.00, 240827.00,  693946.00,  -0.1044,  "Produtos"),
        ("Tech Academy",            122660.70,  121893.00,  166899.70,   411453.40,  120609.00, 120609.00, 120609.00,  361828.00,   0.1372,  "Produtos"),
        ("Produtos Offline/Eventos", 78055.31,   77566.76,  109303.50,   264925.57,   99526.00,  99526.00,  99526.00,  298577.00,  -0.1127,  "Produtos"),
        ("Produtos Inter",          330046.59,  228653.14,  241196.10,   799895.83,  260846.00, 260846.00, 262349.00,  784042.00,   0.0202,  "Produtos"),
        ("Contabilidade",            77844.00,   77356.00,  105919.00,   261119.00,   62104.00,  62104.00,  62104.00,  186312.00,   0.4015,  "Backoffice"),
        ("Financeiro",               91831.31,   35988.59,   50973.30,   178793.20,   82980.00,  82980.00,  82980.00,  248941.00,  -0.2818,  "Backoffice"),
        ("People",                   63560.00,   63162.00,   86484.00,   213206.00,   53298.00,  66312.00,  66312.00,  185921.00,   0.1468,  "Backoffice"),
        ("Atendimento",              67813.22,   67388.77,   88022.63,   223224.62,   58515.00,  58515.00,  59770.00,  176799.00,   0.2626,  "Backoffice"),
        ("Revops",                   99757.00,   98482.00,  132671.00,   330911.00,   91235.00,  91235.00,  91235.00,  273706.00,   0.2090,  "Backoffice"),
        ("Facilites",                38521.20,   38280.09,   52414.30,   129215.59,   36031.00,  36031.00,  36031.00,  108092.00,   0.1954,  "Backoffice"),
        ("Ops",                     115169.00,  113798.00,  129631.00,   358598.00,  156317.00, 164320.00, 175396.00,  496032.00,  -0.2771,  "Backoffice"),
        ("Tech",                    321517.50,  260130.90,  316521.00,   898169.40,  324443.00, 324443.00, 331575.00,  980461.00,  -0.0839,  "Backoffice"),
        ("Diretoria",               831669.00,  831669.00,  831669.00,  2495006.00,  593667.00, 593667.00, 593667.00, 1781000.00,   0.4009,  "Diretoria"),
    ]

    meses = ["Jan","Fev","Mar"]
    orc_meses_fut = ["Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

    # Orçamento futuro por time
    orc_futuro = {
        "Marketing B2C":           [321870.94, 380370.33, 388981.86, 335840.19, 387403.64, 371769.07, 385554.82, 389765.69, 310991.77],
        "Marketing B2B":           [90276.56, 136812.17, 140150.97, 119547.29, 142860.88, 136654.86, 142127.00, 143798.47, 112529.79],
        "Vendas B2C":              [381103.54, 468212.53, 483999.89, 446159.65, 517218.09, 494749.61, 514561.14, 520612.58, 407406.46],
        "Vendas B2B":              [503533.60, 590526.02, 603331.25, 515880.53, 636122.83, 610226.65, 633060.54, 640035.17, 509558.77],
        "Produtos Corporate":      [240826.95, 276079.84, 281109.06, 250073.79, 292262.77, 282607.45, 291121.01, 293721.48, 245073.71],
        "Tech Academy":            [120609.24, 143894.88, 147406.53, 125736.20, 145511.37, 139190.21, 144763.87, 146466.36, 114617.55],
        "Produtos Offline/Eventos":[99525.51, 118842.01, 121742.26, 103844.86, 123246.30, 117892.36, 122613.19, 124055.17, 97079.63],
        "Produtos Inter":          [49436.07, 59118.41, 60561.15, 51658.02, 59782.53, 57185.52, 59475.43, 60174.88, 47089.98],
        "Contabilidade":           [62104.12, 76025.06, 77880.40, 67463.72, 78074.07, 74682.46, 77673.01, 78586.47, 61498.01],
        "Financeiro":              [84652.35, 102000.97, 104490.22, 92012.80, 106484.11, 101858.34, 108990.58, 110272.36, 86293.86],
        "People":                  [67938.55, 81703.74, 83697.66, 71393.22, 82621.59, 79032.42, 82197.16, 83163.83, 65080.03],
        "Atendimento":             [59770.32, 71477.79, 73222.15, 62457.72, 72280.76, 69140.81, 71909.45, 72755.13, 56934.68],
        "Revops":                  [91235.36, 108765.93, 111420.28, 95040.31, 116915.41, 111836.49, 116314.82, 117682.73, 92092.86],
        "Facilites":               [36030.55, 43218.68, 44273.40, 38648.78, 44727.27, 42784.27, 44497.51, 45020.81, 35231.13],
        "Ops":                     [183398.48, 225672.47, 240612.85, 213286.46, 256142.84, 253922.96, 273354.83, 285942.44, 231099.59],
        "Tech":                    [338979.28, 410566.93, 420586.50, 372995.57, 431658.46, 412906.78, 429441.03, 434491.43, 340012.17],
        "Diretoria":               [593666.67, 593666.67, 593666.67, 593666.67, 593666.67, 593666.67, 593666.67, 593666.67, 593666.67],
    }

    records = []
    for r in rows:
        time_name, j, f, m, t1, orc_jan, orc_fev, orc_mar, orc_1t, ab, area = r
        rec = {
            "Time": time_name, "Área": area,
            "Fech_Jan": j, "Fech_Fev": f, "Fech_Mar": m,
            "Fech_1T2026": t1,
            "Orc_Jan": orc_jan, "Orc_Fev": orc_fev, "Orc_Mar": orc_mar,
            "Orc_1T2026": orc_1t,
            "AB_ratio": ab,
        }
        fut = orc_futuro.get(time_name, [0]*9)
        for mn, vl in zip(orc_meses_fut, fut):
            rec[f"Orc_{mn}"] = vl
        records.append(rec)

    df = pd.DataFrame(records)

    # ── Totais reais da folha (linha 9 da planilha) ──
    # Estes são os totais CORRETOS para KPIs e evolução mensal.
    # A soma dos times individuais é menor pois não inclui encargos/benefícios globais.
    totais_people = {
        "Fech_Jan": 3600312.70, "Fech_Fev": 3418096.24, "Fech_Mar": 3875704.07,
        "Fech_1T":  10894113.01,
        "Orc_Jan":  3478663.24, "Orc_Fev":  3541853.25, "Orc_Mar":  3675770.30,
        "Orc_1T":   10696286.80,
        "Orc_Abr":  3518458.09, "Orc_Mai":  4095454.41, "Orc_Jun":  4185633.10,
        "Orc_Jul":  3787205.74, "Orc_Ago":  4326479.59, "Orc_Set":  4189606.91,
        "Orc_Out":  4330822.03, "Orc_Nov":  4379711.67, "Orc_Dez":  3645756.67,
    }

    # Total People (da linha 9 da planilha)
    df_people = pd.DataFrame([{
        "Time": "People (Total)", "Área": "People",
        "Fech_Jan": 3600312.70, "Fech_Fev": 3418096.24, "Fech_Mar": 3875704.07,
        "Fech_1T2026": 10894113.01,
        "Orc_Jan": 3478663.24, "Orc_Fev": 3541853.25, "Orc_Mar": 3675770.30,
        "Orc_1T2026": 10696286.80, "AB_ratio": 0.0185,
    }])

    return df, totais_people

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


def chart_waterfall(df, xcol, ycol, total_override=None):
    df_s = df.sort_values(ycol, ascending=False)
    total = total_override if total_override is not None else df_s[ycol].sum()
    # Se há override, adiciona uma barra "Outros" para a diferença
    xs = df_s[xcol].tolist()
    ys = df_s[ycol].tolist()
    measures = ["relative"] * len(df_s)
    if total_override is not None:
        diff = total_override - df_s[ycol].sum()
        if abs(diff) > 1:
            xs.append("Outros/Encargos")
            ys.append(diff)
            measures.append("relative")
    xs.append("TOTAL")
    ys.append(total)
    measures.append("total")

    fig = go.Figure(go.Waterfall(
        orientation="v", measure=measures, x=xs, y=ys,
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


def chart_area_meses(df_filtered, totais_people):
    """
    totais_people: dict com os totais reais da linha 9 (People/folha total).
    Usado quando todos os times estão selecionados.
    df_filtered é usado quando há filtro de times (subtotal dos filtrados).
    """
    todos_selecionados = len(df_filtered) == 17  # total de times

    meses_fech = ["Jan", "Fev", "Mar"]
    if todos_selecionados:
        totais_fech = [totais_people[f"Fech_{m}"] for m in meses_fech]
    else:
        totais_fech = [df_filtered[f"Fech_{m}"].sum() for m in meses_fech]

    meses_orc_1t  = ["Jan", "Fev", "Mar"]
    meses_orc_fut = ["Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    if todos_selecionados:
        totais_orc_1t  = [totais_people[f"Orc_{m}"] for m in meses_orc_1t]
        totais_orc_fut = [totais_people[f"Orc_{m}"] for m in meses_orc_fut]
    else:
        totais_orc_1t  = [df_filtered[f"Orc_{m}"].sum() for m in meses_orc_1t]
        totais_orc_fut = [df_filtered[f"Orc_{m}"].sum() if f"Orc_{m}" in df_filtered.columns else 0
                          for m in meses_orc_fut]

    todos_meses_orc = meses_orc_1t + meses_orc_fut
    todos_vals_orc  = totais_orc_1t + totais_orc_fut

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=meses_fech, y=totais_fech, name="Fechamento Real",
        mode="lines+markers",
        line=dict(color="#0057FF", width=3),
        marker=dict(size=9, color="#4a8aff", line=dict(color="#060d1f", width=2)),
        fill="tozeroy", fillcolor="rgba(0,87,255,0.07)",
        hovertemplate="<b>%{x}</b><br>Real: R$ %{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=todos_meses_orc, y=todos_vals_orc, name="Orçamento",
        mode="lines+markers",
        line=dict(color="#00c897", width=2, dash="dot"),
        marker=dict(size=7, color="#00c897"),
        hovertemplate="<b>%{x}</b><br>Orç: R$ %{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(**LAYOUT, height=320,
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
    df, totais_people = get_data()

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

    todos_selecionados = len(df_f) == len(df)
    val_col = "Fech_1T2026" if "Fechamento" in visao else "Orc_1T2026"

    # Usa totais da linha 9 (People) quando todos os times estão selecionados
    total_real = totais_people["Fech_1T"] if todos_selecionados else df_f["Fech_1T2026"].sum()
    total_orc  = totais_people["Orc_1T"]  if todos_selecionados else df_f["Orc_1T2026"].sum()
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
    # TAB 1 — VISÃO POR TIME
    # ══════════════════════════════════════════
    with tab1:
        visao_label = "Fechamento 1T2026" if "Fechamento" in visao else "Orçamento 1T2026"
        col_a, col_b = st.columns([3,2], gap="large")
        with col_a:
            st.markdown(f'<div class="sec"><span class="sec-dot">▌</span> Despesas por Time — {visao_label}</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_hbar(df_f, val_col, "Time"), use_container_width=True)
        with col_b:
            st.markdown(f'<div class="sec"><span class="sec-dot">▌</span> Distribuição % · {visao_label}</div>', unsafe_allow_html=True)
            top9 = df_f.nlargest(9, val_col)
            outros = df_f[val_col].sum() - top9[val_col].sum()
            lbls = top9["Time"].tolist()
            vals = top9[val_col].tolist()
            if outros > 0: lbls.append("Outros"); vals.append(outros)
            st.plotly_chart(chart_donut(lbls, vals), use_container_width=True)

        st.markdown(f'<div class="sec"><span class="sec-dot">▌</span> Treemap Hierárquico · Área › Time · {visao_label}</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_treemap(df_f, "Time", "Área", val_col), use_container_width=True)

        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Composição por Área</div>', unsafe_allow_html=True)
        df_grp = df_f.groupby("Área")[val_col].sum().reset_index().sort_values(val_col, ascending=False)
        st.plotly_chart(chart_donut(df_grp["Área"].tolist(), df_grp[val_col].tolist()), use_container_width=True)

        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Insights Automáticos</div>', unsafe_allow_html=True)
        top3 = df_f.nlargest(3, val_col)
        total_vis = df_f[val_col].sum()
        pct3 = top3[val_col].sum() / total_vis * 100 if total_vis else 0
        maior_grp = df_grp.iloc[0]
        for txt in [
            f"Top 3 Times (<strong>{', '.join(top3['Time'].tolist())}</strong>) concentram <strong>{pct3:.1f}%</strong> do total ({visao_label}).",
            f"A área <strong>{maior_grp['Área']}</strong> tem a maior alocação: <strong>{brl(maior_grp[val_col])}</strong> ({maior_grp[val_col]/total_vis*100:.1f}% do total).",
            f"Total realizado 1T2026: <strong>{brl(total_real)}</strong> vs orçado <strong>{brl(total_orc)}</strong> — variação de <strong>{total_ab*100:+.1f}%</strong>.",
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
        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Evolução Mensal: Realizado Jan–Mar + Orçamento Jan–Dez 2026</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_area_meses(df_f, totais_people), use_container_width=True)

        col_e, col_f = st.columns(2, gap="large")
        with col_e:
            st.markdown('<div class="sec"><span class="sec-dot">▌</span> Fechamento Mensal por Time — Jan, Fev, Mar</div>', unsafe_allow_html=True)
            fig_m = go.Figure()
            meses = ["Jan","Fev","Mar"]
            for i, time_name in enumerate(df_f["Time"].tolist()):
                row = df_f[df_f["Time"]==time_name].iloc[0]
                vals_f = [row[f"Fech_{m}"] for m in meses]
                vals_o = [row[f"Orc_{m}"] for m in meses]
                color = COLORS[i % len(COLORS)]
                fig_m.add_trace(go.Scatter(
                    x=meses, y=vals_f, name=f"{time_name} (Real)",
                    mode="lines+markers",
                    line=dict(color=color, width=2),
                    marker=dict(size=7),
                    hovertemplate=f"<b>{time_name} Real</b><br>%{{x}}: R$ %{{y:,.0f}}<extra></extra>"
                ))
            fig_m.update_layout(**LAYOUT, height=400,
                xaxis=dict(showgrid=False, tickfont=dict(color="#b0bcd4")),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,87,255,0.07)", tickformat=",.0f"))
            fig_m.update_layout(legend=dict(font=dict(size=9)))
            st.plotly_chart(fig_m, use_container_width=True)

        with col_f:
            st.markdown(f'<div class="sec"><span class="sec-dot">▌</span> Waterfall Acumulado 1T2026 · {visao_label}</div>', unsafe_allow_html=True)
            wf_total = totais_people["Fech_1T"] if (todos_selecionados and "Fechamento" in visao) else (totais_people["Orc_1T"] if todos_selecionados else None)
            st.plotly_chart(chart_waterfall(df_f, "Time", val_col, total_override=wf_total), use_container_width=True)

        st.markdown('<div class="sec"><span class="sec-dot">▌</span> Variação Jan→Fev e Fev→Mar por Time (Fechamento Real)</div>', unsafe_allow_html=True)
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
