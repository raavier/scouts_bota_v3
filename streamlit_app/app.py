"""
Scouts Bota - Gerenciador de Pesos
Interface Streamlit para editar base_peso.xlsx
"""

import streamlit as st
import pandas as pd
from components.data_loader import DataLoader
from utils.constants import (
    POSITIONS,
    POSITION_LIST,
    CONSIDERAR_OPTIONS,
    DIRECAO_OPTIONS,
    CATEGORIAS,
    PESO_MIN,
    PESO_MAX,
    PESO_DEFAULT
)

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Scouts Bota - Gerenciador de Pesos",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS CUSTOMIZADO
# ============================================================================

st.markdown("""
<style>
    /* Cabeçalho principal */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }

    /* Cards de indicadores */
    .indicator-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }

    .indicator-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }

    /* Métricas */
    .metric-container {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }

    /* Botões */
    .stButton>button {
        width: 100%;
    }

    /* Divider customizado */
    .custom-divider {
        margin: 2rem 0;
        border-top: 2px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

# Inicializar data loader
if 'loader' not in st.session_state:
    st.session_state.loader = DataLoader()

# Inicializar DataFrame
if 'df' not in st.session_state:
    st.session_state.df = None
    st.session_state.original_df = None

# Inicializar estado de edição
if 'has_changes' not in st.session_state:
    st.session_state.has_changes = False

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def load_data():
    """Carrega dados do arquivo Excel"""
    df = st.session_state.loader.load_weights()
    if df is not None:
        st.session_state.df = df.copy()
        st.session_state.original_df = df.copy()
        st.session_state.has_changes = False
        return True
    return False

def save_data():
    """Salva dados no arquivo Excel"""
    if st.session_state.df is not None:
        success = st.session_state.loader.save_weights(st.session_state.df, create_backup=True)
        if success:
            st.session_state.original_df = st.session_state.df.copy()
            st.session_state.has_changes = False
            st.success("✅ Alterações salvas com sucesso!")
            st.rerun()
        return success
    return False

def reset_changes():
    """Descarta alterações e volta ao estado original"""
    if st.session_state.original_df is not None:
        st.session_state.df = st.session_state.original_df.copy()
        st.session_state.has_changes = False
        st.rerun()

def mark_as_changed():
    """Marca que há alterações não salvas"""
    st.session_state.has_changes = True

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    st.divider()

    # Botão para carregar dados
    if st.button("📁 Carregar Dados", use_container_width=True):
        if load_data():
            st.success("✅ Dados carregados!")

    # Criar arquivo de exemplo se não existir
    if st.session_state.df is None:
        st.divider()
        st.markdown("### 📋 Arquivo não encontrado")
        st.info("Nenhum arquivo base_peso.xlsx encontrado.")

        if st.button("🔨 Criar Arquivo de Exemplo", use_container_width=True):
            if st.session_state.loader.create_sample_file():
                st.success("✅ Arquivo de exemplo criado!")
                if load_data():
                    st.rerun()

    # Informações gerais
    if st.session_state.df is not None:
        st.divider()
        st.markdown("### 📊 Estatísticas")

        total_indicators = len(st.session_state.df)
        active_indicators = len(st.session_state.df[st.session_state.df["CONSIDERAR?"] == "SIM"])
        inactive_indicators = total_indicators - active_indicators

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", total_indicators)
            st.metric("Ativos", active_indicators)
        with col2:
            st.metric("Inativos", inactive_indicators)

        # Indicador de alterações
        if st.session_state.has_changes:
            st.divider()
            st.warning("⚠️ Há alterações não salvas")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Salvar", use_container_width=True):
                    save_data()
            with col2:
                if st.button("↩️ Descartar", use_container_width=True):
                    reset_changes()

        # Backups
        st.divider()
        st.markdown("### 📦 Backups")
        backups = st.session_state.loader.list_backups()
        if backups:
            st.caption(f"{len(backups)} backup(s) disponível(is)")

            # Mostrar último backup
            last_backup = backups[0]
            st.caption(f"Último: {last_backup.name}")
        else:
            st.caption("Nenhum backup disponível")

# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

# Título
st.markdown('<div class="main-header">⚽ Scouts Bota - Gerenciador de Pesos</div>', unsafe_allow_html=True)
st.markdown("Edite os pesos dos indicadores por posição")
st.divider()

# Verificar se dados foram carregados
if st.session_state.df is None:
    st.warning("⚠️ Carregue os dados primeiro usando o botão na barra lateral")
    st.stop()

df = st.session_state.df

# ============================================================================
# SELEÇÃO DE POSIÇÃO
# ============================================================================

st.markdown("### 1️⃣ Selecione a Posição")

# Criar dropdown de posições com labels descritivas
position_options = [f"{code} - {name}" for code, name in POSITIONS.items()]
selected_position_display = st.selectbox(
    "Posição:",
    options=position_options,
    index=0,
    help="Selecione a posição para editar os pesos dos indicadores"
)

# Extrair código da posição (ex: "GK - Goleiro" -> "GK")
selected_position = selected_position_display.split(" - ")[0]

st.divider()

# ============================================================================
# CAMPO DE BUSCA
# ============================================================================

st.markdown("### 2️⃣ Buscar Indicadores")

col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input(
        "Buscar:",
        placeholder="Digite o nome do indicador...",
        help="Filtre indicadores por nome",
        label_visibility="collapsed"
    )

with col2:
    show_only_active = st.checkbox("Apenas Ativos", value=False)

# Filtrar DataFrame
filtered_df = df.copy()

# Aplicar busca
if search_query:
    mask = filtered_df["INDICADOR"].str.contains(search_query, case=False, na=False)
    filtered_df = filtered_df[mask]

# Aplicar filtro de ativos
if show_only_active:
    filtered_df = filtered_df[filtered_df["CONSIDERAR?"] == "SIM"]

# Mostrar contador
st.caption(f"📋 Mostrando {len(filtered_df)} de {len(df)} indicadores")

st.divider()

# ============================================================================
# EDITOR DE INDICADORES
# ============================================================================

st.markdown(f"### 3️⃣ Editar Indicadores - {POSITIONS[selected_position]}")

if len(filtered_df) == 0:
    st.info("🔍 Nenhum indicador encontrado com os filtros aplicados")
else:
    # Iterar sobre cada indicador
    for idx, row in filtered_df.iterrows():
        indicator_name = row["INDICADOR"]

        # Card do indicador
        with st.expander(f"📊 {indicator_name}", expanded=False):

            # Criar 2 colunas: configurações + peso
            col_config, col_peso = st.columns([2, 1])

            # ========== COLUNA DE CONFIGURAÇÕES ==========
            with col_config:
                st.markdown("**⚙️ Configurações do Indicador**")

                # Linha 1: Considerar + Melhor para
                subcol1, subcol2 = st.columns(2)

                with subcol1:
                    new_considerar = st.selectbox(
                        "Considerar?",
                        options=CONSIDERAR_OPTIONS,
                        index=CONSIDERAR_OPTIONS.index(row["CONSIDERAR?"]) if row["CONSIDERAR?"] in CONSIDERAR_OPTIONS else 0,
                        key=f"considerar_{idx}"
                    )

                    if new_considerar != row["CONSIDERAR?"]:
                        st.session_state.df.at[idx, "CONSIDERAR?"] = new_considerar
                        mark_as_changed()

                with subcol2:
                    new_direcao = st.selectbox(
                        "Melhor para",
                        options=DIRECAO_OPTIONS,
                        index=DIRECAO_OPTIONS.index(row["Melhor para"]) if row["Melhor para"] in DIRECAO_OPTIONS else 0,
                        key=f"direcao_{idx}",
                        help="CIMA: maior é melhor | BAIXO: menor é melhor"
                    )

                    if new_direcao != row["Melhor para"]:
                        st.session_state.df.at[idx, "Melhor para"] = new_direcao
                        mark_as_changed()

                # Linha 2: Classificação + Especial
                subcol3, subcol4 = st.columns(2)

                with subcol3:
                    current_categoria = row.get("CLASSIFICACAO RANKING", "")
                    new_categoria = st.text_input(
                        "Classificação Ranking",
                        value=current_categoria if pd.notna(current_categoria) else "",
                        key=f"categoria_{idx}",
                        help="Categoria do indicador (PASS, DEFENSIVE, OFFENSIVE, etc.)"
                    )

                    if new_categoria != current_categoria:
                        st.session_state.df.at[idx, "CLASSIFICACAO RANKING"] = new_categoria
                        mark_as_changed()

                with subcol4:
                    current_especial = row.get("ESPECIAL?", "")
                    new_especial = st.text_input(
                        "Especial?",
                        value=current_especial if pd.notna(current_especial) else "",
                        key=f"especial_{idx}",
                        help="Marcador especial do indicador"
                    )

                    if new_especial != current_especial:
                        st.session_state.df.at[idx, "ESPECIAL?"] = new_especial
                        mark_as_changed()

                # Explicação
                current_explicacao = row.get("Explicação indicador", "")
                new_explicacao = st.text_area(
                    "Explicação",
                    value=current_explicacao if pd.notna(current_explicacao) else "",
                    key=f"explicacao_{idx}",
                    height=80,
                    help="Descrição do que o indicador mede"
                )

                if new_explicacao != current_explicacao:
                    st.session_state.df.at[idx, "Explicação indicador"] = new_explicacao
                    mark_as_changed()

            # ========== COLUNA DE PESO ==========
            with col_peso:
                st.markdown(f"**⚖️ Peso para {POSITIONS[selected_position]}**")

                # Obter valor atual do peso
                current_weight = row.get(selected_position, PESO_DEFAULT)
                if pd.isna(current_weight):
                    current_weight = PESO_DEFAULT
                else:
                    current_weight = float(current_weight)

                # Slider
                new_weight_slider = st.slider(
                    "Ajustar peso:",
                    min_value=PESO_MIN,
                    max_value=PESO_MAX,
                    value=int(current_weight),
                    step=1,
                    key=f"slider_{selected_position}_{idx}",
                    help="Use o slider para ajustar o peso"
                )

                # Input manual
                new_weight_input = st.number_input(
                    "Ou digite:",
                    min_value=PESO_MIN,
                    max_value=PESO_MAX,
                    value=new_weight_slider,
                    step=1,
                    key=f"input_{selected_position}_{idx}",
                    help="Digite um valor exato"
                )

                # Usar o valor do input se foi alterado
                final_weight = new_weight_input

                # Atualizar se mudou
                if final_weight != current_weight:
                    st.session_state.df.at[idx, selected_position] = final_weight
                    mark_as_changed()

                # Mostrar valor atual grande
                st.markdown(f"<div style='text-align: center; font-size: 3rem; font-weight: bold; color: #1f77b4;'>{int(final_weight)}</div>", unsafe_allow_html=True)

                # Barra visual
                percentage = (final_weight / PESO_MAX) * 100
                st.progress(percentage / 100)

# ============================================================================
# RODAPÉ COM AÇÕES
# ============================================================================

if st.session_state.has_changes:
    st.divider()
    st.markdown("### 💾 Salvar Alterações")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("✅ Salvar Todas", type="primary", use_container_width=True):
            save_data()

    with col2:
        if st.button("❌ Descartar Todas", use_container_width=True):
            reset_changes()

    with col3:
        st.info(f"⚠️ {len(filtered_df)} indicador(es) editado(s)")
