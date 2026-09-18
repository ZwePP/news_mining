"""
===============================================================================
Data Mining & Pipeline Visualization
===============================================================================
Script Purpose:
This script generates exploratory, mining, and evaluation visualizations for
the news classification pipeline, saving output figures to the docs/ directory.

Visualizations Generated:
1. Class Distribution (Raw Imbalanced vs. Preprocessed Balanced)
2. Confusion Matrix Heatmap (LinearSVC Model Evaluation)
3. Classification Performance Metrics Comparison (Precision, Recall, F1)
4. 2D PCA Latent Semantic Space Projection (SentenceTransformer Embeddings)
5. Text Word Count Distribution by News Category

Usage:
    python scripts/visualize.py
===============================================================================
"""

# =============================================================================
# Imports and Configuration
# =============================================================================
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer

# Ensure repository root is on sys.path for database module imports
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
import scripts.db as db

# Output directory for visualization assets
DOCS_DIR = REPO_ROOT / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Set global visualization aesthetic styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11


# =============================================================================
# 1. Class Distribution Visualization
# =============================================================================
def plot_class_distribution():
    """Visualizes raw class imbalance vs balanced preprocessed distribution."""
    print("Generating: Class Distribution Plot...")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    colors = ['#2b5c8f', '#d95f02']

    # Subplot A: Raw Imbalanced Distribution from Gold Layer
    raw_counts = {'Real News (0)': 189512, 'Fake News (1)': 12815}
    bars1 = axes[0].bar(raw_counts.keys(), raw_counts.values(), color=colors, width=0.5, edgecolor='black')
    axes[0].set_title('Raw Dataset Distribution (Imbalanced)', fontsize=13, fontweight='bold')
    axes[0].set_ylabel('Number of Articles', fontsize=11)
    axes[0].set_ylim(0, 210000)
    for bar in bars1:
        yval = bar.get_height()
        axes[0].text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + 3000,
            f'{yval:,}\n({yval / 202327 * 100:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold'
        )

    # Subplot B: Balanced Distribution after Downsampling
    bal_counts = {'Real News (0)': 12815, 'Fake News (1)': 12815}
    bars2 = axes[1].bar(bal_counts.keys(), bal_counts.values(), color=colors, width=0.5, edgecolor='black')
    axes[1].set_title('Preprocessed Dataset Distribution (Balanced)', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('Number of Articles', fontsize=11)
    axes[1].set_ylim(0, 16000)
    for bar in bars2:
        yval = bar.get_height()
        axes[1].text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + 300,
            f'{yval:,}\n(50.0%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold'
        )

    plt.tight_layout()
    output_path = DOCS_DIR / "class_distribution.png"
    fig.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")


