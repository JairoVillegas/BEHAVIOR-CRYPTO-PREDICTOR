import os
import numpy as np
import pandas as pd


def compute_drawdown(series):
    """
    Calcula el drawdown de una serie de precios.
    (precio - máximo_acumulado) / máximo_acumulado
    """
    running_max = series.cummax()
    drawdown = (series - running_max) / running_max
    return drawdown


def transform_raw_to_features(
    input_path="data/raw/prices_raw.csv",
    output_path="data/processed/prices_features.csv",
    window_vol=30
):
    """
    Lee el archivo crudo y genera métricas:
    - retornos logarítmicos
    - volatilidad rolling
    - volumen promedio rolling
    - drawdown
    """

    # Nos aseguramos de que exista la carpeta de salida
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Leemos el CSV crudo
    df = pd.read_csv(input_path, parse_dates=["datetime"])

    # Ordenamos por moneda y fecha
    df = df.sort_values(by=["coin", "datetime"])

    # ---- RETORNOS LOGARÍTMICOS ----
    # r_t = ln(P_t / P_{t-1})
    df["ret_log"] = (
        df.groupby("coin")["price"]
        .transform(lambda s: np.log(s / s.shift(1)))
    )

    # ---- VOLATILIDAD ROLLING ----
    df["vol_rolling"] = (
        df.groupby("coin")["ret_log"]
        .transform(lambda s: s.rolling(window_vol).std())
    )

    # ---- VOLUMEN PROMEDIO ROLLING ----
    df["volumen_promedio"] = (
        df.groupby("coin")["volume"]
        .transform(lambda s: s.rolling(window_vol).mean())
    )

    # ---- DRAWDOWN ----
    df["drawdown"] = (
        df.groupby("coin")["price"]
        .transform(compute_drawdown)
    )

    # Guardamos el resultado
    df.to_csv(output_path, index=False)
    print(f"Datos procesados guardados en {output_path}")
