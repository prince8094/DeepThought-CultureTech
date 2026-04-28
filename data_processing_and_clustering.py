import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

def clean_and_cluster_companies(raw_data_path):
    """
    Ingests raw scraped company data and applies K-Means clustering 
    to filter out commodity businesses from specialty manufacturers.
    """
    df = pd.read_csv(raw_data_path)
    
    # Drop rows without product descriptions
    df = df.dropna(subset=['product_description_scraped'])
    
    # Text Vectorization
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['product_description_scraped'])
    
    # K-Means Clustering (Assuming 2 main clusters: Commodity/Services vs. Specialty Mfg)
    kmeans = KMeans(n_clusters=2, random_state=42)
    df['cluster_id'] = kmeans.fit_predict(X)
    
    # Identify the 'Specialty' cluster by checking for high-value keywords in cluster centers
    terms = vectorizer.get_feature_names_out()
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    
    specialty_cluster = None
    target_keywords = ['synthesis', 'recombinant', 'proprietary', 'precision', 'aerospace', 'custom']
    
    for i in range(2):
        top_terms = [terms[ind] for ind in order_centroids[i, :15]]
        if any(keyword in top_terms for keyword in target_keywords):
            specialty_cluster = i
            break
            
    # Filter dataset
    if specialty_cluster is not None:
        filtered_df = df[df['cluster_id'] == specialty_cluster].copy()
        
        # Hard exclusion rules (Auto-Fails)
        exclusions = 'trader|distributor|dealer|subsidiary|group company|cro|testing lab'
        filtered_df = filtered_df[~filtered_df['about_us_scraped'].str.contains(exclusions, case=False, na=False)]
        
        filtered_df.to_csv('cleaned_specialty_candidates.csv', index=False)
        print(f"Pre-filtering complete. {len(filtered_df)} high-probability targets ready for LLM scoring.")
    else:
        print("Failed to isolate specialty cluster.")

if __name__ == "__main__":
    # Example execution
    # clean_and_cluster_companies('raw_scraped_universe.csv')
    pass
