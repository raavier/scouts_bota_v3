# Contexto de Execucao - Pipeline de Scouts

## Resumo do que foi feito

Implementacao completa da pipeline de processamento de dados de scouts conforme definido em `PLANO.md`.

## Estrutura Criada

```
v3/
├── .claude/
│   ├── PLANO.md              # Plano original
│   └── CONTEXTO_EXECUCAO.md  # Este arquivo
├── config/
│   ├── config.yaml           # Caminhos dos arquivos
│   └── positions.yaml        # Mapeamento de posicoes (22 posicoes -> 12 padrao)
├── bases/
│   ├── inputs/
│   │   ├── business/
│   │   │   └── base_peso.xlsx    # Tabela de pesos (109 indicadores ativos x 12 posicoes)
│   │   └── scouts_base/
│   │       ├── argentina_2025.xlsx  (1002 jogadores)
│   │       ├── belgium_1.xlsx       (501 jogadores)
│   │       ├── europe_3.xlsx        (1066 jogadores)
│   │       ├── france_1.xlsx        (553 jogadores)
│   │       ├── germany_1.xlsx       (492 jogadores)
│   │       └── italy_1.xlsx         (634 jogadores)
│   └── outputs/
│       ├── consolidated_overral.parquet     # 4248 linhas, 19 colunas
│       ├── consolidated_weights.parquet     # 109 indicadores
│       ├── consolidated_context.parquet     # 4248 linhas, 219 colunas
│       └── consolidated_normalized.parquet  # 4248 linhas, 114 colunas
└── code/
    ├── 00_exploratory_analysis.ipynb  # Analise exploratoria dos parquets
    ├── 01_load_data.ipynb
    ├── 02_prepare_positions.ipynb
    ├── 03_consolidate_players.ipynb
    ├── 04_normalize_indicators.ipynb
    ├── 05_calculate_overall.ipynb
    └── 06_export.ipynb
```

## Pipeline Executada com Sucesso

A pipeline foi executada e os parquets foram gerados em 10/Jan/2026.

### Estatisticas da Execucao

| Metrica | Valor |
|---------|-------|
| Total de registros | 4.248 |
| Jogadores unicos (v_current=True) | 4.103 |
| Registros historicos (v_current=False) | 145 |
| Indicadores normalizados | 109 |
| Posicoes mapeadas | 12 |
| Competicoes | 6 |

### Distribuicao por Posicao

| Posicao | Jogadores |
|---------|-----------|
| DM | 620 |
| CF | 579 |
| AM | 390 |
| LB | 373 |
| RB | 363 |
| RCB | 344 |
| LCB | 323 |
| GK | 291 |
| LW | 278 |
| CM | 259 |
| RW | 239 |
| CB | 82 |
| None | 107 |

## Notebooks Criados

### 00_exploratory_analysis.ipynb (NOVO)
- Analise exploratoria dos parquets gerados
- Funcoes para buscar jogador por ID ou nome
- Rankings e top jogadores por posicao
- Comparacao entre jogadores
- Filtros customizados

### 01_load_data.ipynb
- Carrega `config.yaml` e `positions.yaml`
- Carrega os 6 arquivos de scouts e concatena
- Carrega tabela de pesos (`base_peso.xlsx`)
- Filtra indicadores com `CONSIDERAR? = SIM`
- **Output**: `_temp_scouts_raw.parquet`, `_temp_weights_active.parquet`

### 02_prepare_positions.ipynb
- Aplica mapeamento de `primary_position` para posicao padronizada
- Cria 3 colunas: `mapped_position`, `position_group`, `position_sub_group`
- **Output**: `_temp_scouts_positions.parquet`

### 03_consolidate_players.ipynb
- Cria chave unica: `player_id + competition_id`
- **NAO remove duplicatas** - mantem TODOS os registros
- Cria coluna `v_current` (True para registro mais recente por unique_key)
- Cria colunas auxiliares: `player_name`, `competition_name`, `team_name`
- **Output**: `_temp_scouts_consolidated.parquet`

### 04_normalize_indicators.ipynb
- Normaliza valores para 0-100
- Considera direcao: `Melhor para = CIMA` (maior=100) ou `BAIXO` (menor=100)
- Cria colunas `{indicador}_norm` para cada indicador
- **Output**: `_temp_scouts_normalized.parquet`, `_temp_weights_map.json`, `_temp_indicators_available.json`

