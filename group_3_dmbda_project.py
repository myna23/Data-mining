# -*- coding: utf-8 -*-
"""Group 3 - DMBDA project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uVfPjcRcVX33eJ7lh09YxGdPVqwKZ3ZB

# DMBDA Project: Unsupervised and supervised mining
## Group No.3: 
___

#**Unsupervised mining**

# **Importing Library needed**
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.image as mpimg
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import cv2

import matplotlib.pyplot as plt
import seaborn as sn
from yellowbrick.cluster import KElbowVisualizer
from sklearn.metrics import silhouette_score,adjusted_rand_score
from scipy.cluster.hierarchy import linkage,dendrogram
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster import hierarchy

"""# **Data of cleaning**

> **Importation data**


> **Descriptive Statisatics**




"""

mfeat_mor = pd.read_table('http://archive.ics.uci.edu/ml/machine-learning-databases/mfeat/mfeat-mor',names=['mor'], sep='\n')

mfeat_mor = mfeat_mor.mor.str.split(expand=True)
mfeat_mor.head(2000)

mfeat_morf= mfeat_mor.astype(float) #convert the data to float
mfeat_morf.columns = ['mor'+str(i+1) for i in range(6)]
mfeat_morf

mfeat_morf.describe()

mfeat_mor.isnull().sum() #check the missig data

mfeat_pix = pd.read_csv("http://archive.ics.uci.edu/ml/machine-learning-databases/mfeat/mfeat-pix",sep = '\n',names=['pix'])

mfeat_pix = mfeat_pix.pix.str.split(expand=True)

mfeat_pixf= mfeat_pix.astype(float)#convert the data to float
mfeat_pixf.columns = ['pix'+str(i+1) for i in range(240)]
mfeat_pixf

mfeat_pix.mode()

mfeat_pix.isnull().sum()#checking for missing data

mfeat_fac = pd.read_csv("http://archive.ics.uci.edu/ml/machine-learning-databases/mfeat/mfeat-fac", sep = '\n', names= ['fac'])

mfeat_fac = mfeat_fac.fac.str.split(expand=True)

mfeat_fac.head(5)

mfeat_facf= mfeat_fac.astype(float) #convert data to float
mfeat_facf.columns = ['fac'+str(i+1) for i in range(216)]
mfeat_facf.describe()

mfeat_fou = pd.read_csv("http://archive.ics.uci.edu/ml/machine-learning-databases/mfeat/mfeat-fou",sep='\n',names=['fou'])

mfeat_fou=mfeat_fou.fou.str.split(expand=True)
mfeat_fou.shape

mfeat_fouf= mfeat_fou.astype(float)#convert the data to float
mfeat_fouf.columns = ['fou'+str(i+1) for i in range(76)]
mfeat_fouf.describe()

mfeat_kar = pd.read_csv("http://archive.ics.uci.edu/ml/machine-learning-databases/mfeat/mfeat-kar",sep='\n', names=['kar'])

mfeat_kar = mfeat_kar.kar.str.split(expand=True)
mfeat_kar.shape

mfeat_karf= mfeat_kar.astype(float)#convert the data to float
mfeat_karf.columns = ['kar'+str(i+1) for i in range(64)]
mfeat_karf.describe()

mfeat_zer = pd.read_csv('http://archive.ics.uci.edu/ml/machine-learning-databases/mfeat/mfeat-zer',sep='\n', names=['zer'])

mfeat_zer = mfeat_zer.zer.str.split(expand=True)
mfeat_zer.shape

mfeat_zerf= mfeat_zer.astype(float)#convert the data to float
mfeat_zerf.columns = ['zer'+str(i+1) for i in range(47)]
mfeat_zerf.describe()

"""# **Explorative Analysis**


> **Correlation matrix**


> **Principal Component Analysis**


> **K Means Clustering**






