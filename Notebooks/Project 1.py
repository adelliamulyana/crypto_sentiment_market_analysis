import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
import yfinance as yf
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
from matplotlib import pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

print("--- Data Berita ---")
data = pd.read_csv("Data Berita.csv")
print("Data Berita:")
print(data.head())
print("Data Harga BTC dan ETH akan diunduh dari Yahoo Finance untuk periode 1 bulan terakhir (9 April 2026 - 9 Mei 2026).")
data1 = yf.download("BTC-USD", start="2026-04-09", end="2026-05-09")
data2 = yf.download("ETH-USD", start="2026-04-09", end="2026-05-09")
print("\n--- Data Harga BTC ---")
print(data1.head())
print("\n--- Data Harga ETH ---")
print(data2.head())

print("\n--- text preprocessing dan sentiment analysis ---")
def clean_text(text):
    text = str(text).lower() 
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text) 
    text = re.sub(r'https?://\S+|www\.\S+', '', text) 
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

data['c_Title'] = data['Title'].apply(clean_text)

def get_sentiment_polarity(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

data['sentiment'] = data['c_Title'].apply(get_sentiment_polarity)

def categorize_sentiment(score):
    if score > 0.0005:
        return 'Positive'
    elif score < -0.0005:
        return 'Negative'
    else:
        return 'Neutral'

data['kategori_sentimen'] = data['sentiment'].apply(categorize_sentiment)
print(data[['c_Title', 'sentiment', 'kategori_sentimen']].head())


print("\n--- sentiment harian ---")
data['Published_At'] = pd.to_datetime(data['Published_At'])
sentimen_harian = data.groupby(data['Published_At'].dt.date)['sentiment'].mean().reset_index()
sentimen_harian['Published_At'] = pd.to_datetime(sentimen_harian['Published_At'])
sentimen_harian = sentimen_harian.rename(columns={'Published_At': 'tanggal'})


print("\n---preprocessing data harga dan sentiment harian---")
def prep_crypto_df(df, name):
    df = df.reset_index()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df['Date'] = pd.to_datetime(df['Date'])
    
    df['daily_return'] = df['Close'].pct_change()
    
    df = df.rename(columns={'Date': 'tanggal', 'Close': f'{name}_close', 'daily_return': f'{name}_return'})
    return df

btc_df = prep_crypto_df(data1, 'btc')
eth_df = prep_crypto_df(data2, 'eth')

merged_btc = pd.merge(btc_df, sentimen_harian, on='tanggal', how='inner').dropna()
merged_eth = pd.merge(eth_df, sentimen_harian, on='tanggal', how='inner').dropna()

print(f"Jumlah baris data gabungan BTC: {len(merged_btc)}")
print(f"Jumlah baris data gabungan ETH: {len(merged_eth)}")


print("\n--- analisis korelasi pearson ---")
pearrson_btc = merged_btc['btc_return'].corr(merged_btc['sentiment'])
pearrson_eth = merged_eth['eth_return'].corr(merged_eth['sentiment'])

matrix_korelasi_btc = merged_btc[['btc_return', 'sentiment']].corr(method='pearson')
matrix_korelasi_eth = merged_eth[['eth_return', 'sentiment']].corr(method='pearson')

print("Korelasi Pearson antara Daily Return BTC dan sentimen berita:", pearrson_btc)
print("Korelasi Pearson antara Daily Return ETH dan sentimen berita:", pearrson_eth)


print("\n---analisis lag time ---")
merged_btc['sentiment_lag1'] = merged_btc['sentiment'].shift(1)
merged_eth['sentiment_lag1'] = merged_eth['sentiment'].shift(1)

lag_corr_btc = merged_btc['btc_return'].corr(merged_btc['sentiment_lag1'])
lag_corr_eth = merged_eth['eth_return'].corr(merged_eth['sentiment_lag1'])

print(f"Lag-1 Correlation (Sentimen Kemarin vs Return BTC Hari Ini): {lag_corr_btc:.4f}")
print(f"Lag-1 Correlation (Sentimen Kemarin vs Return ETH Hari Ini): {lag_corr_eth:.4f}")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.heatmap(matrix_korelasi_btc, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f")
plt.title('Korelasi Sentimen vs Daily Return BTC')

plt.subplot(1, 2, 2)
sns.heatmap(matrix_korelasi_eth, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f")
plt.title('Korelasi Sentimen vs Daily Return ETH')

plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 6))

plt.subplot(2, 1, 1)
plt.plot(merged_btc['tanggal'], merged_btc['btc_close'], color='orange', linewidth=2, label='BTC Close Price')
plt.title('Pergerakan Harga Penutupan Harian (BTC vs ETH)')
plt.ylabel('BTC Price (USD)')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)

plt.subplot(2, 1, 2)
plt.plot(merged_eth['tanggal'], merged_eth['eth_close'], color='blue', linewidth=2, label='ETH Close Price')
plt.xlabel('Tanggal')
plt.ylabel('ETH Price (USD)')
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

sns.regplot(
    data=merged_btc, x='sentiment', y='btc_return', 
    ax=axes[0], color='orange', 
    scatter_kws={'alpha': 0.7}, line_kws={'color': 'darkred'}
)
axes[0].set_title('Regresi Sentimen vs Daily Return (BTC)')
axes[0].set_xlabel('Skor Sentimen Berita')
axes[0].set_ylabel('Daily Return BTC')
axes[0].grid(True, linestyle='--', alpha=0.5)

sns.regplot(
    data=merged_eth, x='sentiment', y='eth_return', 
    ax=axes[1], color='blue', 
    scatter_kws={'alpha': 0.7}, line_kws={'color': 'darkred'}
)
axes[1].set_title('Regresi Sentimen vs Daily Return (ETH)')
axes[1].set_xlabel('Skor Sentimen Berita')
axes[1].set_ylabel('Daily Return ETH')
axes[1].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()