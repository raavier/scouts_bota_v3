# 🎨 Streamlit App - Gerenciador de Pesos

Interface web interativa para gerenciar o arquivo `base_peso.xlsx` do projeto Scouts Bota.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Funcionalidades](#-funcionalidades)
- [Estrutura de Arquivos](#-estrutura-de-arquivos)
- [Perguntas Frequentes](#-perguntas-frequentes)

---

## 🎯 Visão Geral

Esta aplicação Streamlit permite que você visualize e edite os pesos dos indicadores por posição de forma intuitiva, sem precisar editar planilhas Excel manualmente.

### Principais Características:

✅ **Interface intuitiva** - Edite pesos usando sliders ou input manual
✅ **Busca rápida** - Encontre indicadores facilmente
✅ **Backup automático** - Cria backup antes de salvar
✅ **Validação em tempo real** - Previne erros de dados
✅ **Isolado do pipeline** - Não interfere no processamento existente

---

## 🔧 Pré-requisitos

- **Python 3.11 ou superior**
- **pip** (gerenciador de pacotes Python)
- Arquivo `base_peso.xlsx` em `bases/inputs/business/` (ou use o gerador de exemplo)

---

## 📦 Instalação

### Opção 1: Instalação Automática (Windows)

```bash
# Execute o script batch
run_streamlit.bat
```

O script irá:
1. Verificar se Python está instalado
2. Instalar dependências automaticamente
3. Iniciar a aplicação

### Opção 2: Instalação Manual

```bash
# 1. Instalar dependências
pip install -r requirements_streamlit.txt

# 2. Executar aplicação
streamlit run streamlit_app/app.py
```

---

## 🚀 Como Usar

### Passo 1: Iniciar a Aplicação

Execute `run_streamlit.bat` (Windows) ou:

```bash
streamlit run streamlit_app/app.py
```

A aplicação abrirá automaticamente no navegador em: `http://localhost:8501`

### Passo 2: Carregar Dados

1. Clique em **"📁 Carregar Dados"** na barra lateral
2. Se o arquivo não existir, clique em **"🔨 Criar Arquivo de Exemplo"**

### Passo 3: Selecionar Posição

No dropdown principal, selecione a posição que deseja editar:

- GK - Goleiro
- CB - Zagueiro Central
- RCB - Zagueiro Direito
- LCB - Zagueiro Esquerdo
- RB - Lateral Direito
- LB - Lateral Esquerdo
- DM - Volante
- CM - Meio-Campo Central
- AM - Meia Atacante
- LW - Ponta Esquerda
- RW - Ponta Direita
- CF - Centro-Avante

### Passo 4: Buscar Indicador (Opcional)

Use o campo de busca para filtrar indicadores:

```
Digite: "Passes"
Resultado: Mostra apenas indicadores que contém "Passes" no nome
```

**Dica:** Marque "Apenas Ativos" para ver somente indicadores com CONSIDERAR? = SIM

### Passo 5: Editar Indicadores

Para cada indicador, você pode editar:

#### 📋 Configurações:
- **Considerar?** - Se o indicador está ativo (SIM/NÃO)
- **Melhor para** - Direção de normalização (CIMA/BAIXO)
- **Classificação Ranking** - Categoria do indicador
- **Especial?** - Marcador especial
- **Explicação** - Descrição do indicador

#### ⚖️ Peso:
- Use o **slider** para ajustar visualmente (0-100)
- Ou digite um **valor exato** no input
- O número grande mostra o valor atual
- A barra de progresso mostra visualmente o peso

### Passo 6: Salvar Alterações

Quando terminar de editar:

1. Clique em **"✅ Salvar Todas"** (cria backup automático)
2. Ou clique em **"❌ Descartar Todas"** para cancelar

---

## ✨ Funcionalidades

### 🎯 Editor de Pesos por Posição

- Selecione UMA posição por vez para editar
- Edite os pesos de todos os indicadores para aquela posição
- Visualização clara com slider + input manual

### 🔍 Busca e Filtros

- **Busca por nome**: Encontre indicadores rapidamente
- **Filtro de ativos**: Mostre apenas indicadores ativos
- **Contador**: Veja quantos indicadores estão sendo exibidos

### 📊 Estatísticas

A barra lateral mostra:
- Total de indicadores
- Indicadores ativos
- Indicadores inativos

### 💾 Sistema de Backup

- **Backup automático**: Criado antes de cada salvamento
- **Localização**: `bases/inputs/business/backups/`
- **Formato**: `base_peso_backup_YYYYMMDD_HHMMSS.xlsx`
- **Visualização**: Lista de backups disponíveis na sidebar

### ⚠️ Controle de Alterações

- Indicador visual de alterações não salvas
- Botões de Salvar/Descartar sempre visíveis
- Confirmação antes de descartar mudanças

---

## 📁 Estrutura de Arquivos

```
scouts_bota_v3/
├── streamlit_app/
│   ├── __init__.py
│   ├── app.py                      # Aplicação principal
│   ├── components/
│   │   ├── __init__.py
│   │   └── data_loader.py          # Carrega/salva Excel
│   └── utils/
│       ├── __init__.py
│       └── constants.py            # Constantes (posições, etc)
├── bases/
│   └── inputs/
│       └── business/
│           ├── base_peso.xlsx      # Arquivo principal
│           └── backups/            # Backups automáticos
├── requirements_streamlit.txt      # Dependências
├── run_streamlit.bat              # Script de execução
└── README_STREAMLIT.md            # Esta documentação
```

---

## 🎨 Interface

### Tela Principal

```
╔══════════════════════════════════════════════════════════╗
║  ⚽ Scouts Bota - Gerenciador de Pesos                   ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║                                                          ║
║  1️⃣ Selecione a Posição                                  ║
║  Posição: [GK - Goleiro ▾]                              ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║                                                          ║
║  2️⃣ Buscar Indicadores                                   ║
║  [___________________________] [☐ Apenas Ativos]        ║
║  📋 Mostrando 206 de 206 indicadores                     ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║                                                          ║
║  3️⃣ Editar Indicadores - Goleiro                         ║
║                                                          ║
║  ▶ 📊 Passes Attempted                                   ║
║  ▼ 📊 Tackles                                            ║
║    ┌─────────────────────┬──────────────────┐           ║
║    │ ⚙️ Configurações     │ ⚖️ Peso para GK   │           ║
║    │                     │                  │           ║
║    │ Considerar: [SIM▾]  │ Ajustar: [█████] │           ║
║    │ Melhor: [CIMA▾]     │ Ou digite: [85]  │           ║
║    │ Categoria: [DEF]    │                  │           ║
║    │ Especial: [____]    │       85         │           ║
║    │                     │ ████████████░░░░ │           ║
║    └─────────────────────┴──────────────────┘           ║
║  ▶ 📊 Shots                                              ║
║                                                          ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║  💾 Salvar Alterações                                    ║
║  [✅ Salvar Todas] [❌ Descartar Todas] [⚠️ 3 editados]  ║
╚══════════════════════════════════════════════════════════╝
```

---

## ❓ Perguntas Frequentes

### Como o Streamlit interage com o pipeline de processamento?

O Streamlit **apenas edita** o arquivo `base_peso.xlsx`. O pipeline de processamento continua funcionando normalmente, carregando o arquivo quando você executa `ProcessarScouts.bat`.

**Workflow:**
```
1. Streamlit → Edita base_peso.xlsx
2. Você salva as alterações
3. ProcessarScouts.bat → Carrega base_peso.xlsx
4. Pipeline processa com os novos pesos
```

### Os backups são criados automaticamente?

Sim! Sempre que você clica em "Salvar Todas", um backup com timestamp é criado em:
```
bases/inputs/business/backups/base_peso_backup_YYYYMMDD_HHMMSS.xlsx
```

### Posso editar múltiplas posições ao mesmo tempo?

Não nesta versão. A interface foi projetada para editar UMA posição por vez, o que facilita o foco e evita confusão.

Para editar outra posição:
1. Salve as alterações atuais
2. Selecione outra posição no dropdown
3. Edite os pesos

### E se eu fechar o navegador sem salvar?

As alterações **não são perdidas** enquanto a aplicação Streamlit estiver rodando! O estado é mantido na sessão. Mas **ATENÇÃO**: se você parar o servidor Streamlit (Ctrl+C), as alterações não salvas serão perdidas.

**Recomendação:** Sempre salve antes de fechar.

### Como restaurar um backup?

Por enquanto, manualmente:
1. Vá para `bases/inputs/business/backups/`
2. Encontre o backup desejado
3. Copie e substitua o arquivo `base_peso.xlsx`

*Feature de restauração automática em desenvolvimento!*

### Posso adicionar novos indicadores?

Na versão atual, você pode editar indicadores existentes. Para adicionar novos:
1. Edite o Excel manualmente, ou
2. Aguarde a próxima versão com formulário de adição!

### A aplicação funciona em Mac/Linux?

Sim! Use o comando manual:
```bash
streamlit run streamlit_app/app.py
```

O script `.bat` é apenas para Windows.

### Como parar a aplicação?

- **Windows**: Pressione `Ctrl+C` no terminal
- **Ou**: Feche a janela do terminal

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'streamlit'"

**Solução:**
```bash
pip install -r requirements_streamlit.txt
```

### Erro: "Arquivo base_peso.xlsx não encontrado"

**Solução 1:** Copie seu arquivo para `bases/inputs/business/base_peso.xlsx`

**Solução 2:** Clique em "Criar Arquivo de Exemplo" na aplicação

### A aplicação não abre no navegador

**Solução:**
1. Veja a URL no terminal (geralmente `http://localhost:8501`)
2. Abra manualmente no navegador
3. Se a porta 8501 estiver ocupada, o Streamlit usará outra (8502, 8503...)

### Alterações não estão sendo salvas

**Verifique:**
1. Você clicou em "Salvar Todas"?
2. Há mensagem de erro no terminal?
3. Você tem permissão de escrita na pasta?

---

## 🔄 Workflow Recomendado

1. **Abra a aplicação** → `run_streamlit.bat`
2. **Carregue os dados** → Botão "Carregar Dados"
3. **Selecione a posição** → Dropdown de posições
4. **Busque indicadores** (opcional) → Campo de busca
5. **Edite os pesos** → Slider ou input manual
6. **Salve** → Botão "Salvar Todas"
7. **Teste no pipeline** → Execute `ProcessarScouts.bat`
8. **Verifique outputs** → Confira `consolidated_overall.parquet`

---

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte este README
- Verifique os logs no terminal
- Revise a seção de Troubleshooting

---

## 🎯 Próximas Funcionalidades (Roadmap)

- [ ] Restaurar backups pela interface
- [ ] Adicionar novos indicadores via formulário
- [ ] Visualização gráfica de distribuição de pesos
- [ ] Comparar pesos entre posições
- [ ] Exportar/importar configurações
- [ ] Validação avançada de dados
- [ ] Tema dark mode

---

**Versão:** 1.0
**Data:** 2026-01-12
**Autor:** Claude (Sonnet 4.5)