"""

plt.figure(figsize=(10,10)) #Correlation Matrix Mfeat-pix
covMatrix = mfeat_pixf.corr()
sn.heatmap(covMatrix,square=True)
plt.title('correlation matrix of mfeat-pix')
plt.show()

scaler =StandardScaler()#standardization of data
mfeat_pix_std = scaler.fit_transform(mfeat_pix)

model = PCA() #PCA for mfeat-pix
mfeat_pix_t=model.fit_transform(mfeat_pix_std)
mfeat_pix_t
mfeat_pix_tr = mfeat_pix_t[:,0:33]

feature =range(model.n_components_)
explained_variance = pd.DataFrame(model.explained_variance_, columns =['Explained_var'])
explained_var_ratio = pd.DataFrame(model.explained_variance_ratio_, columns =['Explained_var'])
variance_df = pd.concat([explained_variance,explained_var_ratio],axis=1, join='inner')
#variance_df.sort_values(by=['explained_var_ratio'],ascending= False, inplace=True)
variance_df.head(33)
variance_df[0:33].sum()

"""**From the above the number of component choosen is 33 with eigenvalue greater than 1.The 33 components explained 85.09% of the variance**"""

plt.figure(figsize = (8, 6))
plt.bar(feature,model.explained_variance_, alpha=0.5)
plt.ylabel('Explained variance ratio')
plt.xlabel('Ranked Principal Components')
plt.title("Scree Graph for Mfeat-pix Components")
plt.show()

fig = plt.figure(figsize=(6,4))#plot for cummulative explained variance
plt.plot(np.cumsum(model.explained_variance_ratio_))
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative explained variance')
plt.title('Explained Variance for Mfeat-pix')
plt.show()

from sklearn.cluster import KMeans

model15 =KMeans()
elbow1 = KElbowVisualizer(model15,k=(1,15)).fit(mfeat_pix_tr)
elbow1.show()

model1 = KMeans(n_clusters=5,random_state = 42, max_iter=300, n_init=10)#KMean model for Mfeat-pix
cluster1= model1.fit_predict(mfeat_pix_tr)
model1.labels_

centroids = model1.cluster_centers_
model1.inertia_

silhouette_score(mfeat_pix_tr,model1.labels_,metric = 'euclidean')

LABEL_COLOR_MAP = {0 : 'r',1 : 'g',2 : 'b',3:'c',4:'k',5:'m'}
label_color = [LABEL_COLOR_MAP[l] for l in cluster1]

# Plot the scatter digram
plt.figure(figsize = (7,7))
plt.scatter(mfeat_pix_tr[:,0],mfeat_pix_tr[:,2], c= label_color, alpha=1)
plt.show()

df = pd.DataFrame(mfeat_pix_tr)
df = df[[0,1,2]] # only want to visualise relationships between first 5 projections
df['cluster1'] = cluster1

sn.pairplot(df, hue='cluster1', palette= 'Dark2', diag_kind='kde',size=1.85)

model1.cluster_centers_

m = pd.DataFrame(model1.cluster_centers_, columns= ['ccol'+str(i) for i in range(33)])
m['cluster mean']=m.mean(axis=1)
m

"""**Mfeat_mor BLOCK PCA AND CLUSTERING**"""

mfeat_mor.shape

plt.figure(figsize=(10,10))
covMatrix = mfeat_morf.corr()
sn.heatmap(covMatrix,square=True)
plt.title('Correlation matrix for Mfeat-mor')
plt.show()

scaler =StandardScaler()
mfeat_mor_std = scaler.fit_transform(mfeat_mor)
model_mor = PCA()
mfeat_mor_t=model_mor.fit_transform(mfeat_mor_std)
mfeat_mor_t
mfeat_mor_tr = mfeat_mor_t[:,0:2]

feature_mor =range(model_mor.n_components_)
explained_variance_mor = pd.DataFrame(model_mor.explained_variance_, columns =['Explained_var'])
explained_var_ratio_mor = pd.DataFrame(model_mor.explained_variance_ratio_, columns =['Explained_var'])
variance_df_mor = pd.concat([explained_variance_mor,explained_var_ratio_mor],axis=1, join='inner')
#variance_df.sort_values(by=['explained_var_ratio'],ascending= False, inplace=True)
variance_df_mor.head(2)
variance_df_mor[0:2].sum()

plt.figure(figsize = (8, 6))
plt.bar(feature_mor,model_mor.explained_variance_, alpha=0.5)
plt.ylabel('Explained variance ratio')
plt.xlabel('Ranked Principal Components')
plt.title("Scree Graph for mfeat_mor")
plt.show()

fig = plt.figure(figsize=(6,4))
plt.plot(np.cumsum(model_mor.explained_variance_ratio_))
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative explained variance')
plt.title('Explained Variance Mfeat-mor')
plt.show()

#Determining the best value of K to use using KElbow plot
model15 =KMeans()
elbow2 = KElbowVisualizer(model15,k=(1,15)).fit(mfeat_mor_tr)
elbow2.show()

#KMean model
model2 = KMeans(n_clusters=4,random_state = 42, max_iter=100, n_init=10)
cluster1= model2.fit_predict(mfeat_mor_tr)
model2.labels_

xcentroids = model2.cluster_centers_
model2.inertia_

silhouette_score(mfeat_mor_tr,model2.labels_ )#cheking the level of how dense is the cluster

LABEL_COLOR_MAP2 = {0 : 'r',1 : 'g',2 : 'b',3:'y'}
label_color2 = [LABEL_COLOR_MAP2[l] for l in cluster1]

# Plot the scatter digram
plt.figure(figsize = (7,7))
plt.scatter(mfeat_mor_tr[:,0],mfeat_mor_tr[:,1], c= label_color2, alpha=0.5)
plt.title('Scatter plot for clusters for Mfeat-mor')
plt.show()

df1 = pd.DataFrame(mfeat_mor_tr)
df1 = df1[[0,1]] # only want to visualise relationships between first projections
df1['cluster1'] = cluster1
sn.pairplot(df, hue='cluster1', palette= 'Dark2', diag_kind='kde',size=1.85)

mfeat_mor_h = hierarchy.linkage(mfeat_mor_tr, method ='complete')
plt.figure()
dn_mor = hierarchy.dendrogram(mfeat_mor_h,truncate_mode = 'lastp')

import scipy.cluster.hierarchy as shc

plt.figure(figsize=(10, 7))
plt.title("Mfeat_mor Dendograms")
dend = shc.dendrogram(shc.linkage(mfeat_mor_tr, method='ward'))

"""## **Mfeat-fac PCA and clustering**"""

