import plotly.graph_objects as go
from logica.logica import status


mapa = {
    "NEGATIVO": ("red", 0),
    "NEUTRO": ("gold", 1),
    "POSITIVO": ("green", 2)
}

cor_ativa, posicao = mapa[status]

# ==========================================
# 🎨 CORES INICIAIS (apagadas)
# ==========================================

cores = ["lightgray", "lightgray", "lightgray"]
cores[posicao] = cor_ativa

# ==========================================
# 🚦 DESENHANDO O SEMÁFORO
# ==========================================

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[0, 0, 0],
    y=[0, 1, 2],
    mode="markers+text",

    marker=dict(
        size=120,
        color=cores
    ),

    text=["NEGATIVO", "NEUTRO", "POSITIVO"],
    textposition="middle right",
    textfont=dict(size=18)
))

# ==========================================
# 🧹 DESIGN LIMPO (sem bordas)
# ==========================================

fig.update_layout(

    title=f"Status do Banco: {status}",

    xaxis=dict(visible=False),
    yaxis=dict(visible=False),

    plot_bgcolor="white",
    paper_bgcolor="white",

    height=600
)

fig.show()