import random

from logica.logica import saldos_tamnaho

import plotly.graph_objects as go
import plotly.express as px


ano_2022 = random.randint(10,100)
ano_2023 = random.randint(10,100)
ano_2024 = random.randint(10,100)
ano_2025 = random.randint(10,100)
ano_atual = saldos_tamnaho
print(saldos_tamnaho)

anos = [2022, 2023, 2024, 2025, 2026]
quantidades = [ano_2022, ano_2023, ano_2024, ano_2025, ano_atual]

fig = go.Figure(data = go.Scatter(x = anos, y = quantidades))


#mudo a cor dos traços e no final ativo as bolinhas
fig = px.line(x = anos, y = quantidades, color_discrete_sequence=['red'], markers=True)



fig.update_layout(
    template = "plotly_white",
    title=dict(
        text=" Evolução ao longo dos tempos",
        x=0.5,
        font=dict(size=24)
    ),
    xaxis=dict(
        title= "Ano",
        showgrid=False
    ),
    yaxis=dict(
        title= "Quantidades de Clientes",
         gridcolor="lightgray"
    ),
    title_font_size = 24,

)

fig.update_traces(
    text=quantidades,
    textposition="top left"
)



fig.show()