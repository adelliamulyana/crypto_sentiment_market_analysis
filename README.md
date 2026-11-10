# crypto_sentiment_market_analysis

**Studi Kasus Portofolio Data: Crypto Market & Sentiment Dynamics (BTC vs. ETH)**

**Fokus Domain: Analisis Pasar Aset Kripto, Behavioral Finance, dan Sentimen Publik**

**Target Sektor: Inovasi Teknologi Sektor Keuangan, Aset Keuangan Digital, & Aset Kripto (ITSK & AKD)**

**Latar Belakang Masalah**

Pasar aset keuangan digital, khususnya kripto, dikenal memiliki volatilitas tinggi yang sangat dipengaruhi oleh persepsi publik, pemberitaan media, serta narasi regulasi. Berbeda dengan instrumen keuangan konvensional yang digerakkan oleh fundamental ekonomi makro secara langsung, pergerakan harga aset kripto (seperti Bitcoin dan Ethereum) sering kali dipicu oleh gelombang sentimen emosional di ruang digital (retail panic, FOMO, atau berita adopsi institusional).
Bagi regulator, analis risiko, maupun lembaga pengawas seperti OJK (di sektor ITSK & AKD), memahami hubungan antara sentimen publik dan volatilitas pasar sangat krusial untuk mendeteksi potensi risiko pasar, manipulasi informasi, atau perlindungan konsumen (consumer protection) di ekosistem keuangan digital.

**Pernyataan Masalah**

Studi kasus ini bertujuan untuk menjawab beberapa pertanyaan kunci:

a. Sejauh mana korelasi antara skor sentimen harian terhadap pergerakan harga dan volume transaksi Bitcoin (BTC) dan Ethereum (ETH)?

b. Apakah aset blue-chip utama memiliki ketahanan sentimen yang berbeda dibandingkan dengan Ethereum yang memiliki ekosistem utilitas (smart contract) lebih luas?

c. Apakah ada pola lag time, apakah lonjakan sentimen negatif hari ini baru memicu penurunan harga pada keesokan harinya?

**Dataset**

Project ini menggunakan dataset berita yang bersumber dari kaggle dan data Harga BTC dan ETH yang diunduh dari Yahoo Finance untuk periode 1 bulan terakhir (9 April 2026 - 9 Mei 2026).

**Tools**

Python, Pandas, NumPy, Matplotlib, Seaborn, Textblob

**Project Workflow**
1. Business & Problem Definition
2. Data Extraction: (Yahoo Finance: BTC & ETH Prices) + (Dataset Berita/Sosmed)
3. Data Preprocessing & NLP: (Text Cleaning & TextBlob Sentiment Scoring)
4. Feature Engineering: (Daily Return Calculation & Time-Series Alignment)
5. Statistical & Correlation Analysis: (Pearson Correlation & Lag-1 Analysis)
6. Visualisasi: (Time-Series Trends, Correlation Heatmaps, & Regression Plots)
   
**Temuan Utama dan Penjelasan Singkat**
1. Pearson Correlation (Daily Sentiment vs. Daily Return)

   Bitcoin (BTC): r = 0.0917 (Korelasi positif sangat lemah)

   Ethereum (ETH): r = -0.0339 (Hampir tidak ada korelasi linear)

   Analisis: Sentimen berita harian tidak memiliki korelasi linear yang kuat terhadap daily return kedua aset. Pergerakan harga harian lebih dominan dipengaruhi oleh faktor likuiditas makro, arus modal institusional, dan transaksi pasar derivatif secara global.

2. Lag-1 Correlation (Sentimen Hari Ini vs. Return Hari Esok)

   BTC Lag-1: r = 0.0009

   ETH Lag-1: r = 0.0434

   Analisis: Efek lag-1 yang mendekati nol menunjukkan bahwa pasar kripto bekerja secara efisien dalam menyerap informasi publik. Lonjakan sentimen publik atau berita diserap secara mendadak/instan pada hari yang sama dan tidak memicu efek tunda yang signifikan pada keesokan harinya.

3. Perbedaan Ketahanan Sentimen (BTC vs. ETH)

   Bitcoin (BTC) cenderung merespons narasi makroekonomi global dan kepatuhan regulasi secara lebih konsisten.

   Ethereum (ETH) memiliki dinamika sentimen yang lebih terdistorsi oleh isu internal ekosistemnya (seperti utilitas smart contract, aktivitas DeFi, dan gas fees), yang menyebabkan respons harganya sering kali independen dari sentimen berita finansial umum.
