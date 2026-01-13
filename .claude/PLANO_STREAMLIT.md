# Plano de Implementação - Interface Streamlit para Gerenciamento de Pesos

## 📋 Resumo Executivo

Criar uma interface web usando **Streamlit** que permita aos usuários visualizar, editar e gerenciar o arquivo `base_peso.xlsx` de forma intuitiva, sem precisar editar planilhas Excel manualmente.

---

## 🎯 Objetivos

1. **Visualização**: Exibir a tabela de pesos de forma clara e organizada
2. **Edição**: Permitir edição inline dos pesos por posição
3. **Validação**: Garantir integridade dos dados (tipos, ranges, valores obrigatórios)
4. **Importação/Exportação**: Importar Excel existente e exportar modificações
5. **Isolamento**: Não interferir no pipeline de processamento existente

---

## 📊 Estrutura do Arquivo `base_peso.xlsx`

### Colunas Identificadas:

| Coluna | Tipo | Descrição | Valores |
|--------|------|-----------|---------|
| **INDICADOR** | string | Nome do indicador (ex: "Passes Attempted") | Único, obrigatório |
| **CLASSIFICACAO RANKING** | string | Categoria principal | PASS, DEFENSIVE, OFFENSIVE, DGP, GK |
| **SUBCLASSIFICACAO RANKING** | string | Subcategoria | Varia por categoria |
| **CONSIDERAR?** | string | Indica se está ativo | "SIM" ou "NÃO" |
| **ESPECIAL?** | string | Marcador especial | Valores diversos |
| **Melhor para** | string | Direção de normalização | "CIMA" ou "BAIXO" |
| **tipo_agreg** | string | Tipo de agregação | Valores diversos |
| **GK** | float | Peso para Goleiro | 0-100 |
| **RCB** | float | Peso para Zagueiro Direito | 0-100 |
| **LCB** | float | Peso para Zagueiro Esquerdo | 0-100 |
| **CB** | float | Peso para Zagueiro Central | 0-100 |
| **RB** | float | Peso para Lateral Direito | 0-100 |
| **LB** | float | Peso para Lateral Esquerdo | 0-100 |
| **DM** | float | Peso para Volante | 0-100 |
| **CM** | float | Peso para Meio-Campo Central | 0-100 |
| **AM** | float | Peso para Meia Atacante | 0-100 |
| **LW** | float | Peso para Ponta Esquerda | 0-100 |
| **RW** | float | Peso para Ponta Direita | 0-100 |
| **CF** | float | Peso para Centro-Avante | 0-100 |
| **Explicação indicador** | string | Descrição do indicador | Texto livre |

### Dados Conhecidos:
- **Total de indicadores**: 206
- **Indicadores ativos** (CONSIDERAR? = SIM): 109
- **Posições suportadas**: 12

---

## 🏗️ Arquitetura Proposta

### Estrutura de Diretórios

```
scouts_bota_v3/
├── streamlit_app/              # Nova pasta (isolada)
│   ├── __init__.py
│   ├── app.py                  # Aplicação principal Streamlit
│   ├── components/             # Componentes reutilizáveis
│   │   ├── __init__.py
│   │   ├── data_loader.py      # Carrega/salva Excel
│   │   ├── data_editor.py      # Editor de tabela
│   │   ├── filters.py          # Filtros e buscas
│   │   └── validators.py       # Validação de dados
│   ├── pages/                  # Páginas multi-page
│   │   ├── 1_📊_Visualizar.py
│   │   ├── 2_✏️_Editar.py
│   │   ├── 3_➕_Adicionar.py
│   │   ├── 4_📥_Importar.py
│   │   └── 5_⚙️_Configurar.py
│   ├── utils/                  # Utilitários
│   │   ├── __init__.py
│   │   ├── constants.py        # Constantes (posições, categorias)
│   │   └── helpers.py          # Funções auxiliares
│   └── assets/                 # CSS, imagens
│       └── styles.css
├── config/
│   └── streamlit_config.yaml   # Config específico do Streamlit
├── requirements_streamlit.txt  # Dependências adicionais
├── run_streamlit.bat           # Script de execução Windows
└── (arquivos existentes...)
```

---

## 🎨 Funcionalidades por Página

### 1. 📊 Página: Visualizar

**Objetivo**: Visualização geral dos pesos

**Funcionalidades**:
- [ ] Exibir tabela completa com todos os indicadores
- [ ] Filtros por:
  - Categoria (CLASSIFICACAO RANKING)
  - Subcategoria (SUBCLASSIFICACAO RANKING)
  - Status (CONSIDERAR? = SIM/NÃO)
  - Direção (Melhor para: CIMA/BAIXO)