mfeat_fac.shape

plt.figure(figsize=(10,10))
covMatrix = mfeat_facf.corr()
sn.heatmap(covMatrix,square=True)
plt.title('Correlation matrix plot fo for Mfeat-fac')
plt.show()

scaler =StandardScaler()#Data standardization
mfeat_fac_std = scaler.fit_transform(mfeat_fac)
model_fac = PCA()
mfeat_fac_t=model_fac.fit_transform(mfeat_fac_std)
mfeat_fac_tr = mfeat_fac_t[:,0:23]
mfeat_fac_tr

feature_fac =range(model_fac.n_components_)
explained_variance_fac = pd.DataFrame(model_fac.explained_variance_, columns =['Explained_var'])
explained_var_ratio_fac = pd.DataFrame(model_fac.explained_variance_ratio_, columns =['Explained_var'])
variance_df_fac = pd.concat([explained_variance_fac,explained_var_ratio_fac],axis=1, join='inner')
#variance_df.sort_values(by=['explained_var_ratio'],ascending= False, inplace=True)
variance_df_fac.head(23)
variance_df_fac[0:23].sum()

plt.figure(figsize = (8, 6))
plt.bar(feature_fac,model_fac.explained_variance_, alpha=0.5)
plt.ylabel('Explained variance ratio')
plt.xlabel('Ranked Principal Components')
plt.title("Scree plot for mfeat-fac")
plt.show()

