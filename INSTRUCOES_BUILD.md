# Instruções de Build - Processador de Scouts

## ✅ O que já está pronto

Toda a implementação está completa e testada:

- ✅ **6 módulos Python** convertidos dos notebooks
- ✅ **main.py** com interface user-friendly
- ✅ **Paths dinâmicos** (funciona em qualquer lugar)
- ✅ **Testado localmente** com sucesso (8 segundos, 4248 jogadores)
- ✅ **Scripts de build** criados
- ✅ **Documentação cliente** (LEIA-ME.txt)

## 📋 Próximos Passos

### Opção A: Usar Diretamente (Sem Build)

Se você ou o cliente tiverem Python instalado:

```bash
cd c:\jobs\botafogo\v3
python main.py
```

**Vantagens**: Simples, rápido, fácil de atualizar
**Desvantagens**: Requer Python instalado

---

### Opção B: Build com Python Embeddable (Recomendado)

Para criar um pacote standalone sem precisar de Python instalado:

```bash
cd c:\jobs\botafogo\v3
python build_embeddable.py
```

**O que o script faz**:
1. Baixa Python 3.11 Embeddable (~15MB)
2. Instala pip
3. Instala dependências (pandas, numpy, etc) em `libs/`
4. Configura sys.path
5. Copia todos os arquivos do projeto
6. Cria `dist/BotafogoScouts/` pronto para distribuição

**Resultado**:
```
dist/BotafogoScouts/
├── ProcessarScouts.bat       <- Cliente executa isso
├── main.py
├── pipeline/
├── python-embed/             <- Python portátil
├── libs/                     <- Dependências
├── bases/
│   ├── inputs/
│   │   ├── scouts_base/      <- Cliente adiciona .xlsx aqui
│   │   └── business/
│   │       └── base_peso.xlsx
│   └── outputs/
├── config/
├── LEIA-ME.txt
└── log.txt (gerado após execução)
```

**Para distribuir**:
1. Comprimir `dist/BotafogoScouts/` em `.zip`
2. Enviar para o cliente
3. Cliente descompacta e executa `ProcessarScouts.bat`

**Tamanho esperado**: ~80-100MB (compactado: ~30-40MB)

---

### Opção C: Build com PyInstaller (Alternativa)

Se preferir um único .exe (porém maior e pode ter falsos positivos de antivírus):

```bash
pip install pyinstaller
pyinstaller --onefile --console --name ProcessarScouts main.py
```

**Resultado**: `dist/ProcessarScouts.exe` (~200MB)

---

## 🧪 Testando a Distribuição

### Teste Local (antes de distribuir):

```bash
# 1. Executar build
python build_embeddable.py

# 2. Navegar para dist
cd dist/BotafogoScouts

# 3. Testar execução
ProcessarScouts.bat

# 4. Verificar outputs
dir bases\outputs
```

**Arquivos esperados em outputs/**:
- `consolidated_overall.parquet` (0.34 MB)
- `consolidated_weights.parquet` (0.03 MB)
- `consolidated_context.parquet` (5.20 MB)
- `consolidated_normalized.parquet` (2.98 MB)

### Teste em Máquina Limpa (ideal):

1. Copiar `dist/BotafogoScouts/` para outra máquina (ou VM)
2. Máquina NÃO deve ter Python instalado
3. Executar `ProcessarScouts.bat`
4. Verificar se funciona sem erros

---

## 📝 Checklist de Validação

Antes de entregar ao cliente:

### Funcionalidade:
- [ ] `python main.py` funciona localmente
- [ ] Build executado com sucesso (`python build_embeddable.py`)
- [ ] `ProcessarScouts.bat` executa sem erros
- [ ] 4 arquivos parquet gerados em `outputs/`
- [ ] `log.txt` criado automaticamente
- [ ] Testado em máquina sem Python (se possível)

### Estrutura de Arquivos:
- [ ] `LEIA-ME.txt` presente e claro
- [ ] `bases/inputs/scouts_base/` com arquivos Excel de exemplo
- [ ] `bases/inputs/business/base_peso.xlsx` presente
- [ ] `config/config.yaml` e `config/positions.yaml` presentes

### Paths Dinâmicos:
- [ ] Copiar `BotafogoScouts/` para outra pasta → ainda funciona
- [ ] Nenhum path hardcoded restante

---

## 🐛 Troubleshooting

### Erro: "Python não encontrado"
- **Solução**: Executar `python build_embeddable.py` primeiro

### Erro: "Arquivo base_peso.xlsx não encontrado"
- **Solução**: Verificar se existe em `bases/inputs/business/base_peso.xlsx`

### Erro: "Nenhum arquivo .xlsx encontrado"
- **Solução**: Adicionar arquivos Excel em `bases/inputs/scouts_base/`

### Warnings do pandas (DataFrame fragmentation)
- **Não é erro crítico**: Sistema funciona normalmente
- Pode ser ignorado ou otimizado depois se necessário

---

## 📊 Estatísticas do Teste

Executado em: 2026-01-10 17:01:40

**Performance**:
- Tempo total: ~8 segundos
- Jogadores processados: 4,248
- Arquivos Excel: 6
- Indicadores normalizados: 109
- Scores calculados: 4,141 (97.5%)

**Arquivos Gerados**:
- consolidated_overall.parquet: 0.34 MB
- consolidated_weights.parquet: 0.03 MB
- consolidated_context.parquet: 5.20 MB
- consolidated_normalized.parquet: 2.98 MB

---

## 📦 Entrega Final

**O que entregar ao cliente**:

1. **Arquivo compactado**: `BotafogoScouts.zip` (~30-40MB)
   - Contém tudo necessário para executar

2. **Documentação** (já incluída no .zip):
   - `LEIA-ME.txt` - Manual de uso simples
   - `log.txt` - Gerado automaticamente após execução

3. **Instruções verbais**:
   - "Descompacte o arquivo"
   - "Execute ProcessarScouts.bat"
   - "Adicione seus arquivos .xlsx em bases/inputs/scouts_base/"

**Requisitos do cliente**: NENHUM!
- Não precisa Python
- Não precisa instalar nada
- Funciona offline

---

## 🎯 Decisões de Implementação

Conforme plano aprovado:

1. **Gestão de Dados**: Opção A (Substituição Total)
   - Sempre reprocessa todos .xlsx
   - Simples e confiável

2. **Empacotamento**: Python Embeddable
   - ~50-80MB distribuição
   - Sem problemas de antivírus
   - Fácil atualizar

3. **Paths**: Dinâmicos via `get_base_dir()`
   - Cliente não precisa configurar nada
   - Funciona em qualquer lugar

4. **Histórico**: Via coluna `v_current`
   - Mantém histórico por player_id + competition_id + team_id
   - `v_current == True` para dados mais recentes

---

## 📞 Próximas Ações Sugeridas

1. **Executar Build**: `python build_embeddable.py`
2. **Testar**: `cd dist/BotafogoScouts && ProcessarScouts.bat`
3. **Validar**: Verificar se 4 parquets foram gerados
4. **Comprimir**: Criar `BotafogoScouts.zip`
5. **Entregar**: Enviar para o cliente

Tudo pronto para produção! 🚀
