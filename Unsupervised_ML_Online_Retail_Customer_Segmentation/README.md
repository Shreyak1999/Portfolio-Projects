# 🛒 Customer Segmentation on Online Retail Dataset

## 📌 Project Overview
This project applies **unsupervised learning (clustering)** to segment customers of a UK-based online retail store into meaningful groups.  
The goal is to identify distinct customer profiles based on their **purchasing behavior** so businesses can tailor marketing strategies, improve customer retention, and optimize resource allocation.

---

## 🛠️ Tech Stack
- Python (pandas, numpy, scikit-learn)  
- Visualization (matplotlib, seaborn, plotly)  
- Clustering (KMeans, DBSCAN, Hierarchical)  

---

## 📊 Dataset
- Source: [UCI Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/online+retail)  
- Transactions from **Dec 2010 – Dec 2011** (~540,000 rows).  
- Features include:  
  - `InvoiceNo`: Transaction ID  
  - `StockCode`: Product ID  
  - `Description`: Product name  
  - `Quantity`: Units purchased  
  - `InvoiceDate`: Date of purchase  
  - `UnitPrice`: Price per item  
  - `CustomerID`: Unique customer identifier  
  - `Country`: Customer’s country  

---

## 🔧 Methodology
1. **Data Cleaning**  
   - Removed missing Customer IDs  
   - Removed negative quantities (returns)  
   - Created `TotalPrice = Quantity × UnitPrice`

2. **Feature Engineering (RFM Analysis)**  
   - **Recency (R):** Days since last purchase  
   - **Frequency (F):** Number of unique transactions  
   - **Monetary (M):** Total spending  

3. **Preprocessing**  
   - Log transformation of Monetary  
   - StandardScaler applied to R, F, M  

4. **Clustering**  
   - KMeans with Elbow method & Silhouette Score to determine `k`  
   - Compared alternative algorithms (DBSCAN, Hierarchical)  

5. **Visualization & Insights**  
   - Pairplots of clusters  
   - PCA/t-SNE for dimensionality reduction  

---

## 📈 Results
- Optimal number of clusters: **4**  
- Cluster summaries:  

| Cluster | Recency (days) | Frequency | Monetary (£, log-scale) | Interpretation |
|---------|----------------|-----------|--------------------------|----------------|
| 0       | High           | Low       | Low                      | At-risk customers |
| 1       | Low            | High      | High                     | Loyal, high-value customers |
| 2       | Medium         | Medium    | Medium                   | Regular shoppers |
| 3       | High           | Low       | Medium                   | Price-sensitive, inactive |

- **Silhouette Score:** ~0.3 (moderate separation)

---

## 📊 Visualizations
- Elbow Method for optimal clusters  
- Pairplot of RFM features colored by cluster  
- PCA 2D visualization of clusters  

---

## 📂 Repository Structure

│── Data 

    |- Online Retail.xlsx

│notebook.ipynb

│── README.md

│── requirements.txt