fig = plt.figure(figsize=(6,4))
plt.plot(np.cumsum(model_fac.explained_variance_ratio_))
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative explained variance')
plt.title('Explained Variance Mfeat-fac')
plt.show()

model14 =KMeans()
elbow3 = KElbowVisualizer(model14,k=(1,15)).fit(mfeat_fac_tr)
elbow3.show()

model3 = KMeans(n_clusters=4,random_state = 42, max_iter=300, n_init=10)
cluster3= model3.fit_predict(mfeat_fac_tr)
model3.labels_

model3.inertia_

centroids3 = model3.cluster_centers_
model3.inertia_
silhouette_score(mfeat_fac_tr,model3.labels_ )

LABEL_COLOR_MAP3 = {0 : 'r',1 : 'g',2 : 'b',3:'y',4:'m'}
label_color3 = [LABEL_COLOR_MAP3[l] for l in cluster3]

# Plot the scatter digram
plt.figure(figsize = (7,7))
plt.scatter(mfeat_fac_tr[:,0],mfeat_fac_tr[:,2], c= label_color3, alpha=1)
plt.title('Cluster plot for Mfeat-fac')
plt.show()

df2 = pd.DataFrame(mfeat_fac_tr)
df2 = df2[[0,1,2,3]] # only want to visualise relationships between first projections
df2['cluster3'] = cluster3
sn.pairplot(df2, hue='cluster3', palette= 'Dark2', diag_kind='kde',size=1.85)

mfeat_fac_h = hierarchy.linkage(mfeat_fac_tr, 'complete')
plt.figure()
dn_fac = hierarchy.dendrogram(mfeat_fac_h)

"""# **Mfeat-fou PCA and clustering**"""

mfeat_fou.shape

plt.figure(figsize=(10,10))
covMatrix = mfeat_fouf.corr()
sn.heatmap(covMatrix,square=True)
plt.title('correlation matrix of mfeat-fou')
plt.show()

"""**The mfeat_fou data was standardized and the principal components components was calculated**"""

scaler =StandardScaler()
mfeat_fou_std = scaler.fit_transform(mfeat_fou)
model_fou = PCA()
mfeat_fou_t=model_fou.fit_transform(mfeat_fou_std)
mfeat_fou_tr = mfeat_fou_t[:,0:20]
mfeat_fou_tr

feature_fou =range(model_fou.n_components_)
explained_variance_fou = pd.DataFrame(model_fou.explained_variance_, columns =['Explained_var'])
explained_var_ratio_fou = pd.DataFrame(model_fou.explained_variance_ratio_, columns =['Explained_var'])
variance_df_fou = pd.concat([explained_variance_fou,explained_var_ratio_fou],axis=1, join='inner')
#variance_df.sort_values(by=['explained_var_ratio'],ascending= False, inplace=True)
variance_df_fou.head(20).sum ,    variance_df_fou[:20].sum()

"""From the above table, we see that the number of eigenvalues greater than 1 is 20 (by kaiser rule). That means our data was reduced to 20 components. Clustering will be performed on the 20 components to further examine the partern in the data. """

plt.figure(figsize = (8, 6))
plt.bar(feature_fou,model_fou.explained_variance_, alpha=0.5)
plt.ylabel('Explained variance ratio')
plt.xlabel('Ranked Principal Components')
plt.title("Scree Graph for mfeat-fou")
plt.show()

"""The principal components plot """

fig = plt.figure(figsize=(6,4))
plt.plot(np.cumsum(model_fou.explained_variance_ratio_))
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative explained variance')
plt.title('Explained Variance Mfeat-fou')
plt.show()

model13 =KMeans()
elbow4 = KElbowVisualizer(model13,k=(1,15)).fit(mfeat_fou_tr)
elbow4.show()

