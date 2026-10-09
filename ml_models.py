# app/ml_models.py

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Drop rows with zero original price (to avoid division errors)
    df = df[df["Original Price"] > 0]

    # Ensure types are correct
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Original Price'] = pd.to_numeric(df['Original Price'], errors='coerce')
    df['Computed Discount %'] = pd.to_numeric(df['Computed Discount %'], errors='coerce')

    df = df.dropna(subset=['Price', 'Original Price', 'Computed Discount %'])
    return df


def perform_kmeans_clustering(df: pd.DataFrame, n_clusters: int = 3):
    features = df[['Price', 'Original Price', 'Computed Discount %']]

    # Normalize features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    cluster_labels = model.fit_predict(scaled_features)

    df = df.copy()
    df['Cluster'] = cluster_labels
    return df[['Price', 'Original Price', 'Computed Discount %', 'Brand', 'Cluster']]


def get_elbow_data(df: pd.DataFrame, max_k: int = 10):
    features = df[['Price', 'Original Price', 'Computed Discount %']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    inertias = []
    for k in range(1, max_k + 1):
        model = KMeans(n_clusters=k, random_state=42, n_init='auto')
        model.fit(scaled_features)
        inertias.append({'k': k, 'inertia': model.inertia_})
    return inertias
