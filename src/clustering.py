from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.preprocessing import StandardScaler, OneHotEncoder, RobustScaler
from sklearn.cluster import MiniBatchKMeans

def run_kmeans(X_proc, k_values=range(2, 11)):

    sils = []
    models = []
    for k in k_values:
        km = MiniBatchKMeans(n_clusters=k, batch_size=1024, random_state=42)
        labels = km.fit_predict(X_proc)
        score = silhouette_score(X_proc, labels, sample_size=min(10000, X_proc.shape[0]), random_state=42)
        sils.append(score)
        models.append((km, labels))
    idx = int(np.argmax(sils))
    best_model, best_labels = models[idx]
    return best_labels, k_values[idx], sils[idx], best_model

def run_hierarchical_select_k(df_work, features, k=4, k_values=range(2, 11)):

    scaler = RobustScaler()
    X_scaled = scaler.fit_transform(df_work[features])


    Z = linkage(X_scaled, method="ward", metric="euclidean")


    if k is not None:
        labels = fcluster(Z, t=k, criterion="maxclust")
        if len(np.unique(labels)) >= 2:
            score = silhouette_score(X_scaled, labels)
        else:
            score = -1  # Caso degenerado (apenas 1 cluster)
        return labels, k, score, Z, X_scaled

    best_k, best_score, best_labels = None, -1, None
    for k in k_values:
        labels = fcluster(Z, t=k, criterion="maxclust")

        if len(np.unique(labels)) >= 2 and len(np.unique(labels)) < len(labels):
            score = silhouette_score(X_scaled, labels)
            if score > best_score:
                best_k, best_score, best_labels = k, score, labels

    return best_labels, best_k, best_score, Z, X_scaled