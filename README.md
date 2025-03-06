# jeotermal_santral_analiz
# Enerji Üretim Analizi ve Tahminleme Dashboard'u

## 📌 Proje Açıklaması
Bu proje, jeotermal enerji üretim tesislerinden elde edilen verileri analiz etmek, görselleştirmek ve makine öğrenmesi modelleri kullanarak üretim tahminleri yapmak amacıyla geliştirilmiştir. Çalışma, **Streamlit** kullanılarak interaktif bir web uygulaması olarak sunulmuştur.

🔗 **Canlı Uygulamayı İncelemek İçin:** [Enerji Üretim Dashboard](https://iremnazkararti.streamlit.app/)

## 🏗 Kullanılan Teknolojiler ve Kütüphaneler
- **Python** (Veri işleme, modelleme ve görselleştirme)
- **Streamlit** (Web uygulaması geliştirme)
- **Pandas** (Veri manipülasyonu)
- **NumPy** (Sayısal hesaplamalar)
- **Matplotlib & Plotly** (Veri görselleştirme)
- **Statsmodels** (ARIMA ve SARIMA modelleme)
- **Prophet** (Facebook Prophet ile zaman serisi tahmini)
- **XGBoost** (Makine öğrenmesi tabanlı regresyon modeli)
- **LightGBM** (Gelişmiş zaman serisi tahmini için kullanıldı)
- **LSTM (TensorFlow/Keras)** (Derin öğrenme modeli ile enerji üretimi tahmini)

## 📊 Dashboard İçeriği

### **1️⃣ Veri Seti İncelemesi**
- **Veri kaynağı:** Google Drive'da depolanan zaman serisi verileri çekilerek kullanıldı.
- **Ön işleme aşamaları:** Eksik verilerin doldurulması, aykırı değerlerin temizlenmesi ve zaman serisi indekslemesi gerçekleştirildi.
- **Özellik mühendisliği:** Lag (gecikmeli) değişkenler, hareketli ortalamalar ve tarih bazlı özellikler eklendi.

### **2️⃣ Zaman Serisi Analizi**
- Enerji üretim trendleri incelendi.
- 7 günlük hareketli ortalama hesaplandı.
- Veri seti haftalık, aylık ve yıllık periyotlara bölünerek detaylı analiz yapıldı.

### **3️⃣ Korelasyon Analizi**
- Tüm değişkenler arasındaki korelasyon matrisi hesaplandı.
- Yüksek pozitif veya negatif korelasyona sahip değişkenler belirlendi.

### **4️⃣ Enerji Üretim Tahminleri**
- **ARIMA & SARIMA:** Geleneksel istatistiksel zaman serisi modelleri kullanılarak tahmin yapıldı.
- **Prophet:** Facebook Prophet modeli ile üretim tahmini gerçekleştirildi.
- **LSTM:** Derin öğrenme tabanlı LSTM modeli ile enerji üretimi tahmin edildi.
- **XGBoost & LightGBM:** Gecikmeli değişkenler kullanarak gelişmiş tahminleme yapıldı.

### **5️⃣ Anomali Tespiti**
- IQR (Interquartile Range) yöntemiyle anormal veri noktaları belirlendi.
- Anormal değerler grafiksel olarak görselleştirildi.

## 📌 Kurulum & Çalıştırma
1. **Gereksinimleri yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Streamlit uygulamasını başlatın:**
   ```bash
   streamlit run app3.py
   ```
3. **Tahminleme için Google Drive bağlantısını sağlayın** (Eğer Colab kullanıyorsanız):
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

## 📈 Model Performansı ve Karşılaştırma
- **Hata Metrikleri (MAE, RMSE)** kullanılarak modellerin doğrulukları karşılaştırıldı.
- Prophet, SARIMA, XGBoost, LightGBM ve LSTM modelleri üzerinden hata dağılımları görselleştirildi.

## 📬 İletişim
Bu proje hakkında daha fazla bilgi almak veya katkıda bulunmak için benimle iletişime geçebilirsiniz. 🎯
iremnazkararti@gmail.com
