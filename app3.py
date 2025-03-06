import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import gdown  # Google Drive'dan veri indirmek için
import streamlit as st
import pandas as pd
import gdown  # Google Drive'dan veri indirmek için
from sklearn.model_selection import train_test_split
import xgboost as xgb


# 📌 Dashboard Ayarları
st.set_page_config(page_title="⚡ Enerji Üretim Dashboard", layout="wide")

@st.cache_data
def load_data():
    file_id = "1ERlscTm0SV49syHXzyMEvW6pvpPVD3qK"  # Yeni Google Drive ID'si
    url = f"https://drive.google.com/uc?export=download&id={file_id}"  # Yeni indirme linki
    output = "dataset.csv"
    
    try:
        # Veriyi indir
        gdown.download(url, output, quiet=False)
        
        # CSV'yi oku ve işle
        df = pd.read_csv(output)
        df.rename(columns={"Unnamed: 0": "date"}, inplace=True)
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        df = df.resample("D").mean().interpolate()  # Eksik verileri doldur
        return df
    
    except Exception as e:
        st.error(f"📛 Veri yüklenirken hata oluştu: {e}")
        return pd.DataFrame()  # Hata durumunda boş dataframe döndür


df = load_data()  # Veriyi yükle

# 📌 **Sidebar Filtreleri**
st.sidebar.header("⚙️ Filtreler")
start_date = st.sidebar.date_input("Başlangıç Tarihi", df.index.min().date())
end_date = st.sidebar.date_input("Bitiş Tarihi", df.index.max().date())
df = df.loc[start_date:end_date]

view_option = st.sidebar.radio(
    "🔍 Dashboard Seç:", 
    ["📂 Veri Seti", "📊 Zaman Serisi", "📉 Korelasyon", "🔮 Tahminler", "🚨 Anomali Tespiti"]
)

# 📂 **1️⃣ Veri Seti**
if view_option == "📂 Veri Seti":
    st.subheader("📂 Veri Seti")
    st.dataframe(df.head(50))
    st.write("Seçilen tarih aralığında veri setinden ilk 50 satır.")

    # KPI Kartları
    col1, col2 = st.columns(2)
    col1.metric("🔹 Ortalama Sinem Üretimi (MW)", round(df["sinem_guc_net"].mean(), 2))
    col2.metric("🔹 Ortalama Deniz Üretimi (MW)", round(df["deniz_guc_net"].mean(), 2))

# 📊 **2️⃣ Zaman Serisi Analizi**
elif view_option == "📊 Zaman Serisi":
    st.subheader("📊 Enerji Üretimi Zaman Serisi")
    fig = px.line(df, x=df.index, y=["sinem_guc_net", "deniz_guc_net"], title="Sinem & Deniz Güç Üretimi")
    st.plotly_chart(fig, use_container_width=True)

    # Hareketli Ortalama
    df["sinem_7gün"] = df["sinem_guc_net"].rolling(7).mean()
    df["deniz_7gün"] = df["deniz_guc_net"].rolling(7).mean()
    fig2 = px.line(df, x=df.index, y=["sinem_7gün", "deniz_7gün"], title="7 Günlük Hareketli Ortalama")
    st.plotly_chart(fig2, use_container_width=True)

# 📉 **3️⃣ Korelasyon Analizi**
elif view_option == "📉 Korelasyon":
    st.subheader("📉 Korelasyon Analizi")
    
    # Korelasyon matrisi
    corr = df.corr()

    # Plotly heatmap oluşturma
    fig = px.imshow(
        corr.values,
        x=corr.columns,
        y=corr.index,
        color_continuous_scale="RdBu",  # Alternatif: "Viridis", "Blues"
        title="Korelasyon Matrisi",
        labels=dict(color="Korelasyon"),
        zmin=-1, zmax=1
    )

    # Grafik boyutunu artır
    fig.update_layout(
        autosize=False,
        width=900,  # Genişlik (px)
        height=800,  # Yükseklik (px)
        margin=dict(l=100, r=100, t=100, b=100)
    )

    # Grafiği göster
    st.plotly_chart(fig, use_container_width=True)


