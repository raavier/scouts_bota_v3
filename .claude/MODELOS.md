# Configuração de Modelos

## Modelo Atual
Por padrão, o projeto usa **Sonnet 4.5** para um bom equilíbrio entre velocidade e capacidade.

## Como trocar para Opus 4.5
Para usar o modelo mais poderoso (Opus 4.5) em tarefas complexas de planejamento:

1. Abra o arquivo `.claude/settings.local.json`
2. Troque a linha `"model": "sonnet"` por `"model": "opus"`
3. Salve o arquivo

## Modelos disponíveis
- `sonnet` - Sonnet 4.5 (rápido e eficiente)
- `opus` - Opus 4.5 (mais poderoso para tarefas complexas)
- `haiku` - Haiku (mais rápido para tarefas simples)
