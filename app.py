import json
import pandas as pd
import streamlit as st
from modulos import ui_formulario, prancheta, calculos, armazenamento, autenticacao

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="TCTOF-BRA | Avaliação Tática",
    page_icon="⚽",
    layout="centered"
)

# Inicialização do dicionário permanente de respostas
if 'respostas' not in st.session_state:
    st.session_state.respostas = {}

# 2. Carregamento dos dados das questões do JSON
@st.cache_data
def carregar_questoes():
    try:
        with open("dados/questao.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Ficheiro 'dados/questao.json' não foi encontrado.")
        return {}

questoes = carregar_questoes()

# 3. Título Principal
st.title("⚽ Teste de Conhecimento Tático Ofensivo no Futebol (TCTOF-BRA)")
st.markdown("---")

# 4. Tela de Login e Autenticação
if 'usuario_logado' not in st.session_state or not st.session_state.usuario_logado:
    autenticacao.renderizar_tela_login()
    st.stop()

# 5. Barra Superior de Controle de Usuário
col_user, col_logout = st.columns([3, 1])
col_user.caption(f"👤 Logado como: **{st.session_state.usuario_nome}** ({st.session_state.usuario_role.upper()})")
if col_logout.button("Sair / Logout"):
    st.session_state.clear()
    st.rerun()

st.markdown("---")

# 6. TRAVA DE SEGURANÇA: Bloqueia atletas que já responderam ao teste
if st.session_state.usuario_role == "aluno":
    if armazenamento.teste_ja_realizado(st.session_state.usuario_nome) and st.session_state.get('etapa', 1) != 4:
        st.warning("⚠️ Você já realizou este teste anteriormente!")
        st.info(
            "Cada atleta pode responder ao TCTOF-BRA apenas uma única vez.\n\n"
            "Seus dados e notas já foram registrados e enviados para a comissão técnica. "
            "Caso precise refazer por algum motivo, entre em contato com o responsável."
        )
        st.stop()