# =============================================================================
# 2. Confusion Matrix Heatmap
# =============================================================================
def plot_confusion_matrix():
    """Visualizes the LinearSVC confusion matrix with raw counts and percentages."""
    print("Generating: Confusion Matrix Plot...")
    # Confusion matrix corresponding to test evaluation (N=5,126)
    # TN=2514, FP=49, FN=188, TP=2375
    cm = np.array([[2514, 49],
                   [188, 2375]])

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(cm, annot=False, cmap='Blues', fmt='d', cbar=True, ax=ax, linewidths=1, linecolor='gray')

    labels = [
        [f"True Real (TN)\n{cm[0, 0]:,} ({cm[0, 0] / cm[0].sum() * 100:.1f}%)",
         f"False Fake (FP)\n{cm[0, 1]:,} ({cm[0, 1] / cm[0].sum() * 100:.1f}%)"],
        [f"False Real (FN)\n{cm[1, 0]:,} ({cm[1, 0] / cm[1].sum() * 100:.1f}%)",
         f"True Fake (TP)\n{cm[1, 1]:,} ({cm[1, 1] / cm[1].sum() * 100:.1f}%)"]
    ]
    for i in range(2):
        for j in range(2):
            color = "white" if cm[i, j] > 1500 else "black"
            ax.text(j + 0.5, i + 0.5, labels[i][j], ha="center", va="center", color=color, fontsize=12, fontweight='bold')

    ax.set_title('LinearSVC Confusion Matrix (Test Set: N=5,126)', fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel('Predicted Label', fontsize=12, labelpad=8)
    ax.set_ylabel('Actual Label', fontsize=12, labelpad=8)
    ax.set_xticklabels(['Real News (0)', 'Fake News (1)'], fontsize=11)
    ax.set_yticklabels(['Real News (0)', 'Fake News (1)'], fontsize=11, rotation=0)

    plt.tight_layout()
    output_path = DOCS_DIR / "confusion_matrix.png"
    fig.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")


# =============================================================================
# 3. Model Classification Metrics
# =============================================================================
def plot_classification_metrics():
    """Visualizes Precision, Recall, and F1-score across both news classes."""
    print("Generating: Classification Performance Metrics Plot...")
    metrics_data = {
        'Metric': ['Precision', 'Recall', 'F1-Score'] * 2,
        'Score': [0.93, 0.98, 0.95, 0.98, 0.93, 0.95],
        'Class': ['Real News (0)'] * 3 + ['Fake News (1)'] * 3
    }
    metrics_df = pd.DataFrame(metrics_data)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bar_plot = sns.barplot(
        data=metrics_df,
        x='Metric',
        y='Score',
        hue='Class',
        palette=['#2b5c8f', '#d95f02'],
        ax=ax,
        edgecolor='black'
    )
    ax.set_title('Model Performance Metrics Comparison by Class (LinearSVC)', fontsize=14, fontweight='bold', pad=12)
    ax.set_ylabel('Score (0.0 - 1.0)', fontsize=12)
    ax.set_xlabel('Evaluation Metric', fontsize=12)
    ax.set_ylim(0, 1.15)
    ax.axhline(0.95, color='green', linestyle='--', linewidth=1.2, label='Overall Accuracy (95%)')

    for p in bar_plot.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(
                f"{h:.2f}",
                (p.get_x() + p.get_width() / 2.0, h),
                ha='center', va='center',
                xytext=(0, 7),
                textcoords='offset points',
                fontsize=11, fontweight='bold'
            )

    ax.legend(title='Category', loc='upper right', frameon=True)
    plt.tight_layout()
    output_path = DOCS_DIR / "model_metrics.png"
    fig.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")


# =============================================================================
# 4. Latent Semantic Space Projection (PCA)
# =============================================================================
def plot_embedding_latent_space(sample_size=300):
    """Encodes a sample from PostgreSQL and visualizes 2D PCA semantic projection."""
    print("Generating: Semantic Latent Embedding PCA Projection...")
    engine = db.db_engine()
    query = f"""
    (SELECT article_text, is_fake FROM gold.total_news WHERE is_fake = 0 ORDER BY RANDOM() LIMIT {sample_size})
    UNION ALL
    (SELECT article_text, is_fake FROM gold.total_news WHERE is_fake = 1 ORDER BY RANDOM() LIMIT {sample_size});
    """
    df_sample = pd.read_sql(query, engine)

    # Encode articles using SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sample_embeddings = model.encode(df_sample['article_text'].tolist(), show_progress_bar=False)

    # Dimensionality reduction via PCA to 2 components
    pca = PCA(n_components=2, random_state=42)
    pca_results = pca.fit_transform(sample_embeddings)
    df_sample['PCA1'] = pca_results[:, 0]
    df_sample['PCA2'] = pca_results[:, 1]
    df_sample['Category'] = df_sample['is_fake'].map({0: 'Real News (0)', 1: 'Fake News (1)'})

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(
        data=df_sample,
        x='PCA1',
        y='PCA2',
        hue='Category',
        palette={'Real News (0)': '#2b5c8f', 'Fake News (1)': '#d95f02'},
        alpha=0.75,
        s=50,
        edgecolor='none',
        ax=ax
    )
    ax.set_title('2D PCA Projection of SentenceTransformer Latent Embeddings', fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0] * 100:.1f}% Variance)', fontsize=11)
    ax.set_ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1] * 100:.1f}% Variance)', fontsize=11)
    ax.legend(title='News Class', frameon=True)

    plt.tight_layout()
    output_path = DOCS_DIR / "embedding_separation.png"
    fig.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved: {output_path}")

    # =============================================================================
    # 5. Article Text Word Count Distribution
    # =============================================================================
    print("Generating: Text Word Count Distribution Plot...")
    df_sample['word_count'] = df_sample['article_text'].str.split().apply(len)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(
        data=df_sample,
        x='word_count',
        hue='Category',
        palette={'Real News (0)': '#2b5c8f', 'Fake News (1)': '#d95f02'},
        bins=30,
        kde=True,
        element='step',
        ax=ax
    )
    ax.set_title('Word Count Distribution by News Class', fontsize=14, fontweight='bold', pad=12)
    ax.set_xlabel('Word Count per Article Description/Text', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)

    plt.tight_layout()
    output_path_hist = DOCS_DIR / "text_length_distribution.png"
    fig.savefig(output_path_hist, dpi=300)
    plt.close()
    print(f"Saved: {output_path_hist}")


# =============================================================================
# Execution Entrypoint
# =============================================================================
if __name__ == "__main__":
    print("Starting Data Mining Visualization Suite...")
    plot_class_distribution()
    plot_confusion_matrix()
    plot_classification_metrics()
    plot_embedding_latent_space(sample_size=300)
    print("All visualizations successfully generated and saved to docs/!")
