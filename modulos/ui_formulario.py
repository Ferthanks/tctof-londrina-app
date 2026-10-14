import streamlit as st

def renderizar_dados_pessoais():
    st.header("📋 Perfil do Atleta")
    
    # Recupera informações salvas na sessão do login
    nome_usuario = st.session_state.get("usuario_nome", "")
    nasc_usuario = st.session_state.get("nascimento_cadastrado", "")

    # Exibição dos dados salvos no login (Londrina EC Sub-20)
    st.info(
        f"👤 **Atleta:** {nome_usuario}  \n"
        f"📅 **Data de Nascimento:** {nasc_usuario}  \n"
        f"🛡️ **Equipe:** Londrina EC — Sub-20"
    )

    st.markdown("---")
    st.subheader("⚽ Histórico e Perfil de Treino")

    st.text_input("Cidade/UF de Origem:", key="cidade", placeholder="Ex: Londrina - PR")

    # V) Há quantos anos você treina futebol
    st.selectbox(
        "V) Há quantos anos você treina futebol (não considerar futsal; apenas futebol)?",
        options=[
            "Menos de 1 ano",
            "1 a 2 anos",
            "2 a 3 anos",
            "3 a 4 anos",
            "4 a 5 anos",
            "5 a 6 anos",
            "6 a 7 anos",
            "7 a 8 anos",
            "8 a 9 anos",
            "9 a 10 anos",
            "Mais de 10 anos",
            "Não participo regularmente de treinos de futebol"
        ],
        index=None,
        placeholder="Selecione...",
        key="tempo_treino"
    )

    # VI) Posição de jogo
    st.selectbox(
        "VI) Posição de jogo que mais atua:",
        options=[
            "Goleiro",
            "Zagueiro",
            "Lateral",
            "Volante / Primeiro homem do meio-campo",
            "Meia-Central / Segundo homem do meio-campo",
            "Meia Atacante / Camisa 10",
            "Ponta / Extremo",
            "Centroavante"
        ],
        index=None,
        placeholder="Selecione sua posição...",
        key="posicao"
    )

    col1, col2 = st.columns(2)

    with col1:
        # VII) Frequência semanal
        st.selectbox(
            "VII) Quantas vezes por semana você treina futebol?",
            options=["1", "2", "3", "4", "5", "6", "7"],
            index=None,
            placeholder="Selecione...",
            key="freq_treino"
        )

    with col2:
        # VIII) Tempo de duração
        st.selectbox(
            "VIII) Qual o tempo de duração de cada treino?",
            options=["1h", "1h15", "1h30", "2h", "Outro"],
            index=None,
            placeholder="Selecione...",
            key="duracao_treino"
        )

    # IX) Outra modalidade esportiva
    treina_outra = st.radio(
        "IX) Você já treinou ou treina (regularmente) outra modalidade esportiva?",
        options=["Não", "Sim"],
        index=None,
        key="outra_modalidade_radio"
    )

    if treina_outra == "Sim":
        st.text_input("Se sim, quais?", key="outro_esporte", placeholder="Ex: Futsal, Natação, Basquete...")
    elif treina_outra == "Não":
        st.session_state["outro_esporte"] = "Não"


def renderizar_parte_teorica():
    st.header("Parte 1 - Conhecimento Teórico (Q1 a Q8)")
    st.markdown("Leia atentamente cada pergunta e selecione a alternativa correta.")

    st.radio(
        "1) O que você entende por manter a posse de bola?",
        [
            "a) Conservar a posse de bola e não perdê-la.",
            "b) Progredir em direção ao gol adversário.",
            "c) Tentar marcar um gol."
        ],
        key="q1",
        index=None
    )

    st.radio(
        "2) O que você entende por avançar em direção ao gol adversário?",
        [
            "a) Conservar a posse de bola e não perdê-la.",
            "b) Progredir em direção ao gol adversário.",
            "c) Tentar marcar um gol."
        ],
        key="q2",
        index=None
    )

    st.radio(
        "3) O que você entende por atacar a meta adversária?",
        [
            "a) Conservar a posse de bola e não perdê-la.",
            "b) Progredir em direção ao gol adversário.",
            "c) Tentar marcar um gol."
        ],
        key="q3",
        index=None
    )

    st.radio(
        "4) Dar amplitude ao ataque é:",
        [
            "a) Colocar a bola em jogo mediante uma estratégia individual ou coletiva.",
            "b) O deslocamento dos jogadores no ataque em direção ao gol adversário, ocupando razoavelmente o espaço de jogo.",
            "c) O deslocamento dos jogadores no ataque, aumentando “até as laterais” a distância entre os mesmos e ocupando razoavelmente o espaço de jogo."
        ],
        key="q4",
        index=None
    )

    st.radio(
        "5) Dar profundidade ao ataque é:",
        [
            "a) Colocar a bola em jogo mediante uma estratégia individual ou coletiva.",
            "b) O deslocamento dos jogadores no ataque em direção ao gol adversário, ocupando razoavelmente o espaço de jogo.",
            "c) O deslocamento dos jogadores no ataque, aumentando “até as laterais” a distância entre os mesmos e ocupando razoavelmente o espaço de jogo."
        ],
        key="q5",
        index=None
    )

    st.radio(
        "6) Criar situações de superioridade numérica no ataque são:",
        [
            "a) Deslocamentos dos jogadores no ataque, que têm como objetivo conseguir uma situação de jogo em que haja mais atacantes que defensores.",
            "b) Deslocamentos dos jogadores no ataque, com bola e sem bola, criando espaços livres.",
            "c) Deslocamentos dos jogadores no ataque, que têm como objetivo conseguir uma situação de jogo em que haja mais defensores que atacantes."
        ],
        key="q6",
        index=None
    )

    st.radio(
        "7) Criar espaços livres são:",
        [
            "a) Deslocamentos dos jogadores no ataque, que têm como objetivo conseguir uma situação de jogo em que haja mais atacantes que defensores.",
            "b) Deslocamentos dos jogadores no ataque, reduzindo a distância entre os mesmos e ocupando razoavelmente o espaço de jogo.",
            "c) Deslocamentos no ataque que provocam a saída dos defensores da zona que ocupam, com a finalidade de facilitar a entrada de um companheiro atacante."
        ],
        key="q7",
        index=None
    )

    st.radio(
        "8) No futebol, um jogador está em posição de impedimento quando:",
        [
            "a) Se encontra na metade do campo adversário, mais próximo da linha de fundo e atrás da linha da bola.",
            "b) Se encontra na metade do campo adversário, mais próximo da linha de fundo do que o penúltimo oponente e a bola.",
            "c) Se encontra na metade do campo adversário, na mesma linha que o penúltimo oponente."
        ],
        key="q8",
        index=None
    )