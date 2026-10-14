import streamlit as st
import gspread
import pandas as pd
from datetime import datetime

ID_PLANILHA = "1XwKcTYhVpkQJK-M-YdOrBiqQhfLHfnJ8nVtiyHt6Fgo"

@st.cache_resource
def conectar_planilha():
    """
    Conecta ao Google Sheets usando o ID único da planilha.
    """
    credenciais = dict(st.secrets["gcp_service_account"])
    
    if "private_key" in credenciais and isinstance(credenciais["private_key"], str):
        credenciais["private_key"] = credenciais["private_key"].replace("\\n", "\n")
    
    gc = gspread.service_account_from_dict(credenciais)
    planilha = gc.open_by_key(ID_PLANILHA)
    return planilha.sheet1

def ler_dados_planilha():
    """
    Lê os dados da planilha e limpa colunas vazias/duplicadas.
    """
    try:
        aba = conectar_planilha()
        dados = aba.get_all_values()
        
        if not dados or len(dados) <= 1:
            return pd.DataFrame()
            
        cabecalho = dados[0]
        linhas = dados[1:]
        
        df = pd.DataFrame(linhas, columns=cabecalho)
        
        # Remover colunas sem nome
        df = df.loc[:, df.columns != '']
        df = df.loc[:, [col for col in df.columns if str(col).strip() != '']]
        
        # Corrigir nomes de colunas duplicadas
        cols = []
        contagem = {}
        for col in df.columns:
            nome_col = str(col).strip()
            if nome_col in contagem:
                contagem[nome_col] += 1
                cols.append(f"{nome_col}_{contagem[nome_col]}")
            else:
                contagem[nome_col] = 0
                cols.append(nome_col)
        df.columns = cols
        
        return df
    except Exception as e:
        detalhe = str(e) if str(e).strip() else repr(e)
        st.error(f"Erro ao ler a planilha ({type(e).__name__}): {detalhe}")
        return pd.DataFrame()

def teste_ja_realizado(nome_atleta):
    try:
        df = ler_dados_planilha()
        if df.empty or "nome" not in df.columns:
            return False
        nomes = [str(n).strip().lower() for n in df["nome"].tolist()]
        return str(nome_atleta).strip().lower() in nomes
    except Exception:
        return False

def _tratar_num(val, padrao=0.0):
    """
    Converte valores None ou inválidos para números seguros.
    """
    if val is None or val == "" or str(val).strip().lower() == "none":
        return padrao
    try:
        v = float(val)
        return int(v) if v.is_integer() else round(v, 2)
    except (ValueError, TypeError):
        return padrao

def guardar_teste(respostas, resultados):
    """
    Mapeia e guarda os dados sanitizados com base na ordem das colunas da planilha.
    """
    try:
        aba = conectar_planilha()
        
        # 1. Gerar data e hora atual
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # 2. Obter nota geral (testa diferentes nomes de chave possíveis)
        nota_geral = resultados.get("tactical_knowledge_score")
        if nota_geral is None:
            nota_geral = resultados.get("nota_geral", resultados.get("score_geral", 0))

        # 3. Dicionário mapeado e sanitizado (evita None)
        dados_mapeados = {
            "data_hora": respostas.get("data_hora", data_atual),
            "nome": respostas.get("nome", ""),
            "clube": respostas.get("clube", ""),
            "nascimento": respostas.get("nascimento", ""),
            "cidade": respostas.get("cidade", ""),
            "tempo_treino": respostas.get("tempo_treino", ""),
            "posicao": respostas.get("posicao", ""),
            "freq_treino": respostas.get("freq_treino", ""),
            "duracao_treino": respostas.get("duracao_treino", ""),
            "outro_esporte": respostas.get("outro_esporte", ""),
            "q1": respostas.get("q1", ""),
            "q2": respostas.get("q2", ""),
            "q3": respostas.get("q3", ""),
            "q4": respostas.get("q4", ""),
            "q5": respostas.get("q5", ""),
            "q6": respostas.get("q6", ""),
            "q7": respostas.get("q7", ""),
            "q8": respostas.get("q8", ""),
            "q9_obj": respostas.get("obj_q9", respostas.get("q9_obj", "")),
            "q9_acao": respostas.get("acao_q9", respostas.get("q9_acao", "")),
            "q10_obj": respostas.get("obj_q10", respostas.get("q10_obj", "")),
            "q10_acao": respostas.get("acao_q10", respostas.get("q10_acao", "")),
            "q11_obj": respostas.get("obj_q11", respostas.get("q11_obj", "")),
            "q11_acao": respostas.get("acao_q11", respostas.get("q11_acao", "")),
            "q12_obj": respostas.get("obj_q12", respostas.get("q12_obj", "")),
            "q12_acao": respostas.get("acao_q12", respostas.get("q12_acao", "")),
            "q13_obj": respostas.get("obj_q13", respostas.get("q13_obj", "")),
            "q13_acao": respostas.get("acao_q13", respostas.get("q13_acao", "")),
            "q14_obj": respostas.get("obj_q14", respostas.get("q14_obj", "")),
            "q14_acao": respostas.get("acao_q14", respostas.get("q14_acao", "")),
            "q15_respostas": str(respostas.get("multi_q15", "")),
            "acertos_brutos": _tratar_num(resultados.get("acertos_brutos"), 0),
            "total_questoes": _tratar_num(resultados.get("total_questoes"), 15),
            "nota_geral": _tratar_num(nota_geral, 0),
            "f1_score": _tratar_num(resultados.get("f1_score"), 0),
            "f2_score": _tratar_num(resultados.get("f2_score"), 0),
            "f3_score": _tratar_num(resultados.get("f3_score"), 0),
            "f4_score": _tratar_num(resultados.get("f4_score"), 0),
        }
        
        # 4. Ler cabeçalhos reais da folha de cálculo
        cabecalhos = aba.row_values(1)
        
        # 5. Montar a linha garantindo o alinhamento
        linha = [dados_mapeados.get(str(col).strip(), "") for col in cabecalhos if str(col).strip() != ""]
        
        aba.append_row(linha)
        return True
    except Exception as e:
        detalhe = str(e) if str(e).strip() else repr(e)
        st.error(f"Erro ao guardar na planilha ({type(e).__name__}): {detalhe}")
        return False