- [ ] Busca por nome do indicador
- [ ] Ordenação por colunas
- [ ] Exportar vista filtrada para CSV
- [ ] Estatísticas resumidas:
  - Total de indicadores
  - Indicadores ativos/inativos
  - Média de pesos por posição

### 2. ✏️ Página: Editar

**Objetivo**: Edição inline dos pesos

**Funcionalidades**:
- [ ] Editor de tabela interativo (`st.data_editor`)
- [ ] Edição de pesos por posição (0-100)
- [ ] Edição de metadados:
  - CONSIDERAR? (toggle SIM/NÃO)
  - Melhor para (CIMA/BAIXO)
  - Categoria/Subcategoria (dropdown)
- [ ] Validação em tempo real:
  - Pesos entre 0-100
  - Campos obrigatórios preenchidos
- [ ] Destacar células editadas
- [ ] Botão "Salvar Alterações"
- [ ] Botão "Desfazer Alterações"
- [ ] Histórico de modificações (log)

### 3. ➕ Página: Adicionar

**Objetivo**: Adicionar novos indicadores

**Funcionalidades**:
- [ ] Formulário para novo indicador:
  - Nome do indicador
  - Categoria e subcategoria
  - Direção (CIMA/BAIXO)
  - Pesos para cada posição (sliders 0-100)
  - Explicação
- [ ] Validação:
  - Nome único
  - Todos os campos obrigatórios
- [ ] Preview antes de adicionar
- [ ] Botão "Adicionar Indicador"

### 4. 📥 Página: Importar/Exportar

**Objetivo**: Gerenciar arquivos

**Funcionalidades**:
- [ ] **Importar**:
  - Upload de arquivo Excel
  - Validação de estrutura
  - Preview antes de substituir
  - Opção de mesclar com existente
- [ ] **Exportar**:
  - Download do Excel atual
  - Download em formato CSV
  - Backup com timestamp
- [ ] **Backups**:
  - Listar backups automáticos
  - Restaurar de backup
  - Limpar backups antigos

### 5. ⚙️ Página: Configurações

**Objetivo**: Configurações e utilitários

**Funcionalidades**:
- [ ] Configurar categorias disponíveis
- [ ] Configurar subcategorias por categoria
- [ ] Gerenciar posições
- [ ] Validações personalizadas
- [ ] Tema claro/escuro
- [ ] Resetar para padrões

---

## 🔒 Estratégia de Isolamento

### Princípios:

1. **Separação Completa**: Todo código Streamlit em pasta `streamlit_app/`
2. **Sem Modificações no Pipeline**: Pipeline existente não é tocado
3. **Arquivo Compartilhado**: `base_peso.xlsx` é o único ponto de contato
4. **Backups Automáticos**: Sempre criar backup antes de salvar

### Workflow:

```
┌──────────────────┐
│ Streamlit App    │
│                  │
│ 1. Carrega       │──┐
│ 2. Edita         │  │
│ 3. Valida        │  │
│ 4. Salva         │  │
└──────────────────┘  │
                      ▼
           ┌──────────────────┐
           │ base_peso.xlsx   │ ◄─── Arquivo compartilhado
           └──────────────────┘
                      │
                      ▼
           ┌──────────────────┐
           │ Pipeline Scouts  │
           │                  │
           │ 1. Load          │
           │ 2. Process       │
           │ 3. Export        │
           └──────────────────┘
```

### Garantias:

- ✅ Pipeline não importa nada de `streamlit_app/`
- ✅ Streamlit não modifica arquivos do pipeline
- ✅ Backups automáticos em `bases/inputs/business/backups/`
- ✅ Validação de estrutura antes de salvar
- ✅ Lock de arquivo (evitar edição simultânea)

---

## 📦 Dependências Adicionais

**requirements_streamlit.txt**:
```
streamlit>=1.29.0
pandas>=2.1.4
openpyxl>=3.1.2
pyyaml>=6.0.1
plotly>=5.18.0          # Para gráficos interativos
streamlit-aggrid>=0.3.4  # Tabela avançada (opcional)
```

---

## 🎨 Design da Interface

### Layout Principal

```
╔════════════════════════════════════════════════════════╗
║  🎯 Scouts Bota - Gerenciador de Pesos                ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                        ║
║  📊 Visualizar  ✏️ Editar  ➕ Adicionar  📥 Import  ⚙️  ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                        ║
║  [Filtros]                          [Busca: ______ ]  ║
║  ┌────────────────────────────────────────────────┐   ║
║  │ Categoria: [Todas ▾]                          │   ║
║  │ Status: [☑ Ativos  ☐ Inativos]                │   ║
║  └────────────────────────────────────────────────┘   ║
║                                                        ║
║  ┌─────────────────────────────────────────────────┐  ║
║  │ INDICADOR          │ CAT │ GK│ CB│ RB│ DM│ ... │  ║
║  ├─────────────────────────────────────────────────┤  ║
║  │ Passes Attempted   │PASS │ 20│ 85│ 70│ 75│ ... │  ║
║  │ Tackles            │DEF  │ 10│ 90│ 85│ 80│ ... │  ║
║  │ ...                │...  │...│...│...│...│ ... │  ║
║  └─────────────────────────────────────────────────┘  ║
║                                                        ║
║  📊 Total: 206 indicadores (109 ativos)               ║
╚════════════════════════════════════════════════════════╝
```

