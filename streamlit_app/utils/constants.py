"""
Constants for Streamlit App
"""

# Posições disponíveis (12 posições)
POSITIONS = {
    "GK": "Goleiro",
    "CB": "Zagueiro Central",
    "RCB": "Zagueiro Direito",
    "LCB": "Zagueiro Esquerdo",
    "RB": "Lateral Direito",
    "LB": "Lateral Esquerdo",
    "DM": "Volante",
    "CM": "Meio-Campo Central",
    "AM": "Meia Atacante",
    "LW": "Ponta Esquerda",
    "RW": "Ponta Direita",
    "CF": "Centro-Avante"
}

# Lista de posições em ordem
POSITION_LIST = ["GK", "CB", "RCB", "LCB", "RB", "LB", "DM", "CM", "AM", "LW", "RW", "CF"]

# Opções para "Considerar?"
CONSIDERAR_OPTIONS = ["SIM", "NÃO"]

# Opções para "Melhor para"
DIRECAO_OPTIONS = ["CIMA", "BAIXO"]

# Categorias conhecidas (baseado no código)
CATEGORIAS = [
    "PASS",
    "DEFENSIVE",
    "OFFENSIVE",
    "DGP",
    "GK"
]

# Colunas obrigatórias do arquivo base_peso.xlsx
REQUIRED_COLUMNS = [
    "INDICADOR",
    "CLASSIFICACAO RANKING",
    "SUBCLASSIFICACAO RANKING",
    "CONSIDERAR?",
    "ESPECIAL?",
    "Melhor para",
    "tipo_agreg",
    "Explicação indicador"
] + POSITION_LIST

# Range de valores para pesos
PESO_MIN = 0
PESO_MAX = 100
PESO_DEFAULT = 50
