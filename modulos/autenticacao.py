import json
import os
import streamlit as st

def carregar_usuarios():
    caminho = os.path.join("dados", "usuarios.json")
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Ficheiro 'dados/usuarios.json' não foi encontrado.")
        return {"admin": {}, "alunos": []}

def autenticar(login_input, senha_input):
    dados_usuarios = carregar_usuarios()
    
    # 1. Verifica se é o Admin
    admin_info = dados_usuarios.get("admin", {})
    if login_input.strip() == admin_info.get("login") and senha_input.strip() == admin_info.get("senha"):
        return {"sucesso": True, "role": "admin", "nome": admin_info.get("nome")}

    # 2. Verifica se é Aluno (Login = Nome, Senha = Data de nascimento 'AAAA-MM-DD' ou 'DD/MM/AAAA')
    login_limpo = login_input.strip().lower()
    senha_limpa = senha_input.strip().replace("/", "-")

    for aluno in dados_usuarios.get("alunos", []):
        nome_aluno = aluno.get("nome", "").strip().lower()
        nasc_aluno = str(aluno.get("nascimento", "")).strip().replace("/", "-")
        
        if login_limpo == nome_aluno and senha_limpa == nasc_aluno:
            return {
                "sucesso": True, 
                "role": "aluno", 
                "nome": aluno.get("nome"),
                "nascimento": aluno.get("nascimento")
            }

    return {"sucesso": False, "role": None, "nome": None}

def renderizar_tela_login():
    st.subheader("🔑 Acesso ao Sistema TCTOF-BRA")
    
    tipo_usuario = st.radio("Selecione o tipo de acesso:", ["Aluno", "Administrador / Professor"], horizontal=True)
    
    if tipo_usuario == "Aluno":
        login_input = st.text_input("Nome Completo (Conforme cadastrado):")
        senha_input = st.text_input("Data de Nascimento (Ex: 24082007):", type="password")
    else:
        login_input = st.text_input("Usuário Admin:")
        senha_input = st.text_input("Senha Admin:", type="password")
        
    if st.button("Entrar no Sistema 🚀"):
        resultado = autenticar(login_input, senha_input)
        if resultado["sucesso"]:
            st.session_state.usuario_logado = True
            st.session_state.usuario_role = resultado["role"]
            st.session_state.usuario_nome = resultado["nome"]
            st.session_state.nome = resultado["nome"] # Preenche automaticamente no formulário
            if resultado.get("nascimento"):
                st.session_state.nascimento_cadastrado = resultado["nascimento"]
            st.success(f"Bem-vindo(a), {resultado['nome']}!")
            st.rerun()
        else:
            st.error("Credenciais incorretas. Verifique seu nome e data de nascimento com o professor.")