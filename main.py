from src.fetch_data import fetch_and_save_all
from src.transform import transform_raw_to_features
from src.clustering import build_features_per_coin, cluster_coins
from src.classification import build_supervised_dataset

if __name__ == "__main__":

    # 1. Descargar datos
    fetch_and_save_all()

    # 2. Procesar datos y calcular indicadores
    transform_raw_to_features()

    # 3. Construir dataset agregado por moneda (para clustering)
    agg = build_features_per_coin()
    df_clusters, model, scaler = cluster_coins(agg, n_clusters=3)
    df_clusters.to_csv("data/processed/crypto_clusters.csv", index=False)
    print("Clustering completado.")

    # 4. Construir dataset supervisado para el modelo predictivo
    build_supervised_dataset(
        input_path="data/processed/prices_features.csv",
        output_path="data/processed/supervised_dataset.csv",
        horizon=45
    )
