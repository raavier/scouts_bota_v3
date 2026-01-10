# Scripts de Verificação

Esta pasta contém scripts utilitários para verificar e diagnosticar a qualidade dos dados processados.

## Scripts Disponíveis

### 1. `check_none_none.py`
**Propósito**: Verifica se há registros com `player_name = "None None"` no arquivo consolidado.

**Como usar**:
```bash
python scripts/checks/check_none_none.py
```

**O que verifica**:
- Total de registros com "None None"
- Registros com player_name nulo
- Exemplo específico: jogador 410697 (competition_id=12)

---

### 2. `check_player.py`
**Propósito**: Investiga um jogador específico (ID: 410697) nos dados de origem (Excel).

**Como usar**:
```bash
python scripts/checks/check_player.py
```

**O que mostra**:
- Colunas disponíveis no Excel
- Valores de player_name, first_name, last_name, known_name
- Outras informações do jogador (time, posição, competição)

---

### 3. `check_unmapped_positions.py`
**Propósito**: Identifica jogadores sem posição mapeada (mapped_position = None).

**Como usar**:
```bash
python scripts/checks/check_unmapped_positions.py
```

**O que mostra**:
- Total de jogadores sem posição mapeada
- Distribuição de primary_position dos jogadores sem mapeamento
- Exemplos detalhados com informações completas
- Comparação entre dados brutos e após processamento

---

### 4. `check_zeros.py`
**Propósito**: Analisa jogadores com overall_score zerado ou nulo.

**Como usar**:
```bash
python scripts/checks/check_zeros.py
```

**O que mostra**:
- Jogadores com overall_score = 0 ou NaN
- Distribuição por posição e competição
- Diagnóstico de indicadores normalizados

---

### 5. `check_minutes.py`
**Propósito**: Analisa a minutagem dos jogadores sem posição mapeada.

**Como usar**:
```bash
python scripts/checks/check_minutes.py
```

**O que mostra**:
- Estatísticas de minutagem (média, mediana, min, max)
- Distribuição por faixas de minutos
- Comparação com jogadores que têm posição mapeada
- Conclusão sobre a relação entre minutagem e posição

---

### 6. `verify_fix.py`
**Propósito**: Verifica se a correção "Sem posição definida" foi aplicada corretamente.

**Como usar**:
```bash
python scripts/checks/verify_fix.py
```

**O que mostra**:
- Jogadores específicos com a correção aplicada
- Estatísticas gerais da correção
- Confirmação de sucesso da implementação

---

## Notas

- Todos os scripts usam encoding UTF-8 para suportar caracteres especiais
- Os scripts leem dados de `bases/outputs/consolidated_overral.parquet` e arquivos intermediários
- Execute os scripts a partir do diretório raiz do projeto (`c:\jobs\botafogo\v3`)

## Problemas Resolvidos

1. **"None None" em player_name** (check_none_none.py)
   - Causa: Concatenação de first_name + last_name quando ambos eram None
   - Solução: Lógica de prioridade no notebook 03

2. **Valores zerados/NaN** (check_zeros.py, check_unmapped_positions.py)
   - Causa: 107 jogadores sem primary_position nos dados de origem
   - Solução: Preencher com "Sem posição definida" no notebook 02

3. **Baixa minutagem** (check_minutes.py)
   - Observação: Jogadores sem posição têm menos de 30 minutos na temporada
   - Decisão: Manter na base mas sem overall_score
