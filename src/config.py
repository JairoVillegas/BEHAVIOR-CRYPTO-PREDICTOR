# src/config.py
# Aquí definimos la configuración básica del proyecto.

# Monedas a analizar (IDs de CoinGecko)
COINS = [
    "bitcoin",
    "ethereum",
    "solana",
    "binancecoin",   # BNB
    "ripple",        # XRP
    "dogecoin",      # DOGE
   "cardano",       # ADA
    "polkadot",      # DOT
    "avalanche-2",   # AVAX
    "shiba-inu"      # SHIB
]


# Moneda en la que queremos los precios
VS_CURRENCY = "usd"

# Días de histórico que queremos descargar (por ejemplo 365 = 1 año)
DAYS_HISTORY = 365
