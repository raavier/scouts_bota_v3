# Scouts Bota v2 - Pipeline de Análise de Jogadores

Sistema de consolidação e análise de dados de scouts de futebol, aplicando pesos por posição para calcular scores overall de jogadores.

## 📋 Visão Geral

Este projeto processa dados de scouts de múltiplas ligas/competições, aplica normalização de indicadores e calcula scores ponderados por posição para gerar rankings de jogadores.

**Versão**: 4.0
**Posições suportadas**: 12 (GK, CB, RCB, LCB, RB, LB, DM, CM, AM, LW, RW, CF)
**Ligas incluídas**: Argentina, Bélgica, França, Alemanha, Itália, Europa League

## 🚀 Quick Start

### Pré-requisitos
```bash
pip install pandas openpyxl pyyaml pyarrow
```

### Executar Pipeline Completa
```bash
python run_pipeline.py
```

Este comando:
1. Carrega dados de 6 arquivos Excel
2. Mapeia posições para 12 categorias padrão
3. Consolida jogadores únicos
4. Normaliza 109 indicadores
5. Calcula scores overall ponderados
6. Exporta 4 arquivos parquet consolidados

## 📁 Estrutura do Projeto

```
v3/
├── bases/
│   ├── inputs/
│   │   ├── business/
│   │   │   └── base_peso.xlsx              # Tabela de pesos (206 indicadores x 12 posições)
│   │   └── scouts_base/
│   │       ├── argentina_2025.xlsx         # 1002 jogadores - Liga Profesional
│   │       ├── belgium_1.xlsx              # 501 jogadores - Challenger Pro League
│   │       ├── europe_3.xlsx               # 1066 jogadores - UEFA Europa League
│   │       ├── france_1.xlsx               # 553 jogadores - Ligue 1
│   │       ├── germany_1.xlsx              # 492 jogadores - 1. Bundesliga
│   │       └── italy_1.xlsx                # 634 jogadores - Serie A
│   └── outputs/
│       ├── consolidated_overral.parquet    # Tabela final com scores
│       ├── consolidated_weights.parquet    # Pesos utilizados
│       ├── consolidated_context.parquet    # Metadados
│       ├── consolidated_normalized.parquet # Dados normalizados
│       └── _temp_*.parquet                 # Arquivos intermediários
│
├── code/
│   ├── 01_load_data.ipynb                  # Carregamento de dados
│   ├── 02_prepare_positions.ipynb          # Mapeamento de posições
│   ├── 03_consolidate_players.ipynb        # Consolidação de jogadores
│   ├── 04_normalize_indicators.ipynb       # Normalização de indicadores
│   ├── 05_calculate_overall.ipynb          # Cálculo de scores
│   └── 06_export.ipynb                     # Exportação final
│
├── config/
│   ├── config.yaml                         # Configurações gerais
│   └── positions.yaml                      # Mapeamento de posições
│
├── scripts/
│   └── checks/                             # Scripts de verificação
│       ├── check_none_none.py
│       ├── check_player.py
│       ├── check_unmapped_positions.py
│       ├── check_zeros.py
│       ├── check_minutes.py
│       └── verify_fix.py
│
├── run_pipeline.py                         # Script principal de execução
└── README.md                               # Este arquivo
```

## 📊 Pipeline de Processamento

### Etapa 1: Carregamento (01_load_data.ipynb)
- Carrega 6 arquivos Excel de scouts (total: 4248 jogadores)
- Carrega tabela de pesos (206 indicadores, 109 ativos)
- Valida estrutura dos dados
- Exporta: `_temp_scouts_raw.parquet`, `_temp_weights_active.parquet`

### Etapa 2: Preparação de Posições (02_prepare_positions.ipynb)
- Mapeia 23 posições originais → 12 posições padrão
- Extrai `position_group` e `position_sub_group`
- Marca jogadores sem posição como "Sem posição definida"
- Exporta: `_temp_scouts_positions.parquet`

### Etapa 3: Consolidação (03_consolidate_players.ipynb)
- Cria chave única: `player_id + competition_id`
- Marca registro mais recente como `v_current = True`
- Gera colunas auxiliares com lógica de prioridade para `player_name`:
  1. `player_known_name`
  2. `player_name` (do Excel)
  3. `first_name + last_name` (somente se ambos existirem)
  4. `first_name` (somente)
  5. `last_name` (somente)
- Exporta: `_temp_scouts_consolidated.parquet`

### Etapa 4: Normalização (04_normalize_indicators.ipynb)
- Normaliza 109 indicadores para escala 0-100
- Considera direção (`CIMA` = maior melhor, `BAIXO` = menor melhor)
- Exporta: `_temp_scouts_normalized.parquet`

