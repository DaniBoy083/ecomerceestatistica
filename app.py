"""
Ponto de entrada da aplicação Dash — E-Commerce Analytics Dashboard.

Responsabilidades deste módulo:
  - Inicializar o app Dash
  - Registrar os callbacks (interatividade)
  - Iniciar o servidor

A lógica de dados está em src/data/ e os gráficos em src/charts/.
O layout está em src/layout/.
"""

import dash
from dash import Input, Output
import pandas as pd

from src.data import carregar_dados
from src.layout import criar_layout
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

# ── Inicialização ─────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    title="E-Commerce Analytics",
    suppress_callback_exceptions=True,
)
server = app.server  # expõe o Flask server (para deploy via gunicorn)

# Carrega os dados uma única vez na inicialização
df_global: pd.DataFrame = carregar_dados()

app.layout = criar_layout(df_global)


# ── Helpers ───────────────────────────────────────────────────────────────────
def _filtrar(
    df: pd.DataFrame,
    generos: list[str] | None,
    temporadas: list[str] | None,
    faixa_preco: list[float],
) -> pd.DataFrame:
    """Aplica os filtros do usuário ao DataFrame global."""
    mask = (df["Preço"] >= faixa_preco[0]) & (df["Preço"] <= faixa_preco[1])
    if generos:
        mask &= df["Gênero"].isin(generos)
    if temporadas:
        mask &= df["Temporada"].isin(temporadas)
    return df[mask]


# ── Callbacks ─────────────────────────────────────────────────────────────────
@app.callback(
    Output("graf-notas", "figure"),
    Output("graf-marcas", "figure"),
    Output("graf-preco-nota", "figure"),
    Output("graf-genero", "figure"),
    Output("graf-desconto", "figure"),
    Output("graf-material", "figure"),
    Output("graf-temporada", "figure"),
    Output("graf-correlacao", "figure"),
    Input("filtro-genero", "value"),
    Input("filtro-temporada", "value"),
    Input("filtro-preco", "value"),
)
def atualizar_graficos(
    generos: list[str] | None,
    temporadas: list[str] | None,
    faixa_preco: list[float],
):
    """
    Callback principal: recebe os filtros e retorna todas as figuras atualizadas.
    Utiliza um único callback para minimizar round-trips ao servidor.
    """
    df = _filtrar(df_global, generos, temporadas, faixa_preco)

    if df.empty:
        import plotly.graph_objects as go
        fig_vazia = go.Figure()
        fig_vazia.update_layout(
            annotations=[{
                "text": "Nenhum dado para os filtros selecionados.",
                "xref": "paper", "yref": "paper",
                "showarrow": False, "font": {"size": 16},
            }]
        )
        return [fig_vazia] * 8

    return (
        fig_distribuicao_notas(df),
        fig_top_marcas(df),
        fig_preco_vs_nota(df),
        fig_distribuicao_genero(df),
        fig_desconto_vs_vendas(df),
        fig_nota_por_material(df),
        fig_vendas_por_temporada(df),
        fig_correlacao(df),
    )


# ── Entry-point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
