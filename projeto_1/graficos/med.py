import plotly.graph_objects as go

from logica.logica import pocent_positivos
from logica.logica import recomendacao



# ==============================
# 🎯 CRIANDO O MEDIDOR (GAUGE)
# ==============================

fig = go.Figure(go.Indicator(

    # 👉 tipo do gráfico
    mode="gauge+number",

    # 👉 valor do score
    value=pocent_positivos,

    # 👉 título e subtítulo
    title={
        "text": f"Score Financeiro<br><span style='font-size:16px;color:gray'>{recomendacao}</span>",
        "font": {"size": 28}
    },

    # ==============================
    # 🎯 CONFIGURAÇÃO DO MEDIDOR
    # ==============================

    gauge={

        # 👉 formato semicircular (moderno)
        "shape": "angular",

        # 👉 eixo do medidor
        "axis": {
            "range": [0, 100],
            "tickwidth": 0,   # remove números do eixo
        },

        # 👉 remove borda interna
        "borderwidth": 0,

        # 👉 cores das faixas (níveis)
        "steps": [

            # RUIM
            {"range": [0, 30], "color": "#ff4d4d"},

            # ALERTA
            {"range": [30, 50], "color": "#ff9933"},

            # MÉDIO
            {"range": [50, 70], "color": "#ffd633"},

            # BOM
            {"range": [70, 85], "color": "#33cc66"},

            # EXCELENTE
            {"range": [85, 100], "color": "#00994d"},
        ],

        # 👉 barra que mostra o valor atual
        "bar": {
            "color": "#1f2c3d",
            "thickness": 0.35   # grossura da barra
        },

        # 👉 linha indicadora (ponteiro)
        "threshold": {
            "line": {"color": "black", "width": 4},
            "thickness": 0.75,
            "value": pocent_positivos
        }
    }
))

# ==============================
# 🎯 REMOVER TODAS AS BORDAS
# ==============================

fig.update_layout(

    # fundo limpo
    paper_bgcolor="white",
    plot_bgcolor="white",

    # remove margens externas
    margin=dict(l=20, r=20, t=80, b=20),

    # fonte geral
    font=dict(
        family="Segoe UI",
        size=18,
        color="#2c3e50"
    )
)

# ==============================
# 🎯 MOSTRAR GRÁFICO
# ==============================

fig.show()