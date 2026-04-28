import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ── Configuración de la página ─────────────────────────────────────
st.set_page_config(
    page_title="Calidad del Aire en México",
    layout="wide"
)

# Estilos globales
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    h1 { color: #1a1a2e; }
    h2 { color: #16213e; border-bottom: 3px solid #e94560; padding-bottom: 8px; }
    .hallazgo { background: #fff3cd; border-left: 4px solid #ffc107;
                padding: 12px 16px; border-radius: 4px; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)

# ── Cargar datos ───────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    df = pd.read_csv("datos_limpios.csv", parse_dates=["datetime"])
    return df

df = cargar_datos()

# Límites OMS
limites_oms = {"PM2.5": 15, "PM10": 45}

# Colores por ciudad — León ajustado a un morado más claro (#A569BD)
colores_ciudad = {
    "Valle de México": "#e94560",
    "Monterrey":       "#0f3460",
    "Guadalajara":     "#457B9D",
    "Toluca":          "#2A9D8F",
    "León":            "#A569BD",
}

# Línea roja intensa
OMS_COLOR = "#E63946"
OMS_WIDTH = 4

# ── Encabezado ─────────────────────────────────────────────────────
st.title("¿Respiramos peor en lunes?")
st.subheader("Patrones de contaminación del aire en las principales ciudades de México (2010–2021)")
st.markdown("""
México tiene una de las redes de monitoreo atmosférico más extensas de América Latina.
Durante más de una década, cientos de estaciones han registrado los niveles de partículas
y gases que respiramos. Esta historia analiza esos datos para responder una pregunta simple:
**¿importa qué día de la semana es para la calidad del aire que respiramos?**
""")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Estaciones monitoreadas", "78", "todo México")
col2.metric("Años de datos", "2010–2021", "11 años")
col3.metric("Ciudades analizadas", "5", "principales ZM")
pm25_prom = round(df["PM2.5"].mean(), 1)
col4.metric("PM2.5 promedio nacional", f"{pm25_prom} µg/m³", "límite OMS: 15 µg/m³", delta_color="inverse")

st.divider()

# ══════════════════════════════════════════════════════════════════
# VISUALIZACIÓN 1 — ¿Qué ciudad contamina más?
# ══════════════════════════════════════════════════════════════════
st.header("1. El mapa de la contaminación: ¿dónde vivir importa?")
st.markdown("""
No todas las ciudades de México respiran el mismo aire. Antes de hablar de patrones semanales,
necesitamos ver el panorama general: **¿cuáles son las ciudades con peor calidad del aire?**
La línea indica el límite anual recomendado por la Organización Mundial de la Salud.
Si una ciudad supera ese límite, sus habitantes respiran aire considerado dañino para la salud.
""")

contaminante = st.selectbox(
    "Selecciona el contaminante:",
    options=["PM2.5", "PM10"],
    index=0,
    key="viz1"
)

df_ciudad = (
    df.groupby("ciudad")[contaminante]
    .mean()
    .dropna()
    .reset_index()
    .sort_values(contaminante, ascending=True)
)
limite_oms = limites_oms[contaminante]

fig1 = go.Figure()

for _, row in df_ciudad.iterrows():
    color = colores_ciudad.get(row["ciudad"], "#aaaaaa")
    supera = row[contaminante] > limite_oms
    fig1.add_trace(go.Bar(
        x=[row[contaminante]],
        y=[row["ciudad"]],
        orientation="h",
        marker_color=color,
        marker_line_color="white",
        marker_line_width=1.5,
        name=row["ciudad"],
        text=f"  {row[contaminante]:.1f} µg/m³{'  ⚠️' if supera else ''}",
        textposition="outside",
        hovertemplate=f"<b>{row['ciudad']}</b><br>{contaminante}: {row[contaminante]:.1f} µg/m³<extra></extra>"
    ))

fig1.add_vline(
    x=limite_oms,
    line_dash="dash",
    line_color=OMS_COLOR,
    line_width=OMS_WIDTH,
    annotation_text=f"Límite OMS: {limite_oms} µg/m³",
    annotation_position="top right",
    annotation_font_color="black", 
    annotation_font_size=12,
)

fig1.update_layout(
    title=dict(text=f"Concentración promedio de {contaminante} por ciudad (2010–2021)", font_size=16),
    xaxis_title=f"Promedio de {contaminante} (µg/m³)",
    yaxis_title="",
    showlegend=False,
    height=380,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=10, r=120, t=50, b=40),
    xaxis=dict(gridcolor="#eeeeee"),
)
st.plotly_chart(fig1, use_container_width=True)

ciudades_malas = df_ciudad[df_ciudad[contaminante] > limite_oms]["ciudad"].tolist()
if ciudades_malas:
    st.markdown(f'<div class="hallazgo">⚠️ <b>{", ".join(ciudades_malas)}</b> superan el límite anual de la OMS para {contaminante} ({limite_oms} µg/m³). Sus habitantes respiran aire considerado dañino para la salud de forma crónica.</div>', unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════
# VISUALIZACIÓN 2 — ¿Qué día de la semana es el peor?
# ══════════════════════════════════════════════════════════════════
st.header("2. El ritmo semanal: ¿respiramos peor en lunes?")
st.markdown("""
La intuición dice que los **lunes**, con más tráfico y actividad industrial, deberían ser los días
más contaminados de la semana. Pero los datos cuentan otra historia. Los días de descanso no
necesariamente significan aire más limpio — el uso recreativo de autos, las fogatas y otros
factores cambian el patrón. Filtra por ciudad para ver si el comportamiento varía.
""")

col1, col2 = st.columns(2)
with col1:
    ciudad_sel = st.selectbox(
        "Ciudad:",
        options=["Todas"] + sorted(df["ciudad"].unique().tolist()),
        key="viz2_ciudad"
    )
with col2:
    cont_sel = st.selectbox(
        "Contaminante:",
        options=["PM2.5", "PM10"],
        key="viz2_cont"
    )

df_viz2 = df.copy()
if ciudad_sel != "Todas":
    df_viz2 = df_viz2[df_viz2["ciudad"] == ciudad_sel]

orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
nombres_dias = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
}

df_dias = (
    df_viz2.groupby("day_name")[cont_sel]
    .mean()
    .dropna()
    .reindex(orden_dias)
    .reset_index()
)
df_dias["dia_es"] = df_dias["day_name"].map(nombres_dias)
promedio_semana = df_dias[cont_sel].mean()

# Colores para las barras
colores_barras = []
for dia in df_dias["day_name"]:
    if dia == "Saturday": colores_barras.append("#E76F51") 
    elif dia == "Sunday": colores_barras.append("#2A9D8F") 
    else: colores_barras.append("#457B9D") 

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=df_dias["dia_es"],
    y=df_dias[cont_sel],
    marker_color=colores_barras,
    marker_line_color="white",
    marker_line_width=1.5,
    text=[f"{v:.1f}" for v in df_dias[cont_sel]],
    textposition="outside",
    textfont=dict(size=12, color="#333333"),
    hovertemplate="<b>%{x}</b><br>" + cont_sel + ": %{y:.2f} µg/m³<extra></extra>",
    showlegend=False,
))

