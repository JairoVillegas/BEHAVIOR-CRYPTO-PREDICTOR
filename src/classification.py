import os
import pandas as pd


def build_supervised_dataset(
    input_path="data/processed/prices_features.csv",
    output_path="data/processed/supervised_dataset.csv",
    horizon=1
):
    """
    Construye un dataset supervisado para clasificación binaria:
    target = 1 si el precio dentro de 'horizon' días es mayor al actual, 0 en caso contrario.

    - input_path: CSV con las features diarias por moneda.
    - output_path: dónde guardar el dataset supervisado.
    - horizon: cuántos días hacia adelante queremos mirar (por defecto 1).
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    df = pd.read_csv(input_path, parse_dates=["datetime"])

    # Ordenamos por moneda y fecha
    df = df.sort_values(by=["coin", "datetime"])

    # Precio futuro por moneda (shift negativo)
    df["future_price"] = (
        df.groupby("coin")["price"]
        .shift(-horizon)
    )

    # Variable objetivo: 1 si el precio futuro es mayor al actual, 0 si no.
    df["target_up"] = (df["future_price"] > df["price"]).astype(int)

    # Eliminamos filas sin futuro (las últimas de cada moneda)
    df = df.dropna(subset=["future_price"])

    # Elegimos columnas de features que vamos a usar para el modelo
    feature_cols = [
        "coin",
        "datetime",
        "price",
        "volume",
        "ret_log",
        "vol_rolling",
        "volumen_promedio",
        "drawdown"
    ]

    df_supervised = df[feature_cols + ["target_up"]]

    # Guardamos
    df_supervised.to_csv(output_path, index=False)
    print(f"Dataset supervisado guardado en {output_path}")

    return df_supervised