### Etapa 5: Cálculo de Overall (05_calculate_overall.ipynb)
- Aplica pesos específicos por posição
- Calcula scores por categoria (PASS, DEFENSIVE, DGP, OFFENSIVE, GK)
- Gera `overall_score` ponderado
- Cria rankings geral e por posição
- Exporta: `_temp_scouts_scored.parquet`

### Etapa 6: Exportação (06_export.ipynb)
- Gera 4 arquivos parquet finais
- Valida integridade dos dados
- Gera estatísticas finais

## 🔧 Configuração

### config.yaml
```yaml
app:
  name: "Scouts Bota v2"
  version: "4.0"

paths:
  scouts_dir: "bases/inputs/scouts_base"
  weights_file: "bases/inputs/business/base_peso.xlsx"
  output_dir: "bases/outputs"

filters:
  min_minutes: 0  # Filtro de minutos (0 = desabilitado)
```

### positions.yaml
Define o mapeamento de 23 posições originais para 12 posições padrão, com grupos e subgrupos de lateralidade.

## 📈 Outputs

### consolidated_overral.parquet
Tabela principal com scores de jogadores.

**Colunas principais**:
- `player_id`, `competition_id` - Identificadores
- `player_name`, `team_name`, `competition_name` - Informações básicas
- `primary_position` - Posição original
- `mapped_position` - Posição mapeada (GK, CB, RCB, LCB, RB, LB, DM, CM, AM, LW, RW, CF)
- `position_group` - Grupo da posição (ex: "Zagueiro - Direita")
- `position_sub_group` - Lateralidade (Centro, Direita, Esquerda)
- `overall_score` - Score geral ponderado
- `score_PASS`, `score_DEFENSIVE`, `score_DGP`, `score_OFFENSIVE`, `score_GK` - Scores por categoria
- `rank_overall` - Ranking geral
- `rank_position` - Ranking na posição

**Total de registros**: 4248 jogadores
**Jogadores com score válido**: 4141 (97.5%)
**Jogadores sem posição**: 107 (2.5% - baixa minutagem)

### consolidated_weights.parquet
Tabela de pesos utilizados no cálculo.

### consolidated_context.parquet
Metadados e contexto do processamento.

### consolidated_normalized.parquet
Valores normalizados dos indicadores (0-100).

## 🧪 Scripts de Verificação

A pasta `scripts/checks/` contém scripts para diagnosticar problemas:

```bash
# Verificar nomes "None None"
python scripts/checks/check_none_none.py

# Verificar jogadores sem posição
python scripts/checks/check_unmapped_positions.py

# Verificar scores zerados
python scripts/checks/check_zeros.py

# Verificar minutagem
python scripts/checks/check_minutes.py

# Verificar correção aplicada
python scripts/checks/verify_fix.py
```

Consulte [scripts/checks/README.md](scripts/checks/README.md) para detalhes.

## 🐛 Problemas Conhecidos e Soluções

### 1. Player Name "None None" ✅ RESOLVIDO
**Problema**: 1914 jogadores com `player_name = "None None"`
**Causa**: Concatenação de `first_name + last_name` quando ambos eram None
**Solução**: Implementada lógica de prioridade no notebook 03

### 2. Overall Score NaN ✅ RESOLVIDO
**Problema**: 107 jogadores com `overall_score = NaN`
**Causa**: Jogadores sem `primary_position` nos dados de origem (baixa minutagem: 1-26 min)
**Solução**: `primary_position` preenchido com "Sem posição definida" no notebook 02

## 📝 Notas Técnicas

- **Duplicatas**: Mantém registros separados por competição (chave: `player_id + competition_id`)
- **Filtro de minutos**: Configurável via `config.yaml` (desabilitado por padrão)
- **Indicadores ESPECIAL**: Tratados igual aos demais
- **Posição para pesos**: Usa `primary_position` mapeada
- **Encoding**: Todos os scripts usam UTF-8

## 🔄 Reprocessamento

Para reprocessar toda a pipeline após mudanças:

```bash
python run_pipeline.py
```

O script executa automaticamente os 6 notebooks em sequência e gera relatório de sucesso/erro.

## 📚 Documentação Adicional

- [Plano Detalhado](.claude/PLANO.md) - Decisões técnicas e estrutura
- [Contexto de Execução](.claude/CONTEXTO_EXECUCAO.md) - Informações do ambiente
- [Modelos](.claude/MODELOS.md) - Definições de dados

## 🤝 Contribuindo

1. Execute os scripts de verificação antes de commitar
2. Documente mudanças significativas
3. Atualize READMEs quando necessário
4. Mantenha compatibilidade com dados existentes

## 📧 Suporte

Para dúvidas ou problemas, consulte os scripts de diagnóstico em `scripts/checks/`.