# 7. PAINEL EXCLUSIVO DO ADMINISTRADOR (Análise e Visualização de Resultados)
if st.session_state.usuario_role == "admin":
    st.header("📊 Painel Geral de Resultados (Admin)")
    st.caption("Visão gerencial de desempenho tático do elenco em tempo real.")
    
    df_dados = armazenamento.ler_dados_planilha()
    
    if df_dados.empty:
        st.warning("Nenhum teste foi registrado no banco de dados até o momento.")
    else:
        # Converter colunas numéricas de texto para número e tratar valores nulos (None/NaN)
        colunas_numericas = ['nota_geral', 'acertos_brutos', 'total_questoes', 'f1_score', 'f2_score', 'f3_score', 'f4_score']
        for col in colunas_numericas:
            if col in df_dados.columns:
                # Substitui textos 'None', 'nan' ou vazios por 0 antes da conversão
                s_limpa = df_dados[col].astype(str).replace(['None', 'none', 'nan', 'NaN', ''], '0')
                df_dados[col] = pd.to_numeric(s_limpa, errors='coerce').fillna(0)

        st.subheader("📈 Estatísticas da Equipe")
        
        media_geral = df_dados['nota_geral'].mean() if not df_dados.empty else 0.0
        media_acertos = df_dados['acertos_brutos'].mean() if not df_dados.empty else 0.0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Avaliações", len(df_dados))
        col2.metric("Média Geral da Equipe", f"{media_geral:.2f} / 10")
        col3.metric("Média de Acertos Brutos", f"{media_acertos:.1f} / 15")
        
        st.markdown("**Desempenho Médio por Categoria (Fatores)**")
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        col_f1.metric("F1: Decisão", f"{df_dados['f1_score'].mean():.2f}")
        col_f2.metric("F2: Princípios", f"{df_dados['f2_score'].mean():.2f}")
        col_f3.metric("F3: Elementos", f"{df_dados['f3_score'].mean():.2f}")
        col_f4.metric("F4: Impedimento", f"{df_dados['f4_score'].mean():.2f}")
        
        if 'posicao' in df_dados.columns:
            st.markdown("**Desempenho Médio por Posição em Campo**")
            df_posicao = df_dados.groupby('posicao')['nota_geral'].mean().reset_index()
            df_posicao.rename(columns={'posicao': 'Posição', 'nota_geral': 'Nota Média'}, inplace=True)
            st.dataframe(df_posicao.style.format({'Nota Média': '{:.2f}'}), use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("📋 Banco de Dados Completo")
        st.dataframe(df_dados, use_container_width=True)
        
        csv = df_dados.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Planilha (CSV)", data=csv, file_name="resultados_tctof.csv", mime="text/csv")

    st.stop()

# 8. Controle do Fluxo do Teste (Etapas 1 a 4 - Exclusivo para Alunos)
if 'etapa' not in st.session_state:
    st.session_state.etapa = 1

def proxima_etapa():
    st.session_state.etapa += 1

def etapa_anterior():
    st.session_state.etapa -= 1

# === ETAPA 1: PERFIL DO ATLETA ===
if st.session_state.etapa == 1:
    ui_formulario.renderizar_dados_pessoais()
    if st.button("Avançar para Parte 1 (Teórica) ➡"):
        # Gravação automática dos dados do usuário logado
        st.session_state.respostas["nome"] = st.session_state.get("usuario_nome", "")
        st.session_state.respostas["nascimento"] = st.session_state.get("nascimento_cadastrado", "")
        st.session_state.respostas["clube"] = "Londrina EC - Sub-20"
        
        # Salva as respostas das informações complementares
        campos_complementares = ["cidade", "posicao", "tempo_treino", "freq_treino", "duracao_treino", "outro_esporte"]
        for campo in campos_complementares:
            if campo in st.session_state:
                st.session_state.respostas[campo] = st.session_state[campo]
                
        proxima_etapa()
        st.rerun()

# === ETAPA 2: PARTE TEÓRICA (Q1 a Q8) ===
elif st.session_state.etapa == 2:
    ui_formulario.renderizar_parte_teorica()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Voltar"):
            etapa_anterior()
            st.rerun()
    with col2:
        if st.button("Avançar para Parte 2 (Cenários) ➡️"):
            # VALIDAÇÃO: Verifica se as questões de 1 a 8 estão preenchidas
            questoes_em_falta = []
            for i in range(1, 9):
                chave = f"q{i}"
                # Verifica se a chave existe no session_state e se não está vazia/None
                if not st.session_state.get(chave):
                    questoes_em_falta.append(f"Q{i}")
            
            if questoes_em_falta:
                st.error(f"⚠️ Por favor, responda às seguintes questões antes de avançar: {', '.join(questoes_em_falta)}")
            else:
                # Salva respostas teóricas permanentemente
                for i in range(1, 9):
                    chave = f"q{i}"
                    st.session_state.respostas[chave] = st.session_state[chave]
                proxima_etapa()
                st.rerun()

# === ETAPA 3: CENÁRIOS SITUACIONAIS (Q9 a Q15) ===
elif st.session_state.etapa == 3:
    if 'questao_atual' not in st.session_state:
        st.session_state.questao_atual = 9
    
    q_atual = st.session_state.questao_atual
    id_cenario = f"q{q_atual}"
    
    dados_q = questoes.get(id_cenario, {})
    pergunta_texto = dados_q.get("pergunta", "Analise a jogada abaixo e tome sua decisão.")
    
    st.subheader(f"Parte 2 - Cenários Situacionais ({q_atual}/15)")
    st.markdown(f"**Questão {q_atual}:** {pergunta_texto}")
    
    # Lógica Exclusiva para a Questão 15 (Múltipla Escolha - Impedimento)
    if q_atual == 15:
        col_img1, col_img2 = st.columns(2)
        
        with col_img1:
            st.markdown("**a)**")
            st.plotly_chart(prancheta.desenhar_campo("q15a"), use_container_width=True)
            st.markdown("**c)**")
            st.plotly_chart(prancheta.desenhar_campo("q15c"), use_container_width=True)
            
        with col_img2:
            st.markdown("**b)**")
            st.plotly_chart(prancheta.desenhar_campo("q15b"), use_container_width=True)
            st.markdown("**d)**")
            st.plotly_chart(prancheta.desenhar_campo("q15d"), use_container_width=True)

        opcoes_q15 = dados_q.get("opcoes", [
            "a) Imagem a",
            "b) Imagem b",
            "c) Imagem c",
            "d) Imagem d"
        ])
        
        def_q15 = st.session_state.respostas.get("multi_q15", [])
        sel_q15 = st.multiselect(
            "Selecione em quais imagens você estaria em posição de impedimento:",
            options=opcoes_q15,
            default=def_q15,
            key="widget_multi_q15"
        )
        # Salva permanentemente a resposta da Q15
        st.session_state.respostas["multi_q15"] = sel_q15

    # Lógica Padrão para as Questões 9 a 14
    else:
        figura = prancheta.desenhar_campo(id_cenario)
        st.plotly_chart(figura, use_container_width=True)
        
        opcoes_obj = dados_q.get("opcoes_objetivo", [
            "a) Manter a posse de bola e não perdê-la.", 
            "b) Avançar em direção ao gol adversário.", 
            "c) Atacar a meta adversária."
        ])
        
        subtitulo_acao = dados_q.get("subtitulo_acao", "Realizando para isso:")
        
        opcoes_acao = dados_q.get("opcoes_acao", [
            "a) Um passe ao companheiro mais próximo.", 
            "b) Uma condução em direção ao gol adversário.", 
            "c) Um chute ao gol."
        ])
        
        # Recupera valores salvos para manter a seleção visível ao navegar
        val_obj = st.session_state.respostas.get(f"obj_{id_cenario}")
        idx_obj = opcoes_obj.index(val_obj) if val_obj in opcoes_obj else None

        val_acao = st.session_state.respostas.get(f"acao_{id_cenario}")
        idx_acao = opcoes_acao.index(val_acao) if val_acao in opcoes_acao else None

        sel_obj = st.radio(
            "Qual seu objetivo?", 
            opcoes_obj, 
            index=idx_obj,
            key=f"widget_obj_{id_cenario}"
        )
        
        sel_acao = st.radio(
            subtitulo_acao, 
            opcoes_acao, 
            index=idx_acao,
            key=f"widget_acao_{id_cenario}"
        )

        # Atualiza o dicionário permanente de respostas
        if sel_obj:
            st.session_state.respostas[f"obj_{id_cenario}"] = sel_obj
        if sel_acao:
            st.session_state.respostas[f"acao_{id_cenario}"] = sel_acao

    # Botões de Navegação entre Questões
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Voltar"):
            if q_atual > 9:
                st.session_state.questao_atual -= 1
                st.rerun()
            else:
                etapa_anterior()
                st.rerun()
    with col2:
        if q_atual < 15:
            if st.button("Próximo Cenário ➡️"):
                # VALIDAÇÃO: Bloqueia se o Objetivo ou Ação não foram selecionados
                if not sel_obj or not sel_acao:
                    st.error("⚠️ Por favor, selecione uma opção para o **Objetivo** e para a **Ação** antes de avançar.")
                else:
                    st.session_state.questao_atual += 1
                    st.rerun()
        else:
            if st.button("Finalizar Teste ✅"):
                # VALIDAÇÃO: Bloqueia a Q15 se nada for selecionado
                if not sel_q15:
                    st.error("⚠️ Por favor, selecione pelo menos uma opção na Questão 15 antes de finalizar.")
                else:
                    proxima_etapa()
                    st.rerun()

# === ETAPA 4: RESULTADOS E PROCESSAMENTO FINAL ===
elif st.session_state.etapa == 4:
    st.success("🎉 Teste finalizado com sucesso!")
    
    resultados = calculos.calcular_resultado(st.session_state.respostas)
    
    if 'guardado' not in st.session_state or not st.session_state.guardado:
        armazenamento.guardar_teste(st.session_state.respostas, resultados)
        st.session_state.guardado = True
        st.toast("Resultados salvos com sucesso no sistema! 💾")
    
    nome_atleta = st.session_state.respostas.get('nome', st.session_state.get('usuario_nome', 'Atleta'))
    st.header(f"📊 Desempenho Tático: {nome_atleta}")
    st.divider()

    col_g, col_f1, col_f2, col_f3, col_f4 = st.columns(5)
    col_g.metric("Nota Geral", f"{resultados['tactical_knowledge_score']} / 10")
    col_f1.metric("F1: Decisão", f"{resultados['f1_score']}")
    col_f2.metric("F2: Princípios", f"{resultados['f2_score']}")
    col_f3.metric("F3: Elementos", f"{resultados['f3_score']}")
    col_f4.metric("F4: Impedimento", f"{resultados['f4_score']}")

    st.subheader(f"Total de Acertos: {resultados['acertos_brutos']} de {resultados['total_questoes']}")
    st.info("Suas respostas foram registradas no sistema da comissão técnica.")

    if st.button("🔴 Finalizar Sessão e Sair"):
        st.session_state.clear()
        st.rerun()