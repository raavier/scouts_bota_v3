# Plano: Consolidação de Base de Scouts

## Objetivo
Criar uma pipeline de processamento de dados de scouts de futebol que:
1. Consolide dados de diferentes ligas/arquivos Excel
2. Aplique pesos por posição para calcular scores overall
3. Gere outputs consolidados em formato parquet

## Estrutura Atual do Projeto

### Inputs
- **`bases/inputs/business/base_peso.xlsx`**: Tabela de pesos (206 indicadores x 12 posições)
  - Colunas: INDICADOR, CLASSIFICACAO RANKING, SUBCLASSIFICACAO RANKING, CONSIDERAR?, ESPECIAL?, Melhor para, tipo_agreg, GK, RCB, LCB, CB, RB, LB, DM, CM, AM, LW, RW, CF, Explicação indicador
  - Filtrar por `CONSIDERAR? = SIM`
  - `Melhor para`: CIMA (maior é melhor) ou BAIXO (menor é melhor)

- **`bases/inputs/scouts_base/*.xlsx`**: 6 arquivos de scouts
  - argentina_2025.xlsx (1002 jogadores - Liga Profesional)
  - belgium_1.xlsx (501 jogadores - Challenger Pro League)
  - europe_3.xlsx (1066 jogadores - UEFA Europa League)
  - france_1.xlsx (553 jogadores - Ligue 1)
  - germany_1.xlsx (492 jogadores - 1. Bundesliga)
  - italy_1.xlsx (634 jogadores - Serie A)
  - Cada arquivo tem 224 colunas com métricas de jogadores

### Configurações
- **`config/positions.yaml`**: Mapeamento de posições detalhadas → posições padrão
  - Estrutura expandida com: `position`, `position_group`, `position_sub_group`
  - 12 posições: GK, CB, RCB, LCB, RB, LB, DM, CM, AM, LW, RW, CF
  - `position_group`: categoria em português (ex: "Zagueiro - Direita")
  - `position_sub_group`: lateralidade (Centro, Direita, Esquerda)
- **`config/config.yaml`**: Caminhos dos arquivos + filtro de minutos (desabilitado por padrão)

### Outputs Esperados
- `bases/outputs/consolidated_overral.parquet`: Tabela final com scores overall
- `bases/outputs/consolidated_weights.parquet`: Pesos utilizados
- `bases/outputs/consolidated_context.parquet`: Contexto/metadados
- `bases/outputs/consolidated_normalized.parquet`: Dados normalizados

## Plano de Implementação

### Etapa 1: Setup e Carregamento de Dados
**Notebook**: `code/01_load_data.ipynb`
- Carregar configurações YAML
- Carregar todos os arquivos de scouts e concatenar
- Carregar tabela de pesos
- Validar estrutura dos dados

### Etapa 2: Preparação e Mapeamento de Posições
**Notebook**: `code/02_prepare_positions.ipynb`
- Aplicar mapeamento de posições (primary_position → posição padrão)
- Extrair `position`, `position_group`, `position_sub_group` do mapeamento
- Tratar posições secundárias
- Validar que todas as posições foram mapeadas para uma das 12 posições padrão

### Etapa 3: Consolidação de Jogadores Únicos
**Notebook**: `code/03_consolidate_players.ipynb`
- Criar chave única: `player_id + competition_id`
- Para duplicatas: manter o registro mais recente (`player_season_most_recent_match`)
- Gerar colunas auxiliares: `player_name`, `competition_name` (para visualização)

### Etapa 4: Normalização de Indicadores
**Notebook**: `code/04_normalize_indicators.ipynb`
- Filtrar indicadores com `CONSIDERAR? = SIM`
- Normalizar valores (0-100) considerando:
  - `Melhor para = CIMA`: maior valor = 100
  - `Melhor para = BAIXO`: menor valor = 100
- Agrupar por `tipo_agreg` se necessário

### Etapa 5: Cálculo de Scores Overall
**Notebook**: `code/05_calculate_overall.ipynb`
- Para cada jogador, aplicar pesos da posição correspondente
- Calcular score ponderado por:
  - Posição (GK, CB, RCB, LCB, RB, LB, DM, CM, AM, LW, RW, CF)
  - Categoria (CLASSIFICACAO RANKING)
  - Subcategoria (SUBCLASSIFICACAO RANKING)
- Gerar rankings

### Etapa 6: Exportação Final
**Notebook**: `code/06_export.ipynb`
- Exportar para parquet:
  - consolidated_overral.parquet
  - consolidated_weights.parquet
  - consolidated_context.parquet
  - consolidated_normalized.parquet

## Estrutura de Saída (consolidated_overral)

| Coluna | Descrição |
|--------|-----------|
| player_id | ID do jogador |
| competition_id | ID da competição |
| player_name | Nome do jogador |
| competition_name | Nome da competição |
| team_name | Time |
| primary_position | Posição original |
| mapped_position | Posição mapeada (GK, CB, RCB, LCB, RB, LB, DM, CM, AM, LW, RW, CF) |
| position_group | Grupo da posição (ex: "Zagueiro - Direita") |
| position_sub_group | Subgrupo de lateralidade (Centro, Direita, Esquerda) |
| overall_score | Score geral ponderado |
| score_[CATEGORIA] | Score por categoria |
| rank_overall | Ranking geral |
| rank_position | Ranking na posição |

## Próximos Passos

1. Criar pasta `code/` para notebooks
2. Implementar cada etapa em notebook separado
3. Testar cada etapa antes de avançar
4. Criar script final consolidado após validação

## Decisões Tomadas

1. **Duplicatas**: Manter registros separados por competição (chave: `player_id + competition_id`)
2. **Filtro de minutos**: Configurável via `config.yaml` (desabilitado por padrão)
3. **Indicadores ESPECIAL?**: Ignorar por enquanto, tratar igual aos demais
4. **Posição para pesos**: Usar `primary_position` mapeada
5. **Granularidade de posições**: Expandido de 9 para 12 posições para maior precisão (CB→CB/RCB/LCB, W→RW/LW)
6. **Lateralidade**: Adicionado `position_sub_group` para distinguir jogadores que atuam mais à direita/esquerda/centro
