import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import time

# Sayfa ayarları
st.set_page_config(page_title="TÜİK Nüfus Analiz Paneli", layout="wide")

# CSS ile görsellik ekleyelim
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stHeader { color: #1e3a8a; }
    </style>
    """, unsafe_allow_view_ Wood=True)

st.title("🇹🇷 TÜİK Doğum İstatistikleri Etkileşimli Paneli")
st.markdown("---")

# --- BÖLÜM 1: GENEL SİMÜLASYON (SLIDER) ---
st.header("1. Türkiye Geneli Gelecek Simülasyonu")
col1, col2 = st.columns([1, 2])

with col1:
    st.write("Aşağıdaki sürgüyü kullanarak 2025 yılı için bir doğurganlık hızı belirleyin ve Türkiye trendine etkisini görün.")
    tahmin_hiz = st.slider("2025 Hedef Hızı Seçin:", 1.0, 3.0, 1.42, 0.01)

# Veri Hazırlama
yillar = [2001, 2010, 2015, 2020, 2025]
turkiye_gercek = [2.38, 2.08, 2.15, 1.71, 1.42]
simulasyon_verisi = [2.38, 2.08, 2.15, 1.71, tahmin_hiz]

df_sim = pd.DataFrame({
    'Yıl': yillar,
    'Mevcut Trend': turkiye_gercek,
    'Sizin Simülasyonunuz': simulasyon_verisi,
    'Yenilenme Eşiği (2.10)': [2.10] * 5
})

with col2:
    st.line_chart(df_sim.set_index('Yıl'))

st.markdown("---")

# --- BÖLÜM 2: HARİTA VE ANİMASYONLU ŞEHİR ANALİZİ ---
st.header("2. Şehir Bazlı Derin Analiz (Harita Etkileşimli)")
st.write("Haritadan bir şehre tıklayın; o şehrin verisinin grafikte **canlı olarak çizilmesini** izleyin.")

sehir_verileri = {
    "Sanliurfa": {"enlem": 37.1674, "boylam": 38.7939, "veriler": [4.50, 4.30, 4.00, 3.71, 3.15]},
    "Sirnak": {"enlem": 37.5182, "boylam": 42.4615, "veriler": [4.00, 3.80, 3.50, 3.20, 2.63]},
    "Istanbul": {"enlem": 41.0082, "boylam": 28.9784, "veriler": [2.03, 1.95, 1.88, 1.50, 1.20]},
    "Ankara": {"enlem": 39.9334, "boylam": 32.8597, "veriler": [1.90, 1.80, 1.70, 1.45, 1.25]},
    "Izmir": {"enlem": 38.4237, "boylam": 27.1428, "veriler": [1.85, 1.75, 1.65, 1.40, 1.22]},
    "Bartin": {"enlem": 41.6344, "boylam": 32.3375, "veriler": [1.75, 1.65, 1.55, 1.35, 1.09]}
}

map_col, chart_col = st.columns([1.2, 1])

with map_col:
    m = folium.Map(location=[39.0, 35.2], zoom_start=6)
    for sehir, bilgi in sehir_verileri.items():
        renk = "green" if bilgi["veriler"][-1] >= 2.10 else "red"
        folium.Marker(
            location=[bilgi["enlem"], bilgi["boylam"]],
            popup=f"{sehir}: {bilgi['veriler'][-1]}",
            tooltip=sehir,
            icon=folium.Icon(color=renk, icon="info-sign")
        ).add_to(m)
    
    map_data = st_folium(m, width=650, height=450)

# Tıklanan şehri bulma
selected_city = None
if map_data and map_data.get("last_object_clicked"):
    lat, lng = map_data["last_object_clicked"]["lat"], map_data["last_object_clicked"]["lng"]
    for s, b in sehir_verileri.items():
        if abs(b["enlem"] - lat) < 0.1 and abs(b["boylam"] - lng) < 0.1:
            selected_city = s

with chart_col:
    chart_placeholder = st.empty() # Animasyon için boş alan
    
    # Başlangıç verisi (Sadece Türkiye ortalaması)
    base_df = pd.DataFrame({'Yıl': yillar, 'Türkiye Ortalaması': turkiye_gercek})
    
    if selected_city:
        st.success(f"📍 {selected_city} seçildi. Veri yükleniyor...")
        city_full_data = sehir_verileri[selected_city]["veriler"]
        
        # ANİMASYON DÖNGÜSÜ: Çizgiyi adım adım çiziyoruz
        for i in range(1, len(yillar) + 1):
            temp_df = base_df.copy()
            # Şehrin sadece i. yıla kadar olan kısmını ekle, gerisini None yap
            temp_df[selected_city] = city_full_data[:i] + [None] * (len(yillar) - i)
            
            # Grafiği güncelle
            chart_placeholder.line_chart(temp_df.set_index('Yıl'))
            time.sleep(0.15) # Çizim hızı (saniye)
            
    else:
        chart_placeholder.line_chart(base_df.set_index('Yıl'))
        st.info("İstatistiklerini çizdirmek için haritadan bir şehre tıklayın.")
