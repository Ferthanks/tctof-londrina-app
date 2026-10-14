import plotly.graph_objects as go
import json
import os

def carregar_dados():
    caminho = os.path.join("dados", "posicoes.json")
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def desenhar_campo(cenario_id):
    dados = carregar_dados()
    cenario = dados.get(cenario_id)
    
    fig = go.Figure()

    # 1. Relvado Exterior
    fig.add_shape(type="rect", x0=-10, y0=-6, x1=110, y1=66, fillcolor="#2E7D32", line=dict(width=0), layer="below")
    
    # 2. Relvado Principal e Linhas de Jogo
    fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=60, fillcolor="#4CAF50", line=dict(color="white", width=3), layer="below")
    
    # 3. Marcações Internas
    fig.add_shape(type="line", x0=50, y0=0, x1=50, y1=60, line=dict(color="white", width=2), layer="below")
    fig.add_shape(type="circle", x0=40, y0=20, x1=60, y1=40, line=dict(color="white", width=2), layer="below")
    
    # Grande Área e Pequena Área Esquerda
    fig.add_shape(type="rect", x0=0, y0=10, x1=16, y1=50, line=dict(color="white", width=2), layer="below")
    fig.add_shape(type="rect", x0=0, y0=20, x1=6, y1=40, line=dict(color="white", width=2), layer="below")
    
    # Grande Área e Pequena Área Direita
    fig.add_shape(type="rect", x0=84, y0=10, x1=100, y1=50, line=dict(color="white", width=2), layer="below")
    fig.add_shape(type="rect", x0=94, y0=20, x1=100, y1=40, line=dict(color="white", width=2), layer="below")

    # 4. BALIZAS / GOLS (Y=24 até Y=36 com rede ajustada)
    # Gol Esquerdo
    fig.add_shape(type="rect", x0=-6, y0=24, x1=0, y1=36, fillcolor="rgba(255, 255, 255, 0.35)", line=dict(color="white", width=3))
    for y_net in range(27, 36, 3):
        fig.add_shape(type="line", x0=-6, y0=y_net, x1=0, y1=y_net, line=dict(color="white", width=1, dash="dot"))

    # Gol Direito
    fig.add_shape(type="rect", x0=100, y0=24, x1=106, y1=36, fillcolor="rgba(255, 255, 255, 0.35)", line=dict(color="white", width=3))
    for y_net in range(27, 36, 3):
        fig.add_shape(type="line", x0=100, y0=y_net, x1=106, y1=y_net, line=dict(color="white", width=1, dash="dot"))

    # 5. Defensores (Vermelhos)
    if cenario and "defensores" in cenario:
        x_def, y_def = zip(*cenario["defensores"]) if cenario["defensores"] else ([], [])
        fig.add_trace(go.Scatter(
            x=x_def, y=y_def, 
            mode='markers', 
            marker=dict(size=26, color='#E53935', line=dict(color='white', width=2)),
            name='Defensor', 
            hovertext='Defensor adversário',
            hoverinfo='text'
        ))

    # 6. Atacantes (Azuis)
    if cenario and "atacantes" in cenario:
        x_ata, y_ata = zip(*cenario["atacantes"]) if cenario["atacantes"] else ([], [])
        fig.add_trace(go.Scatter(
            x=x_ata, y=y_ata, 
            mode='markers', 
            marker=dict(size=26, color='#1E88E5', line=dict(color='white', width=2)),
            name='Atacante', 
            hovertext='Companheiro de equipe',
            hoverinfo='text'
        ))

    # 7. Jogador Principal (VOCÊ - Amarelo)
    if cenario and "cinza" in cenario:
        x_cinza, y_cinza = cenario["cinza"]
        fig.add_trace(go.Scatter(
            x=[x_cinza], y=[y_cinza], 
            mode='markers+text', 
            marker=dict(size=30, color='#FDD835', line=dict(color='black', width=3)),
            text=["VOCÊ"], 
            textposition="top center",
            textfont=dict(size=14, color="black", family="Arial Black"),
            name='Você', 
            hovertext='<b>VOCÊ</b><br>Tome a decisão!',
            hoverinfo='text'
        ))

    # 8. Bola
    if cenario and "bola" in cenario:
        x_bola, y_bola = cenario["bola"]
        fig.add_trace(go.Scatter(
            x=[x_bola], y=[y_bola], 
            mode='text', 
            text=['⚽'], 
            textfont=dict(size=22),
            name='Bola', 
            hovertext='Bola',
            hoverinfo='text'
        ))

    fig.update_layout(
        xaxis=dict(visible=False, range=[-12, 112]),
        yaxis=dict(visible=False, range=[-8, 68], scaleanchor="x", scaleratio=1),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="#2E7D32",
        height=480,
        showlegend=False,
        hovermode="closest"
    )
    
    return fig