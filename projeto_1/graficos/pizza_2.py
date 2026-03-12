import plotly.graph_objects as go
from logica.logica import qtd_vip
from logica.logica import qtd_premium
from logica.logica import qtd_normais
from logica.logica import qtd_restritos


# ==========================================
# 🧠 LISTAS DO GRÁFICO
# ==========================================

valores = [qtd_vip, qtd_premium, qtd_normais, qtd_restritos]

categorias = [
    "Clientes VIP",
    "Clientes Premium",
    "Clientes Normais",
    "Clientes Restritos"
]

# ==========================================
# 🎨 CORES PROFISSIONAIS (psicologia visual)
# ==========================================

cores = [
    "#D4AF37",   # DOURADO → VIP (luxo)
    "#5DADE2",   # AZUL → Premium (confiança)
    "#58D68D",   # VERDE → Normal (estável)
    "#E74C3C"    # VERMELHO → Restrito (risco)
]

# ==========================================
# 🥧 CRIANDO O GRÁFICO DE PIZZA
# ==========================================

fig = go.Figure(data=[go.Pie(

    labels=categorias,   # nomes das fatias
    values=valores,      # valores

    # mostra porcentagem + nome
    textinfo="label+percent",

    # deixa bordas suaves
    marker=dict(colors=cores, line=dict(color="white", width=2)),

    # cria efeito moderno (tipo dashboard)
    hole=0.45
)])

# ==========================================
# ✨ DESIGN PROFISSIONAL
# ==========================================

fig.update_layout(

    title="Distribuição de Clientes por Categoria",

    # fundo limpo
    paper_bgcolor="white",

    # fonte moderna
    font=dict(size=16),

    # centraliza o título
    title_x=0.5
)

fig.show()