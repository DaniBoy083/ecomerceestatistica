"""
Módulo de layout — define a estrutura visual da aplicação Dash.
Separado da lógica de dados e dos callbacks (SRP).
"""

from dash import dcc, html
import pandas as pd

from src.charts import (
    fig_distribuicao_notas,
    fig_top_marcas,
    fig_preco_vs_nota,
    fig_distribuicao_genero,
    fig_desconto_vs_vendas,
    fig_nota_por_material,
    fig_vendas_por_temporada,
    fig_correlacao,
)


def _card(titulo: str, graph_id: str) -> html.Div:
    """Cria um card padronizado que envolve um gráfico."""
    return html.Div(
        className="card",
        children=[
            html.H3(titulo, className="card-title"),
            dcc.Graph(id=graph_id, config={"displayModeBar": False}),
        ],
    )


def criar_layout(df: pd.DataFrame) -> html.Div:
    """
    Monta o layout completo da aplicação.

    Args:
        df: DataFrame já processado.

    Returns:
        html.Div: Componente raiz do Dash.
    """
    # KPIs do cabeçalho
    total_produtos = len(df)
    nota_media = df["Nota"].mean()
    total_vendas = df["Qtd_Vendidos_Num"].sum()
    desconto_medio = df["Desconto"].mean()

    return html.Div(
        id="root",
        children=[
            # ── Header ────────────────────────────────────────────────────
            html.Header(
                className="header",
                children=[
                    html.Div(
                        className="header-inner",
                        children=[
                            html.Div(
                                className="logo-block",
                                children=[
                                    html.Span("🛍️", className="logo-icon"),
                                    html.Div([
                                        html.H1("E-Commerce Analytics", className="app-title"),
                                        html.P("Dashboard de análise estatística", className="app-subtitle"),
                                    ]),
                                ],
                            ),
                        ],
                    )
                ],
            ),

            # ── KPI Cards ─────────────────────────────────────────────────
            html.Section(
                className="kpi-section",
                children=[
                    html.Div(className="kpi-card", children=[
                        html.Span("📦", className="kpi-icon"),
                        html.P("Total de Produtos", className="kpi-label"),
                        html.H2(f"{total_produtos:,}", className="kpi-value"),
                    ]),
                    html.Div(className="kpi-card", children=[
                        html.Span("⭐", className="kpi-icon"),
                        html.P("Nota Média", className="kpi-label"),
                        html.H2(f"{nota_media:.2f}", className="kpi-value"),
                    ]),
                    html.Div(className="kpi-card", children=[
                        html.Span("🛒", className="kpi-icon"),
                        html.P("Total Vendidos", className="kpi-label"),
                        html.H2(f"{total_vendas:,.0f}", className="kpi-value"),
                    ]),
                    html.Div(className="kpi-card", children=[
                        html.Span("🏷️", className="kpi-icon"),
                        html.P("Desconto Médio", className="kpi-label"),
                        html.H2(f"{desconto_medio:.1f}%", className="kpi-value"),
                    ]),
                ],
            ),

            # ── Filtros ───────────────────────────────────────────────────
            html.Section(
                className="filter-section",
                children=[
                    html.Div(className="filter-group", children=[
                        html.Label("Gênero", className="filter-label"),
                        dcc.Dropdown(
                            id="filtro-genero",
                            options=[{"label": g.title(), "value": g} for g in sorted(df["Gênero"].unique())],
                            multi=True,
                            placeholder="Todos os gêneros...",
                            className="dropdown",
                        ),
                    ]),
                    html.Div(className="filter-group", children=[
                        html.Label("Temporada", className="filter-label"),
                        dcc.Dropdown(
                            id="filtro-temporada",
                            options=[{"label": t.title(), "value": t} for t in sorted(df["Temporada"].unique())],
                            multi=True,
                            placeholder="Todas as temporadas...",
                            className="dropdown",
                        ),
                    ]),
                    html.Div(className="filter-group", children=[
                        html.Label("Faixa de Preço (R$)", className="filter-label"),
                        dcc.RangeSlider(
                            id="filtro-preco",
                            min=df["Preço"].min(),
                            max=df["Preço"].max(),
                            value=[df["Preço"].min(), df["Preço"].max()],
                            marks={
                                int(df["Preço"].min()): f'R${df["Preço"].min():.0f}',
                                int(df["Preço"].max()): f'R${df["Preço"].max():.0f}',
                            },
                            tooltip={"placement": "bottom", "always_visible": True},
                            className="range-slider",
                        ),
                    ]),
                ],
            ),

            # ── Grid de gráficos ──────────────────────────────────────────
            html.Main(
                className="charts-grid",
                children=[
                    _card("Distribuição das Notas", "graf-notas"),
                    _card("Top 10 Marcas por Vendas", "graf-marcas"),
                    _card("Preço vs Nota", "graf-preco-nota"),
                    _card("Produtos por Gênero", "graf-genero"),
                    _card("Impacto do Desconto nas Vendas", "graf-desconto"),
                    _card("Nota Média por Material", "graf-material"),
                    _card("Vendas por Temporada e Gênero", "graf-temporada"),
                    _card("Mapa de Correlação", "graf-correlacao"),
                ],
            ),

            # ── Footer ────────────────────────────────────────────────────
            html.Footer(
                className="footer",
                children=[
                    html.P("Projeto 3 — EBAC Data Science · Desenvolvido com Dash & Plotly"),
                ],
            ),
        ],
    )
