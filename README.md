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
- **XGBoost** (Makine öğrenmesi tabanlı regresyon modeli)

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
- **XGBoost:** Gecikmeli değişkenler kullanarak gelişmiş tahminleme yapıldı.

### **5️⃣ Anomali Tespiti**
- IQR (Interquartile Range) yöntemiyle anormal veri noktaları belirlendi.
- Anormal değerler grafiksel olarak görselleştirildi.
- 
## 📬 İletişim
Bu proje hakkında daha fazla bilgi almak veya katkıda bulunmak için benimle iletişime geçebilirsiniz. 🎯
iremnazkararti@gmail.com