### Editor de Pesos (Visualização Individual)

```
╔════════════════════════════════════════════════════════╗
║  Editar Indicador: "Passes Attempted"                 ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                        ║
║  📋 Informações Básicas                                ║
║  ┌────────────────────────────────────────────────┐   ║
║  │ Categoria: [PASS ▾]                            │   ║
║  │ Subcategoria: [Progressive Passing ▾]          │   ║
║  │ Considerar: ☑ SIM  ☐ NÃO                       │   ║
║  │ Melhor para: ◉ CIMA  ○ BAIXO                   │   ║
║  │ Explicação: [________________________________] │   ║
║  └────────────────────────────────────────────────┘   ║
║                                                        ║
║  ⚖️ Pesos por Posição                                  ║
║  ┌────────────────────────────────────────────────┐   ║
║  │ GK  [████────────] 20                          │   ║
║  │ CB  [████████────] 85                          │   ║
║  │ RCB [████████────] 80                          │   ║
║  │ LCB [████████────] 80                          │   ║
║  │ RB  [███████─────] 70                          │   ║
║  │ LB  [███████─────] 70                          │   ║
║  │ DM  [███████████─] 75                          │   ║
║  │ CM  [████████────] 80                          │   ║
║  │ AM  [███████─────] 70                          │   ║
║  │ LW  [██████──────] 60                          │   ║
║  │ RW  [██████──────] 60                          │   ║
║  │ CF  [█████───────] 50                          │   ║
║  └────────────────────────────────────────────────┘   ║
║                                                        ║
║  [💾 Salvar]  [❌ Cancelar]  [🔄 Resetar]             ║
╚════════════════════════════════════════════════════════╝
```

---

## 🔐 Validações

### 1. Validações de Estrutura

```python
def validate_structure(df):
    """Valida estrutura do DataFrame"""
    required_cols = [
        "INDICADOR", "CLASSIFICACAO RANKING",
        "SUBCLASSIFICACAO RANKING", "CONSIDERAR?",
        "Melhor para", "GK", "CB", "RCB", "LCB",
        "RB", "LB", "DM", "CM", "AM", "LW", "RW", "CF"
    ]

    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Colunas faltantes: {missing}")

    return True
```

### 2. Validações de Dados

```python
def validate_data(df):
    """Valida integridade dos dados"""
    errors = []

    # 1. Indicadores únicos
    duplicates = df[df.duplicated("INDICADOR")]
    if not duplicates.empty:
        errors.append(f"Indicadores duplicados: {duplicates['INDICADOR'].tolist()}")

    # 2. CONSIDERAR? em valores válidos
    invalid_considerar = df[~df["CONSIDERAR?"].isin(["SIM", "NÃO"])]
    if not invalid_considerar.empty:
        errors.append(f"CONSIDERAR? inválido em linhas: {invalid_considerar.index.tolist()}")

    # 3. Melhor para em valores válidos
    invalid_direcao = df[~df["Melhor para"].isin(["CIMA", "BAIXO"])]
    if not invalid_direcao.empty:
        errors.append(f"Direção inválida em linhas: {invalid_direcao.index.tolist()}")

    # 4. Pesos entre 0-100
    position_cols = ["GK", "CB", "RCB", "LCB", "RB", "LB",
                     "DM", "CM", "AM", "LW", "RW", "CF"]
    for col in position_cols:
        invalid_weights = df[(df[col] < 0) | (df[col] > 100)]
        if not invalid_weights.empty:
            errors.append(f"{col} fora do range em linhas: {invalid_weights.index.tolist()}")

    if errors:
        raise ValueError("\n".join(errors))

    return True
```

---

## 📝 Exemplo de Código Estrutural

### app.py (Aplicação Principal)

```python
import streamlit as st
from components.data_loader import DataLoader
from components.data_editor import DataEditor
from utils.constants import POSITIONS, CATEGORIES

# Configuração da página
st.set_page_config(
    page_title="Scouts Bota - Gerenciador de Pesos",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
with open("streamlit_app/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Título
st.title("🎯 Scouts Bota - Gerenciador de Pesos")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")

    # Carregar arquivo
    loader = DataLoader()
    df = loader.load_weights()

    st.metric("Total de Indicadores", len(df))
    st.metric("Indicadores Ativos", len(df[df["CONSIDERAR?"] == "SIM"]))
    st.metric("Indicadores Inativos", len(df[df["CONSIDERAR?"] == "NÃO"]))

# Conteúdo principal
editor = DataEditor(df)
editor.render()
```