model4 = KMeans(n_clusters=2,random_state = 42, max_iter=300, n_init=10)
cluster4= model4.fit_predict(mfeat_fou_tr)
model4.labels_

centroids4 = model4.cluster_centers_
model4.inertia_
silhouette_score(mfeat_fou_tr,model4.labels_ )

centroids4

LABEL_COLOR_MAP4 = {0 : 'r',1 : 'g',2:'b',3:'y',4:'m',5:'c',6:'k'}
label_color4 = [LABEL_COLOR_MAP4[l] for l in cluster4]

# Plot the scatter digram
plt.figure(figsize = (7,7))
plt.scatter(mfeat_fou_tr[:,0],mfeat_fou_tr[:,2], c= label_color4, alpha=1)
plt.title('Cluster plot for Mfeat-fou')
plt.show()

df3 = pd.DataFrame(mfeat_fou_tr)
df3 = df3[[0,1,2,3]] # only want to visualise relationships between first projections
df3['cluster4'] = cluster4
sn.pairplot(df3, hue='cluster4', palette= 'Dark2', diag_kind='kde',size=1.85)



mfeat_fou_h = hierarchy.linkage(mfeat_fou_tr, 'complete')
plt.figure()
dn_fou = hierarchy.dendrogram(mfeat_fou_h)

"""#**Mfeat_kar PCA AND CLUSTER**"""

mfeat_kar.shape

plt.figure(figsize=(10,10))
covMatrix = mfeat_karf.corr()
sn.heatmap(covMatrix,square=True)
plt.title('correlation matrix of mfeat-kar')
plt.show()

scaler =StandardScaler()
mfeat_kar_std = scaler.fit_transform(mfeat_kar)
model_kar = PCA()
mfeat_kar_t=model_kar.fit_transform(mfeat_kar_std)
mfeat_kar_tr = mfeat_kar_t[:,0:21]
mfeat_kar_tr

feature_kar =range(model_kar.n_components_)
explained_variance_kar = pd.DataFrame(model_kar.explained_variance_, columns =['Explained_var'])
explained_var_ratio_kar = pd.DataFrame(model_kar.explained_variance_ratio_, columns =['Explained_var'])
variance_df_kar = pd.concat([explained_variance_kar,explained_var_ratio_kar],axis=1, join='inner')
#variance_df.sort_values(by=['explained_var_ratio'],ascending= False, inplace=True)
variance_df_kar.head(21)
variance_df_kar[:20].sum()

plt.figure(figsize = (8, 6))
plt.bar(feature_kar,model_kar.explained_variance_, alpha=0.5)
plt.ylabel('Explained variance ratio')
plt.xlabel('Ranked Principal Components')
plt.title("Scree Graph for mfeat-kar")
plt.show()

fig = plt.figure(figsize=(6,4))
plt.plot(np.cumsum(model_kar.explained_variance_ratio_))
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative explained variance')
plt.title('Explained Variance Mfeat-fou')
plt.show()

model12 =KMeans()
elbow5 = KElbowVisualizer(model12,k=(1,15)).fit(mfeat_kar_tr)
elbow5.show()

model5 = KMeans(n_clusters=6,random_state = 42, max_iter=300, n_init=10)
cluster5= model5.fit_predict(mfeat_kar_tr)
model5.labels_

centroids5 = model5.cluster_centers_
model5.inertia_
silhouette_score(mfeat_kar_tr,model5.labels_ )

LABEL_COLOR_MAP5 = {0 : 'r',1 : 'g',2:'b',3:'y',4:'m',5:'c',6:'k'}
label_color5 = [LABEL_COLOR_MAP5[l] for l in cluster5]

# Plot the scatter digram
plt.figure(figsize = (7,7))
plt.scatter(mfeat_kar_tr[:,0],mfeat_kar_tr[:,2], c= label_color5, alpha=1) 
plt.show()

