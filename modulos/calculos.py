import pandas as pd

# Gabarito oficial
GABARITO = {
    "q1": "a", "q2": "b", "q3": "c", "q4": "c", "q5": "b", "q6": "a", "q7": "c", "q8": "b",
    "q9": {"objetivo": "c", "acao": "c"},
    "q10": {"objetivo": "b", "acao": "c"},
    "q11": {"objetivo": "a", "acao": "c"},
    "q12": {"objetivo": "b", "acao": "a"},
    "q13": {"objetivo": "b", "acao": "a"},
    "q14": {"objetivo": "b", "acao": "a"},
    "q15": ["b", "d"]
}

# Pesos oficiais do TCTOF-BRA
PESOS_GERAL = [0.045, 0.214, 0.301, 0.337, 0.083, 0.255, 0.070, 0.315, 0.403, 0.295, 0.125, 0.559, 0.341, 0.179, 0.252]
PESOS_F1 = [0.006, 0.029, 0.040, 0.045, 0.011, 0.034, 0.009, 0.042, 0.104, 0.076, 0.032, 0.145, 0.088, 0.046, 0.034]
PESOS_F2 = [0.010, 0.046, 0.064, 0.001, 0.000, 0.001, 0.000, 0.002, 0.001, 0.001, 0.002, 0.001, 0.001, 0.001, 0.001]
PESOS_F3 = [0.003, 0.013, 0.018, 0.331, 0.082, 0.250, 0.069, 0.019, 0.025, 0.018, 0.008, 0.034, 0.021, 0.011, 0.015]
PESOS_F4 = [0.004, 0.021, 0.029, 0.033, 0.008, 0.025, 0.007, 0.119, 0.039, 0.029, 0.012, 0.055, 0.033, 0.017, 0.095]

def extrair_letra(texto):
    if not texto:
        return ""
    return str(texto)[0].lower()

def calcular_resultado(session_state):
    acertos = []
    detalhes_respostas = {}

    # 1. Parte 1: Q1 a Q8
    for i in range(1, 9):
        id_q = f"q{i}"
        resposta_usuario = session_state.get(id_q, "")
        letra_usuario = extrair_letra(resposta_usuario)
        correta = GABARITO[id_q]
        pontuou = 1 if letra_usuario == correta else 0
        acertos.append(pontuou)
        detalhes_respostas[id_q] = {"resposta_dada": letra_usuario.upper(), "gabarito": correta.upper(), "pontos": pontuou}

    # 2. Parte 2: Q9 a Q14
    for i in range(9, 15):
        id_q = f"q{i}"
        obj_usuario = extrair_letra(session_state.get(f"obj_{id_q}", ""))
        acao_usuario = extrair_letra(session_state.get(f"acao_{id_q}", ""))
        obj_correto = GABARITO[id_q]["objetivo"]
        acao_correta = GABARITO[id_q]["acao"]
        
        pontuou = 1 if (obj_usuario == obj_correto and acao_usuario == acao_correta) else 0
        acertos.append(pontuou)
        detalhes_respostas[id_q] = {"resposta_dada": f"{obj_usuario.upper()}{acao_usuario.upper()}", "gabarito": f"{obj_correto.upper()}{acao_correta.upper()}", "pontos": pontuou}

    # 3. Parte 3: Q15
    respostas_q15 = session_state.get("multi_q15", [])
    letras_q15 = sorted([extrair_letra(r) for r in respostas_q15])
    gabarito_q15 = sorted(GABARITO["q15"])
    pontuou_q15 = 1 if letras_q15 == gabarito_q15 else 0
    acertos.append(pontuou_q15)
    detalhes_respostas["q15"] = {"resposta_dada": "".join(letras_q15).upper(), "gabarito": "".join(gabarito_q15).upper(), "pontos": pontuou_q15}

    # 4. Cálculo das notas ponderadas escaladas para 10,0
    sg = sum(acertos[i] * PESOS_GERAL[i] for i in range(15))
    sf1 = sum(acertos[i] * PESOS_F1[i] for i in range(15))
    sf2 = sum(acertos[i] * PESOS_F2[i] for i in range(15))
    sf3 = sum(acertos[i] * PESOS_F3[i] for i in range(15))
    sf4 = sum(acertos[i] * PESOS_F4[i] for i in range(15))

    return {
        "acertos_brutos": sum(acertos),
        "total_questoes": 15,
        "tactical_knowledge_score": round(sg * (10 / 3.774), 2),
        "f1_score": round(sf1 * (10 / 0.741), 2),
        "f2_score": round(sf2 * (10 / 0.132), 2),
        "f3_score": round(sf3 * (10 / 0.917), 2),
        "f4_score": round(sf4 * (10 / 0.526), 2),
        "detalhes": detalhes_respostas
    }