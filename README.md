# 🛍️ E-Commerce Analytics Dashboard

Dashboard interativo desenvolvido com **Dash** e **Plotly** para análise estatística de um dataset de e-commerce. Projeto 3 do curso de Data Science da EBAC.

---

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Gráficos Disponíveis](#gráficos-disponíveis)
- [Arquitetura](#arquitetura)
- [Dataset](#dataset)
- [Tecnologias](#tecnologias)

---

## 🎯 Visão Geral

O **E-Commerce Analytics Dashboard** transforma os dados do arquivo `ecommerce_estatistica.csv` em uma aplicação web interativa, permitindo que o usuário final explore os dados **sem precisar interagir com Python**.

A aplicação roda localmente e exibe **8 gráficos** com filtros dinâmicos por Gênero, Temporada e Faixa de Preço, além de **4 KPIs** no cabeçalho.

---

## ✨ Funcionalidades

| Recurso | Descrição |
|---|---|
| 📊 8 gráficos interativos | Histograma, barras, scatter, pizza, heatmap |
| 🎛️ Filtros dinâmicos | Gênero, Temporada e Faixa de Preço |
| 📈 KPIs em tempo real | Total de produtos, nota média, vendas e desconto |
| 🎨 Design responsivo | Grid adaptável para qualquer resolução |
| 🔄 Atualização reativa | Todos os gráficos atualizam simultaneamente ao filtrar |

---

## 📁 Estrutura do Projeto

```
projeto3/
│
├── app.py                  # Ponto de entrada — Dash app + callbacks
│
├── src/                    # Código-fonte (Clean Architecture)
│   ├── data/
│   │   └── loader.py       # Carregamento e pré-processamento do CSV
│   ├── charts/
│   │   └── figures.py      # Funções que retornam figuras Plotly
│   └── layout/
│       └── layout.py       # Estrutura visual do Dash (HTML/componentes)
│
├── assets/
│   └── style.css           # Estilos globais da aplicação
│
├── input/
│   └── ecommerce_estatistica.csv  # Dataset de origem
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Pré-requisitos

- Python **3.10+**
- pip

---

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/projeto3-ecommerce-dash.git
cd projeto3-ecommerce-dash
```

### 2. Crie e ative um ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
python app.py
```

### 5. Acesse no navegador

```
http://127.0.0.1:8050
```

---

## 📊 Gráficos Disponíveis

| # | Gráfico | Tipo | Descrição |
|---|---|---|---|
| 1 | Distribuição das Notas | Histograma | Frequência das notas dos produtos |
| 2 | Top 10 Marcas por Vendas | Barras horizontais | Marcas com maior volume de vendas |
| 3 | Preço vs Nota | Scatter | Relação entre preço e avaliação por gênero |
| 4 | Produtos por Gênero | Pizza (donut) | Proporção de produtos por gênero |
| 5 | Impacto do Desconto nas Vendas | Scatter + tendência | Correlação desconto × quantidade vendida |
| 6 | Nota Média por Material | Barras verticais | Top 12 materiais por nota média |
| 7 | Vendas por Temporada e Gênero | Barras agrupadas | Volume de vendas cruzando temporada e gênero |
| 8 | Mapa de Correlação | Heatmap | Correlação entre todas as variáveis numéricas |

---

## 🏛️ Arquitetura

O projeto segue os princípios de **Clean Architecture** e **Clean Code**:

```
┌─────────────────────────────────────────┐
│                  app.py                  │  ← Orquestração e callbacks
├───────────┬──────────────┬──────────────┤
│  src/data │  src/charts  │  src/layout  │  ← Camadas independentes
│  loader   │   figures    │   layout     │
└───────────┴──────────────┴──────────────┘
                    ↑
              input/  (dados)
              assets/ (estilos)
```

**Princípios aplicados:**

- **SRP** — cada módulo tem uma única responsabilidade
- **DRY** — layout base e paleta de cores centralizados
- **Funções puras** — cada `fig_*` recebe um DataFrame e retorna uma figura
- **Separação de camadas** — dados, visualização e layout totalmente desacoplados
- **Nomes descritivos** — funções e variáveis autoexplicativas em português

---

## 🗂️ Dataset

Arquivo: `input/ecommerce_estatistica.csv`  
Registros: **295 produtos**  
Colunas relevantes:

| Coluna | Tipo | Descrição |
|---|---|---|
| Título | str | Nome do produto |
| Nota | float | Avaliação média (0–5) |
| N_Avaliações | float | Número de avaliações |
| Desconto | float | Percentual de desconto |
| Marca | str | Marca do produto |
| Material | str | Material predominante |
| Gênero | str | Público-alvo (Masculino/Feminino/Unissex) |
| Temporada | str | Temporada indicada |
| Qtd_Vendidos | str | Faixa de quantidade vendida (+100, +1000, +10mil…) |
| Preço | float | Preço em reais |

---

## 🛠️ Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| [Dash](https://dash.plotly.com/) | 2.17.1 | Framework web para dashboards Python |
| [Plotly](https://plotly.com/python/) | 5.22.0 | Gráficos interativos |
| [Pandas](https://pandas.pydata.org/) | 2.2.2 | Manipulação de dados |
| [Statsmodels](https://www.statsmodels.org/) | 0.14.2 | Linha de tendência (OLS) no scatter |
| [Gunicorn](https://gunicorn.org/) | 22.0.0 | Servidor WSGI para deploy |

---

## 👤 Autor

**Daniel** — Estudante de Ciência da Computação  
Curso de Data Science — EBAC  

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
