"""
Módulo responsável pelo carregamento e pré-processamento dos dados.
Segue o princípio de responsabilidade única (SRP).
"""

import pandas as pd
import re
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[2] / "input" / "ecommerce_estatistica.csv"


def _parse_qtd_vendidos(valor: str) -> float:
    """Converte strings como '+10mil', '+500' para valores numéricos."""
    if pd.isna(valor):
        return 0.0
    valor = str(valor).strip().replace("+", "").lower()
    if "mil" in valor:
        numero = re.sub(r"[^\d]", "", valor.replace("mil", ""))
        return float(numero) * 1000 if numero else 0.0
    numero = re.sub(r"[^\d]", "", valor)
    return float(numero) if numero else 0.0


def carregar_dados() -> pd.DataFrame:
    """
    Carrega o CSV e aplica transformações necessárias.

    Returns:
        pd.DataFrame: DataFrame tratado e pronto para visualização.

    Raises:
        FileNotFoundError: Se o arquivo CSV não for encontrado.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {DATA_PATH}\n"
            "Certifique-se de que 'ecommerce_estatistica.csv' está na pasta 'input/'."
        )

    df = pd.read_csv(DATA_PATH)

    # Renomear coluna de índice desnecessária
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")

    # Converter Qtd_Vendidos para numérico
    df["Qtd_Vendidos_Num"] = df["Qtd_Vendidos"].apply(_parse_qtd_vendidos)

    # Garantir tipos corretos
    df["Nota"] = pd.to_numeric(df["Nota"], errors="coerce")
    df["N_Avaliações"] = pd.to_numeric(df["N_Avaliações"], errors="coerce")
    df["Desconto"] = pd.to_numeric(df["Desconto"], errors="coerce")
    df["Preço"] = pd.to_numeric(df["Preço"], errors="coerce")

    # Normalizar strings categóricas
    for col in ["Marca", "Material", "Gênero", "Temporada"]:
        df[col] = df[col].astype(str).str.strip().str.lower()

    return df
