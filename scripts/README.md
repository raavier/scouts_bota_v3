# Scripts Utilitários

Esta pasta contém scripts auxiliares para processamento e verificação de dados.

## Estrutura

```
scripts/
├── checks/          # Scripts de verificação e diagnóstico
│   ├── README.md
│   ├── check_none_none.py
│   ├── check_player.py
│   ├── check_unmapped_positions.py
│   ├── check_zeros.py
│   ├── check_minutes.py
│   └── verify_fix.py
└── README.md        # Este arquivo
```

## Pastas

### `checks/`
Scripts para verificar a qualidade dos dados processados e diagnosticar problemas.

Consulte [checks/README.md](checks/README.md) para documentação detalhada de cada script.

## Scripts de Execução de Notebooks

### `run_notebooks.py`
Script modular e flexível para executar notebooks da pipeline.

**Como usar**:
```bash
# Executar todos os notebooks
python scripts/run_notebooks.py --all

# Executar notebooks específicos
python scripts/run_notebooks.py --notebooks 01 02 03

# Executar a partir do notebook 03
python scripts/run_notebooks.py --from 03

# Executar até o notebook 04
python scripts/run_notebooks.py --to 04

# Executar range (02 a 05)
python scripts/run_notebooks.py --from 02 --to 05

# Executar sem output detalhado
python scripts/run_notebooks.py --all --quiet

# Continuar mesmo se houver erro
python scripts/run_notebooks.py --all --continue-on-error
```

**Recursos**:
- Execução modular (escolha quais notebooks executar)
- Opção de output verboso ou silencioso
- Continuar em caso de erro (opcional)
- Melhor controle sobre a pipeline
- Sem dependências externas (não precisa de nbconvert)

## Como Adicionar Novos Scripts

1. **Scripts de verificação**: Adicione em `scripts/checks/`
2. **Scripts de processamento**: Adicione no diretório raiz ou crie nova pasta específica
3. **Documente**: Sempre atualize os READMEs correspondentes

## Convenções

- Use encoding UTF-8 em todos os scripts
- Adicione tratamento de erros apropriado
- Inclua mensagens de progresso claras
- Configure `sys.stdout` para UTF-8 quando necessário:
  ```python
  import sys
  import io
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
  ```