# 📉 **5️⃣ Tahminleme (Forecasting)**
elif view_option == "🔮 Tahminler":
    st.subheader("🔮 Enerji Üretim Tahminleri")
    model_option = st.selectbox("Tahmin Modeli:", ["XGBoost"])
    days = st.slider("Kaç Günlük Tahmin Yapılsın?", 30, 365, 100)

    if st.button("📈 Tahmini Başlat"):
        with st.spinner("Tahmin yapılıyor..."):
            df_daily = df.resample("D").mean()
            forecast_sinem, forecast_deniz = None, None

     
            if model_option == "XGBoost":
                df_xgb = df_daily.copy()
                for lag in range(1, 8):
                    df_xgb[f"sinem_guc_net_lag{lag}"] = df_xgb["sinem_guc_net"].shift(lag)
                    df_xgb[f"deniz_guc_net_lag{lag}"] = df_xgb["deniz_guc_net"].shift(lag)
                df_xgb.dropna(inplace=True)
                features = [col for col in df_xgb.columns if "lag" in col]
                X_train, X_test, y_train_sinem, y_test_sinem = train_test_split(df_xgb[features], df_xgb["sinem_guc_net"], test_size=0.2, shuffle=False)
                X_train, X_test, y_train_deniz, y_test_deniz = train_test_split(df_xgb[features], df_xgb["deniz_guc_net"], test_size=0.2, shuffle=False)
                xgb_model_sinem, xgb_model_deniz = xgb.XGBRegressor(n_estimators=100), xgb.XGBRegressor(n_estimators=100)
                xgb_model_sinem.fit(X_train, y_train_sinem)
                xgb_model_deniz.fit(X_train, y_train_deniz)
                forecast_sinem = xgb_model_sinem.predict(df_xgb[features].iloc[-days:])
                forecast_deniz = xgb_model_deniz.predict(df_xgb[features].iloc[-days:])

            forecast_dates = pd.date_range(df_daily.index[-1] + pd.DateOffset(1), periods=days, freq="D")

            # MAPE Hesaplama Fonksiyonu (Hata Önleme Dahil)
            def mean_absolute_percentage_error(y_true, y_pred):
                y_true = y_true.replace(0, np.nan).dropna()  # 0 olanları NaN yap, sonra temizle
                y_pred = y_pred[:len(y_true)]  # Uzunluk eşitle
                if len(y_true) == 0 or len(y_pred) == 0:  # Eğer hiç veri kalmadıysa NaN döndür
                    return np.nan
                return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

            # Gerçek verileri alırken NaN olanları temizle
            last_real_sinem = df_daily["sinem_guc_net"].iloc[-days:].dropna()
            last_real_deniz = df_daily["deniz_guc_net"].iloc[-days:].dropna()

            # MAPE hesaplama
            mape_sinem = mean_absolute_percentage_error(last_real_sinem, forecast_sinem)
            mape_deniz = mean_absolute_percentage_error(last_real_deniz, forecast_deniz)

            # Doğruluk yüzdesi hesaplama
            accuracy_sinem = 100 - round(mape_sinem, 2) if not np.isnan(mape_sinem) else "Veri Eksik"
            accuracy_deniz = 100 - round(mape_deniz, 2) if not np.isnan(mape_deniz) else "Veri Eksik"

            # Grafik çizimi
            fig = px.line(title="Enerji Üretim Tahmini")
            fig.add_scatter(x=df_daily.index, y=df_daily["sinem_guc_net"], mode="lines", name="Gerçek Sinem Üretimi", line=dict(color="blue"))
            fig.add_scatter(x=forecast_dates, y=forecast_sinem, mode="lines", name=f"{model_option} Sinem Tahmini", line=dict(color="red"))
            fig.add_scatter(x=df_daily.index, y=df_daily["deniz_guc_net"], mode="lines", name="Gerçek Deniz Üretimi", line=dict(color="green"))
            fig.add_scatter(x=forecast_dates, y=forecast_deniz, mode="lines", name=f"{model_option} Deniz Tahmini", line=dict(color="orange"))
            st.plotly_chart(fig, use_container_width=True)

            # Doğruluk oranlarını göster
            st.markdown(f"### 🎯 Model Doğruluk Oranları")
            col1, col2 = st.columns(2)
            col1.metric(f"🔵 {model_option} Sinem Tahmin Doğruluğu", f"% {accuracy_sinem}")
            col2.metric(f"🟠 {model_option} Deniz Tahmin Doğruluğu", f"% {accuracy_deniz}")


# 🚨 **7️⃣ Anomali Tespiti**
elif view_option == "🚨 Anomali Tespiti":
    st.subheader("🚨 Anormal Üretim Değerleri")
    threshold = st.slider("Anomali Eşik Değeri", 0.5, 2.0, 1.5)
    anomalies = df[(df["sinem_guc_net"] > threshold * df["sinem_guc_net"].mean())]
    st.dataframe(anomalies)
