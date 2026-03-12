
from logica.logica import maior_saldo
from logica.logica import menor_saldo
from logica.logica import saldos


import plotly.graph_objects as go


fig = go.Figure()

# Diagrama de caixa
fig.add_trace(go.Box(
    y=saldos,
    boxpoints=False,   # remove bolinhas
    name="Saldos"
))

# Texto do maior valor
fig.add_annotation(
    x=0,
    y=maior_saldo,
    text=f"Maior: R$ {maior_saldo}",
    showarrow=True,
    arrowhead=2
)

# Texto do menor valor
fig.add_annotation(
    x=0,
    y=menor_saldo,
    text=f"Menor: R$ {menor_saldo}",
    showarrow=True,
    arrowhead=2
)

fig.update_layout(
    title="Distribuição dos Saldos",
    template="plotly_white"
)

fig.show()