df3 = pd.DataFrame(mfeat_fac_tr)
df3 = df3[[0,1,2,3]] # only want to visualise relationships between first projections
df3['cluster5'] = cluster5
sn.pairplot(df3, hue='cluster5', palette= 'Dark2', diag_kind='kde',size=1.85)

mfeat_kar_h = hierarchy.linkage(mfeat_kar_tr, 'complete')
plt.figure(figsize=(10,10))
dn_kar = hierarchy.dendrogram(mfeat_kar_h)

"""## **mfeat_zer PCA AND CLUSTERING**"""

mfeat_zer.shape

plt.figure(figsize=(10,10))
covMatrix = mfeat_zerf.corr()
sn.heatmap(covMatrix,square=True)
plt.title('correlation matrix of mfeat-zer')
plt.show()

scaler =StandardScaler()
mfeat_zer_std = scaler.fit_transform(mfeat_zer)
model_zer = PCA()
mfeat_zer_t=model_zer.fit_transform(mfeat_zer_std)
mfeat_zer_tr = mfeat_zer_t[:,0:11]
mfeat_zer_tr

feature_zer =range(model_zer.n_components_)
explained_variance_zer = pd.DataFrame(model_zer.explained_variance_, columns =['Explained_var'])
explained_var_ratio_zer = pd.DataFrame(model_zer.explained_variance_ratio_, columns =['Explained_var'])
variance_df_zer = pd.concat([explained_variance_zer,explained_var_ratio_zer],axis=1, join='inner')
#variance_df.sort_values(by=['explained_var_ratio'],ascending= False, inplace=True)
variance_df_zer.head(11)
variance_df_zer[:11].sum()

plt.figure(figsize = (8, 6))
plt.bar(feature_zer,model_zer.explained_variance_, alpha=0.5)
plt.ylabel('Explained variance ratio')
plt.xlabel('Ranked Principal Components')
plt.title("Scree Graph for mfeat-kar")
plt.show()

fig = plt.figure(figsize=(6,4))
plt.plot(np.cumsum(model_zer.explained_variance_ratio_))
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative explained variance')
plt.title('Explained Variance Mfeat-zer')
plt.show()

model11 =KMeans()
elbow6 = KElbowVisualizer(model11,k=(1,15)).fit(mfeat_zer_tr)
elbow6.show()

model6 = KMeans(n_clusters=6,random_state = 42, max_iter=1000, n_init=20)
cluster6= model6.fit_predict(mfeat_zer_tr)
model6.labels_

centroids6 = model6.cluster_centers_
model6.inertia_
silhouette_score(mfeat_zer_tr,model6.labels_ )

LABEL_COLOR_MAP6 = {0 : 'r',1 : 'g',2:'b',3:'y',4:'m',5:'c',6:'k'}
label_color6 = [LABEL_COLOR_MAP6[l] for l in cluster6]

# Plot the scatter digram
plt.figure(figsize = (7,7))
plt.scatter(mfeat_zer_tr[:,0],mfeat_zer_tr[:,2], c= label_color6, alpha=1) 
plt.show()

mfeat_zer_h = hierarchy.linkage(mfeat_zer_tr, 'complete')
plt.figure(figsize=(10,10))
dn_zer = hierarchy.dendrogram(mfeat_zer_h)



"""### **COMBINED DATA PCA AND CLUSTERING**"""

mfeat = pd.concat([mfeat_mor,mfeat_fac,mfeat_fou,mfeat_kar,mfeat_pix,mfeat_zer],axis=1, join='inner') #The 6 blocks were joined to form the whole data

mfeat_f= mfeat.astype(float) #convert the combined data to float

plt.figure(figsize=(10,10))
covMatrix = mfeat_f.corr()
sn.heatmap(covMatrix,square=True)
plt.title('correlation matrix of Mfeat')
plt.show()

mfeat.shape

"""**The combined value was standardized to put all the variable in the same scale of variance and the principal components were fitted**"""