### components/data_loader.py

```python
import pandas as pd
import shutil
from pathlib import Path
from datetime import datetime

class DataLoader:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.weights_file = self.base_dir / "bases/inputs/business/base_peso.xlsx"
        self.backup_dir = self.base_dir / "bases/inputs/business/backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def load_weights(self) -> pd.DataFrame:
        """Carrega arquivo de pesos"""
        if not self.weights_file.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.weights_file}")

        return pd.read_excel(self.weights_file)

    def save_weights(self, df: pd.DataFrame, create_backup: bool = True):
        """Salva arquivo de pesos com backup"""
        if create_backup:
            self._create_backup()

        df.to_excel(self.weights_file, index=False)

    def _create_backup(self):
        """Cria backup do arquivo atual"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"base_peso_backup_{timestamp}.xlsx"
        shutil.copy2(self.weights_file, backup_file)
        return backup_file
```

---

## 🚀 Plano de Implementação

### Fase 1: Setup Básico ✅
- [x] Criar branch `feat/streamlit`
- [ ] Criar estrutura de diretórios
- [ ] Configurar `requirements_streamlit.txt`
- [ ] Criar `app.py` básico
- [ ] Testar execução local

### Fase 2: Componente de Carregamento
- [ ] Implementar `data_loader.py`
- [ ] Implementar sistema de backups
- [ ] Testar carregamento de Excel
- [ ] Validar estrutura do arquivo

### Fase 3: Visualização
- [ ] Criar página de visualização
- [ ] Implementar filtros
- [ ] Implementar busca
- [ ] Adicionar estatísticas

### Fase 4: Edição
- [ ] Implementar editor de tabela
- [ ] Adicionar validações em tempo real
- [ ] Implementar salvamento
- [ ] Testar edição de pesos

### Fase 5: Adicionar Indicadores
- [ ] Criar formulário de adição
- [ ] Implementar validações
- [ ] Testar inserção

### Fase 6: Import/Export
- [ ] Implementar upload de Excel
- [ ] Implementar download
- [ ] Implementar restauração de backups

### Fase 7: Polimento
- [ ] Adicionar CSS customizado
- [ ] Melhorar UX
- [ ] Adicionar documentação
- [ ] Testar integração com pipeline

### Fase 8: Documentação e Deploy
- [ ] Criar `README_STREAMLIT.md`
- [ ] Criar `run_streamlit.bat`
- [ ] Documentar uso
- [ ] Testar em ambiente limpo

---

## 🧪 Testes de Integração

### Cenários de Teste:

1. **Editar pesos → Executar pipeline → Verificar outputs**
   - Editar peso de um indicador
   - Salvar no Streamlit
   - Executar `ProcessarScouts.bat`
   - Verificar se `consolidated_overall.parquet` reflete mudança

2. **Adicionar indicador → Validar no pipeline**
   - Adicionar novo indicador
   - Marcar como "SIM"
   - Executar pipeline
   - Verificar se indicador é processado

3. **Desativar indicador → Verificar exclusão**
   - Mudar CONSIDERAR? para "NÃO"
   - Executar pipeline
   - Verificar que indicador não aparece em outputs

4. **Restaurar backup → Verificar integridade**
   - Fazer mudanças
   - Restaurar backup antigo
   - Executar pipeline
   - Verificar consistência

---

## 📚 Documentação Necessária

### README_STREAMLIT.md
- Como instalar dependências
- Como executar aplicação
- Guia de uso básico
- Troubleshooting

### Tutorial em Vídeo (Opcional)
- Demonstração das funcionalidades
- Workflow típico de uso

---

## 🎯 Critérios de Sucesso

- [ ] Interface carrega sem erros
- [ ] Consegue visualizar todos os 206 indicadores
- [ ] Consegue editar pesos e salvar
- [ ] Backups são criados automaticamente
- [ ] Pipeline processa arquivo editado sem erros
- [ ] Validações impedem dados inválidos
- [ ] Usuário consegue adicionar novos indicadores
- [ ] Usuário consegue fazer import/export
- [ ] Documentação está clara e completa
- [ ] Código está isolado e não afeta pipeline

---

## 🔄 Próximos Passos

1. **Revisar este plano** com stakeholders
2. **Aprovar arquitetura** proposta
3. **Iniciar Fase 1**: Setup básico
4. **Iteração incremental**: Uma fase por vez

---

**Status**: 📝 Em planejamento
**Data**: 2026-01-12
**Autor**: Claude (Sonnet 4.5)
