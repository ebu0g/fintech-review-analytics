import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from src.nlp import analyze_reviews

clean = pd.read_csv('data/raw/playstore_reviews_clean.csv')
full = analyze_reviews(clean)
full.to_csv('data/raw/playstore_reviews_analyzed_full.csv', index=False)
print('saved full analysis with columns:', full.columns.tolist())
for bank, group in full.groupby('bank'):
    print('\n', bank)
    print(group['identified_theme'].value_counts().head(10).to_string())