scaler =StandardScaler()
mfeat_std = scaler.fit_transform(mfeat)
model_c = PCA()
mfeat_tr=model_c.fit_transform(mfeat_std)
mfeat_tr

feature_c =range(model_c.n_components_)  #we determine the number of components to choose 
explained_variance_c = pd.DataFrame(model_c.explained_variance_, columns =['Explained_var'])
explained_var_ratio_c = pd.DataFrame(model_c.explained_variance_ratio_, columns =['Explained_var'])
variance_df_c = pd.concat([explained_variance_c,explained_var_ratio_c],axis=1, join='inner')
#variance_df.sort_values(by=['explained_var_ratio'],ascending= False, inplace=True)
variance_df_c.head(77)
variance_df_c[:77].sum()

"""From the above table, we see that the number of eigenvalues greater than 1 is 77 (by kaiser rule). That means our data was reduced to 77 components. Clustering will be performed on the 77 components to further examine the partern in the data.The 77 components explained 87.9% of the total variance"""



mfeat_cc =variance_df_c.iloc[0:77] #creating new variable with 77 components
mfeat_cc

"""**Components Plot**"""

plt.figure(figsize = (8, 6))
plt.bar(feature_c,model_c.explained_variance_, alpha=0.5)
plt.ylabel('Explained variance ratio')
plt.xlabel('Ranked Principal Components')
plt.title("Scree Graph for mfeat-kar")
plt.show()

fig = plt.figure(figsize=(6,4)) #Cumulative Explained variace plot
plt.plot(np.cumsum(model_c.explained_variance_ratio_))
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative explained variance')
plt.title('Explained Variance Mfeat')
plt.show()

"""**The number of clusters for the Kmean of the combined data was determined using the Elbow plot and 5 was choosing as seen below in the plot.**"""

model =KMeans()
elbow7 = KElbowVisualizer(model,k=(1,15)).fit(mfeat_tr)
elbow7.show()

model7 = KMeans(n_clusters=5,random_state = 42, max_iter=1000, n_init=20)
cluster7= model7.fit_predict(mfeat_tr)
model7.labels_

"""The Kmean model was used to cluster the combined data by specifiying 5 clusters as determined by the Elbow plot above"""

centroids7 = model7.cluster_centers_
model7.inertia_
silhouette_score(mfeat_tr,model7.labels_ )

LABEL_COLOR_MAP7 = {0 : 'r',1 : 'g',2:'b',3:'y',4:'m',5:'c',6:'k'}
label_color7 = [LABEL_COLOR_MAP7[l] for l in cluster7]

# Plot the scatter digram for the clusters
plt.figure(figsize = (7,7))
plt.scatter(mfeat_tr[:,0],mfeat_tr[:,2], c= label_color7, alpha=0.5) 
plt.show()

df7 = pd.DataFrame(mfeat_tr)
df7 = df7[[0,1,2,3,4]] # only want to visualise relationships between first projections
df7['cluster7'] = cluster7
sn.pairplot(df7, hue='cluster7', palette= 'Dark2', diag_kind='kde',size=1.85)

mfeat_c_h = hierarchy.linkage(mfeat_tr, 'complete')
plt.figure(figsize=(10,10))
dn_c = hierarchy.dendrogram(mfeat_c_h,leaf_font_size=3)

"""## Supervised mining"""

mfeat_t = mfeat_tr[:,0:77]

from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report
from sklearn.model_selection import cross_val_score

C1=['0' for j in range(200) ]
C2=['1' for j in range(200) ]
C3=['2' for j in range(200) ]
C4=['3' for j in range(200) ]
C5=['4' for j in range(200) ]
C6=['5' for j in range(200) ]
C7=['6' for j in range(200) ]
C8=['7' for j in range(200) ]
C9=['8' for j in range(200) ]
C10=['9' for j in range(200)]
        
