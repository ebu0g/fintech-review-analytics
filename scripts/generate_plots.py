import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path('plots')
OUT.mkdir(exist_ok=True)

# Sentiment share by bank
sfb = pd.read_csv('data/raw/sentiment_summary_by_bank.csv')
if {'bank','positive_share','neutral_share','negative_share'}.issubset(sfb.columns):
    sfb.set_index('bank', inplace=True)
    ax = sfb[['positive_share','neutral_share','negative_share']].plot(kind='bar', stacked=True, figsize=(8,4), colormap='tab20')
    ax.set_ylabel('Share')
    ax.set_title('Sentiment Share by Bank')
    plt.tight_layout()
    plt.savefig(OUT / 'sentiment_share_by_bank.png', dpi=150)
    plt.close()
    print('Saved', OUT / 'sentiment_share_by_bank.png')
else:
    print('Missing columns in sentiment_summary_by_bank.csv')

# Rating distribution per bank
clean = pd.read_csv('data/raw/playstore_reviews_clean.csv')
if {'bank','rating'}.issubset(clean.columns):
    plt.figure(figsize=(8,6))
    for i, (bank, g) in enumerate(clean.groupby('bank')):
        plt.subplot(1,3,i+1)
        g['rating'].hist(bins=[1,2,3,4,5,6])
        plt.title(bank)
        plt.xlabel('Rating')
        plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(OUT / 'rating_distribution_by_bank.png', dpi=150)
    plt.close()
    print('Saved', OUT / 'rating_distribution_by_bank.png')
else:
    print('Missing columns in playstore_reviews_clean.csv')

# Top themes per bank
full = pd.read_csv('data/raw/playstore_reviews_analyzed_full.csv')
if {'bank','identified_theme'}.issubset(full.columns):
    for bank, g in full.groupby('bank'):
        vc = g['identified_theme'].value_counts().head(10)
        plt.figure(figsize=(6,4))
        vc.sort_values().plot(kind='barh')
        plt.title(f'Top Themes — {bank}')
        plt.xlabel('Count')
        plt.tight_layout()
        fname = OUT / f'top_themes_{bank.replace(" ","_")}.png'
        plt.savefig(fname, dpi=150)
        plt.close()
        print('Saved', fname)
else:
    print('Missing columns in playstore_reviews_analyzed_full.csv')
