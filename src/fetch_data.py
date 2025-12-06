# src/fetch_data.py

import os
import time
import requests
import pandas as pd

from .config import COINS, VS_CURRENCY, DAYS_HISTORY

BASE_URL = "https://api.coingecko.com/api/v3"


def fetch_market_chart(coin_id, vs_currency="usd", days=365):
    """
    Descarga datos históricos de una cripto desde CoinGecko.
    Devuelve un DataFrame con columnas: coin, datetime, price, volume.
    """
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days
    }

    # Hacemos la petición HTTP a la API
    response = requests.get(url, params=params)
    response.raise_for_status()  # lanza error si la respuesta no es 200

    data = response.json()

    # data["prices"] es una lista de pares [timestamp_ms, price]
    prices = data.get("prices", [])
    # data["total_volumes"] es una lista [timestamp_ms, volume]
    volumes = data.get("total_volumes", [])

    # Convertimos a DataFrame
    df_prices = pd.DataFrame(prices, columns=["timestamp_ms", "price"])
    df_volumes = pd.DataFrame(volumes, columns=["timestamp_ms", "volume"])

    # Unimos por timestamp
    df = pd.merge(df_prices, df_volumes, on="timestamp_ms", how="left")

    # Pasamos de milisegundos a datetime
    df["datetime"] = pd.to_datetime(df["timestamp_ms"], unit="ms")

    # Agregamos la columna de la moneda
    df["coin"] = coin_id

    # Ordenamos por tiempo y seleccionamos columnas finales
    df = df[["coin", "datetime", "price", "volume"]].sort_values(by="datetime")

    return df


def fetch_and_save_all(output_path="data/raw/prices_raw.csv"):
    """
    Descarga el histórico para todas las monedas en COINS
    y guarda un CSV combinado en data/raw/prices_raw.csv
    """
    # Creamos la carpeta data/raw si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    all_dfs = []

    for coin in COINS:
        print(f"Descargando datos de {coin}...")
        df_coin = fetch_market_chart(coin, VS_CURRENCY, DAYS_HISTORY)
        all_dfs.append(df_coin)
        # pausa entre cada petición, pq si no la api nos bloquea
        time.sleep(15)

    # Concatenamos todos los DataFrames en uno solo
    df_all = pd.concat(all_dfs, ignore_index=True)

    # Guardamos a CSV
    df_all.to_csv(output_path, index=False)
    print(f"Datos guardados en {output_path}")
