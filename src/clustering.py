import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def build_features_per_coin(input_path="data/processed/prices_features.csv"):
    """
    Construye un dataset con una fila por moneda:
    ret_mean, vol_mean, volume_mean, dd_min
    """
    df = pd.read_csv(input_path)

    agg = df.groupby("coin").agg({
        "ret_log": "mean",            # retorno promedio
        "vol_rolling": "mean",        # volatilidad promedio
        "volumen_promedio": "mean",   # volumen promedio
        "drawdown": "min"             # drawdown más profundo (peor caída)
    })

    agg = agg.rename(columns={
        "ret_log": "ret_mean",
        "vol_rolling": "vol_mean",
        "volumen_promedio": "volume_mean",
        "drawdown": "dd_min"
    })

    return agg.reset_index()


def cluster_coins(df_agg, n_clusters=3):
    """
    Aplica K-means a los indicadores agregados.
    Devuelve el dataframe con etiquetas de clúster.
    """

    X = df_agg[["ret_mean", "vol_mean", "volume_mean", "dd_min"]]

    # Escalar (muy importante para K-means)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Modelo K-means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X_scaled)

    df_agg["cluster"] = labels
    return df_agg, kmeans, scaler

def compute_elbow_curve(df_agg, max_clusters=10):
    """
    Calcula la inercia para k = 1..max_clusters y devuelve una lista con los valores.
    Sirve para graficar el método del codo.
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    X = df_agg[["ret_mean", "vol_mean", "volume_mean", "dd_min"]]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    inertias = []

    for k in range(1, max_clusters + 1):
        model = KMeans(n_clusters=k, random_state=42)
        model.fit(X_scaled)
        inertias.append(model.inertia_)

    return inertias