Y=np.array(C1 + C2+C3 +C4+C5+C6+C7+C8+C9+C10)

mfeat_train,mfeat_test,y_train,y_test = train_test_split(mfeat,Y,test_size=0.2,random_state=42)

"""# **Linear Discriminant Analysis**"""

clf = LinearDiscriminantAnalysis()
clf.fit(mfeat_train,y_train)
y_clf_pred = clf.predict(mfeat_test)

print('Prediction accuracy for the test Linear Discriminant Analysis model')
print('{:.2%}'.format(accuracy_score(y_test,y_clf_pred)))

print('Confusion Matrix of the LDA-classifier')
print(confusion_matrix(y_test, y_clf_pred))
print('Classification report LDA-classifier')
print(classification_report(y_test,y_clf_pred))

"""**The linear discriminant Analysis model gave us an accuracy of 98%, recall of 98% nad precision of 98%.**

# **K-Nearest Neighbors (KNN)**
"""

KNN = KNeighborsClassifier(n_neighbors=7,algorithm='ball_tree')
KNN.fit(mfeat_train, y_train)
y_pred_KNN =KNN.predict(mfeat_test)

print('Prediction accuracy for K-Nearest Neighbors (KNN)')
print('{:.2%}\n'.format(accuracy_score(y_test, y_pred_KNN)))

print('Confusion Matrix of K-Nearest Neighbors (KNN)')
print(confusion_matrix(y_test,y_pred_KNN))

print('Classification report K-Nearest Neighbors (KNN)')
print(classification_report(y_test,y_pred_KNN))

"""**The K-Nearest Neighbor model gave us an accuracy of 94%, recall of 94% nad precision of 94%**

# **Classification Task with Random Forest Classifier**
"""

RFC = RandomForestClassifier(n_estimators=100, max_depth=100,min_samples_split=2, random_state=42)
RFC.fit(mfeat_train,y_train)
RFC_pred = RFC.predict(mfeat_test)

print('Prediction accuracy for Random Forest Classifier')
print('{:.2%}\n'.format(accuracy_score(y_test, RFC_pred)))

print('Confusion Matrix for Random Forest Classifier')
print(confusion_matrix(y_test,RFC_pred))

print('Classification report for Random Forest Classifier')
print(classification_report(y_test,RFC_pred))

"""**Random forest classifier model gave us an accuracy of 98%, recall of 98% nad precision of 98%**

# **Classification Task with Decision Tree**
"""

DTC=DecisionTreeClassifier(max_depth=30)
DTC.fit(mfeat_train,y_train)
DTC_pred = DTC.predict(mfeat_test)

print('Prediction accuracy for Decision Tree')
print('{:.2%}\n'.format(accuracy_score(y_test, DTC_pred)))

print('Confusion Matrix for Decision Tree')
print(confusion_matrix(y_test,DTC_pred))

print('Classification report for Decision Tree')
print(classification_report(y_test,DTC_pred))

"""**The Decision tree model gave us an accuracy of 93%, recall of 93% nad precision of 93%**"""

from sklearn.model_selection import cross_val_predict
clf = RandomForestClassifier(n_estimators=100, max_depth=100,min_samples_split=2, random_state=42)
scores = cross_val_predict(clf, mfeat_train, y_train, cv=5)
scores

"""# **Support Vector Machine(SVM)**"""



svm1=SVC(kernel="linear", C=0.025).fit(mfeat_train,y_train)
svm1_pred=svm1.predict(mfeat_test)

print('Prediction accuracy for Support Vector Machine(SVM)')
print('{:.2%}\n'.format(accuracy_score(y_test, svm1_pred)))

print('Confusion Matrix for Support Vector Machine(SVM)')
print(confusion_matrix(y_test,svm1_pred))

print('Classification report for Support Vector Machine(SVM)')
print(classification_report(y_test,svm1_pred))

"""**The support vector machine Analysis model gave us an accuracy of 97%, recall of 97% nad precision of 97%**"""