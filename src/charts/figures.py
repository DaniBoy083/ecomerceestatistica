"""
Módulo de gráficos — cada função retorna uma figura Plotly independente.
Segue o princípio de responsabilidade única: uma função, um gráfico.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Paleta de cores consistente em toda a aplicação
PALETTE = px.colors.qualitative.Pastel
PRIMARY_COLOR = "#6C63FF"
BG_COLOR = "#F8F9FA"
PAPER_COLOR = "#FFFFFF"

_LAYOUT_BASE = dict(
    paper_bgcolor=PAPER_COLOR,
    plot_bgcolor=BG_COLOR,
    font=dict(family="Inter, sans-serif", size=13),
    margin=dict(t=50, b=40, l=40, r=20),
)


# ---------------------------------------------------------------------------
# 1. Distribuição de Notas (Histograma)
# ---------------------------------------------------------------------------
def fig_distribuicao_notas(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df,
        x="Nota",
        nbins=20,
        title="Distribuição das Notas dos Produtos",
        labels={"Nota": "Nota", "count": "Quantidade"},
        color_discrete_sequence=[PRIMARY_COLOR],
    )
    fig.update_layout(**_LAYOUT_BASE)
    fig.update_traces(marker_line_color="white", marker_line_width=1)
    return fig


# ---------------------------------------------------------------------------
# 2. Top 10 Marcas por Quantidade Vendida (Barras horizontais)
# ---------------------------------------------------------------------------
def fig_top_marcas(df: pd.DataFrame) -> go.Figure:
    top = (
        df.groupby("Marca")["Qtd_Vendidos_Num"]
        .sum()
        .nlargest(10)
        .reset_index()
        .sort_values("Qtd_Vendidos_Num")
    )
    fig = px.bar(
        top,
        x="Qtd_Vendidos_Num",
        y="Marca",
        orientation="h",
        title="Top 10 Marcas por Quantidade Vendida",
        labels={"Qtd_Vendidos_Num": "Qtd. Vendidos", "Marca": "Marca"},
        color="Qtd_Vendidos_Num",
        color_continuous_scale="Purples",
    )
    fig.update_layout(**_LAYOUT_BASE, coloraxis_showscale=False)
    return fig


# ---------------------------------------------------------------------------
# 3. Preço vs Nota (Scatter)
# ---------------------------------------------------------------------------
def fig_preco_vs_nota(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        x="Preço",
        y="Nota",
        color="Gênero",
        size="N_Avaliações",
        hover_data=["Título", "Marca"],
        title="Preço vs Nota por Gênero",
        labels={"Preço": "Preço (R$)", "Nota": "Nota média"},
        color_discrete_sequence=PALETTE,
        size_max=30,
    )
    fig.update_layout(**_LAYOUT_BASE)
    return fig


# ---------------------------------------------------------------------------
# 4. Distribuição por Gênero (Pizza)
# ---------------------------------------------------------------------------
def fig_distribuicao_genero(df: pd.DataFrame) -> go.Figure:
    contagem = df["Gênero"].value_counts().reset_index()
    contagem.columns = ["Gênero", "Quantidade"]
    fig = px.pie(
        contagem,
        names="Gênero",
        values="Quantidade",
        title="Distribuição de Produtos por Gênero",
        color_discrete_sequence=PALETTE,
        hole=0.35,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(**_LAYOUT_BASE)
    return fig


# ---------------------------------------------------------------------------
# 5. Desconto vs Quantidade Vendida (Scatter)
# ---------------------------------------------------------------------------
def fig_desconto_vs_vendas(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        x="Desconto",
        y="Qtd_Vendidos_Num",
        color="Material",
        hover_data=["Título", "Marca"],
        title="Impacto do Desconto nas Vendas",
        labels={"Desconto": "Desconto (%)", "Qtd_Vendidos_Num": "Qtd. Vendidos"},
        color_discrete_sequence=PALETTE,
        trendline="ols",
    )
    fig.update_layout(**_LAYOUT_BASE)
    return fig


# ---------------------------------------------------------------------------
# 6. Média de Nota por Material (Barras verticais)
# ---------------------------------------------------------------------------
def fig_nota_por_material(df: pd.DataFrame) -> go.Figure:
    media = (
        df.groupby("Material")["Nota"]
        .mean()
        .reset_index()
        .sort_values("Nota", ascending=False)
        .head(12)
    )
    fig = px.bar(
        media,
        x="Material",
        y="Nota",
        title="Média de Nota por Material (Top 12)",
        labels={"Nota": "Nota Média", "Material": "Material"},
        color="Nota",
        color_continuous_scale="Purples",
    )
    fig.update_layout(**_LAYOUT_BASE, coloraxis_showscale=False, xaxis_tickangle=-30)
    return fig


# ---------------------------------------------------------------------------
# 7. Vendas por Temporada (Barras agrupadas)
# ---------------------------------------------------------------------------
def fig_vendas_por_temporada(df: pd.DataFrame) -> go.Figure:
    grupo = (
        df.groupby(["Temporada", "Gênero"])["Qtd_Vendidos_Num"]
        .sum()
        .reset_index()
    )
    fig = px.bar(
        grupo,
        x="Temporada",
        y="Qtd_Vendidos_Num",
        color="Gênero",
        barmode="group",
        title="Vendas por Temporada e Gênero",
        labels={"Qtd_Vendidos_Num": "Qtd. Vendidos", "Temporada": "Temporada"},
        color_discrete_sequence=PALETTE,
    )
    fig.update_layout(**_LAYOUT_BASE, xaxis_tickangle=-20)
    return fig


# ---------------------------------------------------------------------------
# 8. Correlação — Heatmap
# ---------------------------------------------------------------------------
def fig_correlacao(df: pd.DataFrame) -> go.Figure:
    colunas = ["Nota", "N_Avaliações", "Desconto", "Preço", "Qtd_Vendidos_Num"]
    corr = df[colunas].corr().round(2)
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title="Mapa de Correlação entre Variáveis Numéricas",
        aspect="auto",
    )
    fig.update_layout(**_LAYOUT_BASE)
    return fig
