import streamlit as st
import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import ast  # Placeholder for AST analysis

# --- App Header ---
st.title("🔍HackerRank Plagiarism Checker")
st.markdown("Dual-mode: Upload Code OR View Simulated Contest Use Case")

# --- Mode Switcher ---
mode = st.selectbox("Choose Mode", ["Upload Code File", "Simulated Contest Data"])

# --- Enhanced Similarity Functions ---
def tfidf_similarity(codes):
    """Compute TF-IDF cosine similarity."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(codes)
    return cosine_similarity(tfidf_matrix)

def ngram_similarity(code1, code2, n=3):
    """Compute n-gram similarity between two code snippets."""
    ngrams1 = [code1[i:i+n] for i in range(len(code1)-n+1)]
    ngrams2 = [code2[i:i+n] for i in range(len(code2)-n+1)]
    matches = sum(1 for ngram in ngrams1 if ngram in ngrams2)
    return matches / max(len(ngrams1), len(ngrams2))

def combined_similarity(codes):
    """Combine TF-IDF and n-gram similarity into a single matrix."""
    n = len(codes)
    tfidf_sim_matrix = tfidf_similarity(codes)
    combined_sim_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i, n):
            ng_sim = ngram_similarity(codes[i], codes[j])
            combined_sim_matrix[i][j] = (tfidf_sim_matrix[i][j] + ng_sim) / 2
            combined_sim_matrix[j][i] = combined_sim_matrix[i][j]
    
    return combined_sim_matrix

def detect_plagiarism(sim_matrix, labels, threshold=0.85):
    """Detect pairs with similarity above the threshold."""
    flagged = []
    n = len(labels)
    for i in range(n):
        for j in range(i + 1, n):
            if sim_matrix[i][j] >= threshold:
                flagged.append((labels[i], labels[j], sim_matrix[i][j]))
    return flagged

def show_heatmap(sim_matrix, labels):
    """Display heatmap of the similarity matrix."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(sim_matrix, xticklabels=labels, yticklabels=labels, cmap='YlOrRd', annot=True, fmt=".2f", linewidths=.5, ax=ax)
    st.pyplot(fig)

# --- Similarity Threshold ---
threshold = st.slider("🔧 Set Similarity Threshold", min_value=0.5, max_value=1.0, value=0.85, step=0.01)

# =====================
# 1️⃣ Upload Code File
# =====================
if mode == "Upload Code File":
    uploaded_files = st.file_uploader("Upload code files", accept_multiple_files=True, type=["py", "txt", "cpp", "java"])
    
    if uploaded_files and len(uploaded_files) > 1:
        filenames = []
        codes = []
        
        for file in uploaded_files:
            code = file.read().decode("utf-8")
            filenames.append(file.name)
            codes.append(code)
        
        st.success("Files uploaded successfully. Now comparing...")
        
        # Compute combined similarity matrix
        sim_matrix = combined_similarity(codes)
        
        # Display similarity matrix
        df = pd.DataFrame(sim_matrix, index=filenames, columns=filenames)
        st.subheader("🔬 Combined Similarity Matrix")
        st.dataframe(df.style.background_gradient(cmap='YlOrRd'))
        
        # Display heatmap
        st.subheader("📊 Heatmap View")
        show_heatmap(sim_matrix, filenames)
        
        # Detect plagiarism
        plagiarized_pairs = detect_plagiarism(sim_matrix, filenames, threshold)
        
        if plagiarized_pairs:
            st.subheader("🚨 Potential Plagiarism Detected")
            for u1, u2, score in plagiarized_pairs:
                st.markdown(f"**{u1}** and **{u2}** → Similarity: `{score:.2f}` ❗")
        else:
            st.success("🎉 No high similarity detected. No plagiarism suspected.")
        
        # Download similarity matrix
        csv = df.to_csv()
        st.download_button("Download Similarity Matrix", csv, "upload_similarity.csv", "text/csv")
    
    elif uploaded_files:
        st.warning("Please upload **at least 2** code files to compare.")

# ===============================
# 2️⃣ Simulated Contest Data
# ===============================
elif mode == "Simulated Contest Data":
    st.info("Fetching mock submissions from FastAPI backend...")
    
    response = requests.get("http://127.0.0.1:8000/submissions")
    
    if response.status_code == 200:
        data = response.json()
        
        usernames = [item['username'] for item in data]
        codes = [item['source_code'] for item in data]
        links = [item['srclink'] for item in data]
        
        # Compute combined similarity matrix
        sim_matrix = combined_similarity(codes)
        
        # Display similarity matrix
        df = pd.DataFrame(sim_matrix, index=usernames, columns=usernames)
        st.subheader("👨💻 Combined Similarity Matrix (Mock Submissions)")
        st.dataframe(df.style.background_gradient(cmap='Blues'))
        
        # Display heatmap
        st.subheader("📊 Heatmap View")
        show_heatmap(sim_matrix, usernames)
        
        # Detect plagiarism
        plagiarized_pairs = detect_plagiarism(sim_matrix, usernames, threshold)
        
        if plagiarized_pairs:
            st.subheader("🚨 Potential Plagiarism Detected")
            for u1, u2, score in plagiarized_pairs:
                st.markdown(f"**{u1}** and **{u2}** → Similarity: `{score:.2f}` ❗")
        else:
            st.success("🎉 No high similarity detected. No plagiarism suspected.")
        
        # Submission links
        st.subheader("📌 Submission Links")
        for i, user in enumerate(usernames):
            st.markdown(f"**{user}** → [Link]({links[i]})")
        
        # Download similarity matrix
        csv = df.to_csv()
        st.download_button("Download Similarity Matrix", csv, "simulated_similarity.csv", "text/csv")
    
    else:
        st.error("Failed to fetch simulated data. Is your FastAPI running?")