fig2.add_hline(
    y=promedio_semana,
    line_dash="dot",
    line_color="#888888",
    line_width=1.5,
    annotation_text=f"Promedio semanal: {promedio_semana:.1f}",
    annotation_position="top left",
    annotation_font_color="#888888",
    annotation_font_size=11,
)

limite_cont = limites_oms.get(cont_sel)
if limite_cont:
    fig2.add_hline(
        y=limite_cont,
        line_dash="dash",
        line_color=OMS_COLOR,
        line_width=OMS_WIDTH,
        annotation_text=f"Límite OMS: {limite_cont} µg/m³",
        annotation_position="bottom left",
        annotation_font_color="black", 
        annotation_font_size=11,
    )

fig2.add_trace(go.Scatter(
    x=[None], y=[None], mode="markers",
    marker=dict(size=10, color="#E76F51", symbol="square"),
    name="Pico (Sábado)"
))
fig2.add_trace(go.Scatter(
    x=[None], y=[None], mode="markers",
    marker=dict(size=10, color="#2A9D8F", symbol="square"),
    name="Más limpio (Domingo)"
))

fig2.update_layout(
    title=dict(text=f"Concentración promedio de {cont_sel} por día de la semana — {ciudad_sel}", font_size=16),
    yaxis_title=f"Promedio {cont_sel} (µg/m³)",
    xaxis_title="",
    height=440,
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(gridcolor="#eeeeee"),
    yaxis=dict(gridcolor="#eeeeee"),
    bargap=0.3,
)
st.plotly_chart(fig2, use_container_width=True)

