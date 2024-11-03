import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

data = pd.read_csv('result.csv')
data['Min'] = data['Min'].str.replace(',', '').astype(int)
numeric_data = data.select_dtypes(include=['float64', 'int64'])
numeric_data = numeric_data.fillna(numeric_data.mean())

scaler = StandardScaler()
scaled_features = scaler.fit_transform(numeric_data)

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(scaled_features)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.xlabel('Số lượng cụm')
plt.ylabel('WCSS')
plt.title('Phương pháp Elbow để xác định số lượng cụm tối ưu')
plt.show()

optimal_clusters = 10
kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
clusters = kmeans.fit_predict(scaled_features)

data['Cluster'] = clusters
print(data[['Player', 'Cluster'] + numeric_data.columns.tolist()])

pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_features)

pca_df = pd.DataFrame(data=pca_result, columns=['PCA1', 'PCA2'])
pca_df['Cluster'] = clusters

plt.figure(figsize=(10, 6))
for i in range(optimal_clusters):
    plt.scatter(pca_df[pca_df['Cluster'] == i]['PCA1'],
                pca_df[pca_df['Cluster'] == i]['PCA2'],
                label=f'Cluster {i}')

plt.title('Phân cụm dữ liệu sử dụng PCA')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend()
plt.grid()
plt.show()