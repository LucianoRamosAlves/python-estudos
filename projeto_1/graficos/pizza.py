import matplotlib.pyplot as plt
from logica.logica import qtd_positivos
from logica.logica import qtd_negativados

# ==============================
# DADOS DO GRÁFICO
# ==============================

labels = ['Clientes Positivos', 'Clientes Negativados']
valores = [qtd_positivos, qtd_negativados]

# Cores personalizadas
cores = ['#2ecc71', '#e74c3c']  # verde e vermelho profissional

# Destacar a fatia dos negativados
explode = (0, 0.1)

# ==============================
# CRIAÇÃO DO GRÁFICO
# ==============================

plt.figure(figsize=(8, 6))

plt.pie(
    valores,
    labels=labels,
    colors=cores,
    explode=explode,
    autopct='%1.1f%%',   # mostra porcentagem
    shadow=True,
    startangle=90,
    textprops={'fontsize': 12, 'fontweight': 'bold'}
)

# Título
plt.title(
    'Distribuição de Clientes',
    fontsize=16,
    fontweight='bold'
)

# Deixa redondo perfeito
plt.axis('equal')

# Exibir gráfico
plt.show()