### 05_calculate_overall.ipynb
- Calcula `overall_score` ponderado pela posicao do jogador
- Calcula scores por categoria (`score_{categoria}`)
- Categorias: DGP, PASS, OFFENSIVE, DEFENSIVE, GERAL, GK
- Gera rankings: `rank_overall` e `rank_position`
- **Output**: `_temp_scouts_scored.parquet`

### 06_export.ipynb
- Exporta arquivos finais para `bases/outputs/`
- Opcao para limpar arquivos temporarios

## Posicoes Padronizadas (12)

| Codigo | Descricao |
|--------|-----------|
| GK | Goleiro |
| CB | Zagueiro Central |
| RCB | Zagueiro - Direita |
| LCB | Zagueiro - Esquerda |
| RB | Lateral Direito |
| LB | Lateral Esquerdo |
| DM | Volante |
| CM | Meio-campista Central |
| AM | Meia Atacante |
| RW | Extremo Direita |
| LW | Extremo Esquerda |
| CF | Centroavante |

## Estrutura dos Parquets

### consolidated_overral.parquet (Principal)

| Coluna | Descricao |
|--------|-----------|
| player_id | ID do jogador |
| competition_id | ID da competicao |
| player_name | Nome do jogador |
| competition_name | Nome da competicao |
| team_name | Time |
| primary_position | Posicao original |
| mapped_position | Posicao mapeada (12 opcoes) |
| position_group | Grupo da posicao |
| position_sub_group | Subgrupo (Centro, Direita, Esquerda) |
| v_current | True = registro atual, False = historico |
| overall_score | Score geral ponderado |
| rank_overall | Ranking geral |
| rank_position | Ranking dentro da posicao |
| score_dgp | Score categoria DGP |
| score_pass | Score categoria PASS |
| score_offensive | Score categoria OFFENSIVE |
| score_defensive | Score categoria DEFENSIVE |
| score_geral | Score categoria GERAL |
| score_gk | Score categoria GK |

### consolidated_context.parquet
- Metadados completos dos jogadores (219 colunas)
- Inclui: minutos jogados, datas, times, etc.

### consolidated_normalized.parquet
- Valores normalizados (0-100) de cada indicador
- 109 colunas `{indicador}_norm`

### consolidated_weights.parquet
- Tabela de pesos utilizada
- 109 indicadores com pesos por posicao

## Exemplo de Uso

### Carregar dados
```python
import pandas as pd
df = pd.read_parquet('bases/outputs/consolidated_overral.parquet')
```

### Filtrar apenas registros atuais
```python
df_atual = df[df['v_current'] == True]
```

### Buscar jogador por ID
```python
jogador = df[df['player_id'] == 25079]
```

### Top 10 por posicao
```python
top_cf = df[df['mapped_position'] == 'CF'].nsmallest(10, 'rank_position')
```

## Exemplo: Jogador 25079 (Artem Dovbyk)

| Campo | Serie A | Europa League |
|-------|---------|---------------|
| unique_key | 25079_12 | 25079_35 |
| v_current | True | True |
| overall_score | 26.63 | 26.43 |
| rank_overall | 800 | 885 |
| rank_position (CF) | 291 | 327 |
| minutos | 2550 | 679 |

## Dependencias Python

```python
pandas
pyyaml
pyarrow
openpyxl
```

## Decisoes de Implementacao

1. **Chave unica**: `player_id + competition_id`
2. **Historico**: Mantem TODOS os registros, `v_current = True` marca o mais recente
3. **Normalizacao**: Min-Max scaling para 0-100, respeitando direcao (CIMA/BAIXO)
4. **Score ponderado**: Media ponderada dos indicadores normalizados usando pesos da posicao
5. **Rankings**: `rank_overall` (global) e `rank_position` (dentro da posicao)

## Arquivos Temporarios

Os notebooks geram arquivos `_temp_*` em `bases/outputs/`:
- `_temp_scouts_raw.parquet`
- `_temp_weights_active.parquet`
- `_temp_scouts_positions.parquet`
- `_temp_scouts_consolidated.parquet`
- `_temp_scouts_normalized.parquet`
- `_temp_scouts_scored.parquet`
- `_temp_weights_map.json`
- `_temp_indicators_available.json`

Podem ser removidos apos execucao completa.

## Coluna v_current

A coluna `v_current` identifica o registro mais recente por `unique_key` (player_id + competition_id):
- `v_current = True`: Registro atual
- `v_current = False`: Registro historico

Um jogador pode ter `v_current = True` em multiplas competicoes (ex: Dovbyk tem True na Serie A e True na Europa League, pois sao competicoes diferentes).