if df_dias[cont_sel].notna().sum() > 0:
    dia_max = df_dias.loc[df_dias[cont_sel].idxmax(), "dia_es"]
    dia_min = df_dias.loc[df_dias[cont_sel].idxmin(), "dia_es"]
    val_max = df_dias[cont_sel].max()
    val_min = df_dias[cont_sel].min()
    diff_pct = ((val_max - val_min) / val_min) * 100
    st.markdown(
        f'<div class="hallazgo">📊 <b>Hallazgo:</b> En {ciudad_sel}, el día más contaminado es el <b>{dia_max}</b> '
        f'({val_max:.1f} µg/m³) y el más limpio es el <b>{dia_min}</b> ({val_min:.1f} µg/m³) — '
        f'una diferencia del <b>{diff_pct:.1f}%</b>.</div>',
        unsafe_allow_html=True
    )

st.divider()

# ══════════════════════════════════════════════════════════════════
# VISUALIZACIÓN 3 — Tendencia histórica
# ══════════════════════════════════════════════════════════════════
st.header("3. ¿Estamos mejorando? La tendencia de una década")
st.markdown("""
Más allá de los patrones semanales, la pregunta de fondo es si la calidad del aire en México
**ha mejorado con el tiempo**. Las políticas de verificación vehicular, la transición energética
y los cambios industriales deberían verse reflejados en los datos. La línea punteada marca
el límite saludable de la OMS — todo lo que esté por encima es territorio de riesgo.
""")

ciudades_disp = sorted(df["ciudad"].unique().tolist())
ciudades_multi = st.multiselect(
    "Selecciona ciudades para comparar:",
    options=ciudades_disp,
    default=ciudades_disp[:3],
    key="viz3"
)
cont_tend = st.selectbox(
    "Contaminante:",
    options=["PM2.5", "PM10"],
    key="viz3_cont"
)

if ciudades_multi:
    df_tend = df[df["ciudad"].isin(ciudades_multi)].copy()
    p99 = df_tend[cont_tend].quantile(0.99)
    df_tend = df_tend[df_tend[cont_tend] <= p99]
    df_tend = (
        df_tend
        .groupby(["year", "ciudad"])[cont_tend]
        .mean()
        .dropna()
        .reset_index()
    )

    fig3 = go.Figure()

    for ciudad in ciudades_multi:
        df_c = df_tend[df_tend["ciudad"] == ciudad]
        if df_c.empty:
            continue
        color = colores_ciudad.get(ciudad, "#aaaaaa")
        fig3.add_trace(go.Scatter(
            x=df_c["year"],
            y=df_c[cont_tend],
            mode="lines+markers+text",
            name=ciudad,
            line=dict(color=color, width=2.5),
            marker=dict(size=8, color=color, line=dict(color="white", width=1.5)),
            text=[f"{v:.0f}" if i == len(df_c) - 1 else "" for i, v in enumerate(df_c[cont_tend])],
            textposition="middle right",
            textfont=dict(color=color, size=11),
            hovertemplate=f"<b>{ciudad}</b><br>Año: %{{x}}<br>{cont_tend}: %{{y:.1f}} µg/m³<extra></extra>"
        ))

    limite_t = limites_oms.get(cont_tend)
    if limite_t:
        fig3.add_hline(
            y=limite_t,
            line_dash="dash",
            line_color=OMS_COLOR,
            line_width=OMS_WIDTH,
            annotation_text=f"Límite OMS ({limite_t} µg/m³)",
            annotation_position="top left",
            annotation_font_color="black", 
            annotation_font_size=11,
        )

    fig3.update_layout(
        title=dict(text=f"Tendencia anual de {cont_tend} por ciudad (2010–2021)", font_size=16),
        xaxis_title="Año",
        yaxis_title=f"Promedio anual {cont_tend} (µg/m³)",
        height=450,
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor="#eeeeee", dtick=2),
        yaxis=dict(gridcolor="#eeeeee"),
        hovermode="x unified",
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Selecciona al menos una ciudad.")

st.divider()

# ── Conclusión ─────────────────────────────────────────────────────
st.header("Conclusión")
st.markdown("""
Los datos revelan que **el día de la semana sí importa**, pero no de la manera que esperábamos.
El patrón varía por ciudad y contaminante, lo que refleja diferencias en la estructura económica
y los hábitos de movilidad de cada región. Mientras que en el Valle de México el tráfico laboral
domina la semana, en ciudades industriales como Monterrey el comportamiento es distinto.

La tendencia histórica muestra avances reales en algunas ciudades, pero también estancamientos
preocupantes. La calidad del aire en México sigue siendo un resto de salud pública que los datos
ayudan a entender — y a exigir que se atienda.

---
**Fuente de datos:** SINAICA vía Kaggle — *Mexico Hourly Air Pollution (2010-2021)* **Fecha de descarga:** Abril 2026
""")