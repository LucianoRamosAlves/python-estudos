import plotly.graph_objects as go


anos= [1,3,4,5]
qtd = [20,45,67,78]


fig = go.Figure(data = go.Scatter( x = anos, y = qtd))

fig.update_layout(
    title = " Taxa de desaparecidos",
    xaxis_title = "anos",
    yaxis_title = "qtd",
    showlegend = False
)

fig.show()


