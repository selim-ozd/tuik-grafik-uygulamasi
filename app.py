import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import time

# Sayfa Genişlik Ayarı
st.set_page_config(page_title="TÜİK Nüfus ve AB Kıyaslama Paneli", layout="wide")

# --- OYUN HAFIZASI (Session State) ---
if 'game_guess' not in st.session_state:
    st.session_state.game_guess = 1.42 # Başlangıç değeri (2025 verisi)
if 'game_history' not in st.session_state:
    st.session_state.game_history = []

st.title("🇹🇷 TÜİK Doğum İstatistikleri ve AB Kıyaslama Portalı")
st.markdown("---")

# --- BÖLÜM 1: 2026 TAHMİN OYUNU ---
st.header("1. Hedef 1.62: 2026 Doğurganlık Hızı Tahmin Oyunu")
st.write("Türkiye'nin 2026 yılında doğurganlık hızının kaç olacağını tahmin edin. İpucu: Hedefimiz 1.62!")

col_game1, col_game2 = st.columns([1, 2])

with col_game1:
    user_guess = st.number_input("Tahmininizi Girin (Örn: 1.55):", min_value=1.0, max_value=3.0, value=st.session_state.game_guess, step=0.01)
    
    if st.button("Tahmini Kontrol Et"):
        st.session_state.game_guess = user_guess
        st.session_state.game_history.append(user_guess)
        
        if user_guess < 1.62:
            st.warning("🔼 Biraz daha yukarı! Türkiye'nin daha çok bebeğe ihtiyacı var.")
        elif user_guess > 1.62:
            st.warning("🔽 Biraz daha aşağı! Tahmininiz hedefin üzerinde.")
        else:
            st.balloons()
            st.success("🎯 Tebrikler! 1.62 hedefini tam isabetle buldunuz!")

with col_game2:
    # Grafik hazırlığı
    yillar_game = [2020, 2025, 2026]
    veriler_game = [1.71, 1.42, user_guess]
    df_game = pd.DataFrame({'Yıl': yillar_game, 'Tahmin Trendi': veriler_game})
    st.line_chart(df_game.set_index('Yıl'))
    st.caption("Grafikte 2026 noktası sizin girdiğiniz tahmine göre anlık değişir.")

st.markdown("---")

# --- BÖLÜM 2: HARİTA VE ANİMASYONLU ŞEHİR ANALİZİ ---
st.header("2. Şehir Bazlı Derin Analiz (Harita Etkileşimli)")
st.write("Haritadan bir şehre tıklayın; verinin grafikte canlı olarak çizilmesini izleyin.")

sehir_verileri = {
    "Sanliurfa": {"enlem": 37.1674, "boylam": 38.7939, "veriler": [4.50, 4.30, 4.00, 3.71, 3.15]},
    "Sirnak": {"enlem": 37.5182, "boylam": 42.4615, "veriler": [4.00, 3.80, 3.50, 3.20, 2.63]},
    "Istanbul": {"enlem": 41.0082, "boylam": 28.9784, "veriler": [2.03, 1.95, 1.88, 1.50, 1.20]},
    "Ankara": {"enlem": 39.9334, "boylam": 32.8597, "veriler": [1.90, 1.80, 1.70, 1.45, 1.25]},
    "Izmir": {"enlem": 38.4237, "boylam": 27.1428, "veriler": [1.85, 1.75, 1.65, 1.40, 1.22]},
    "Bartin": {"enlem": 41.6344, "boylam": 32.3375, "veriler": [1.75, 1.65, 1.55, 1.35, 1.09]}
}
yillar_main = [2001, 2010, 2015, 2020, 2025]
turkiye_gercek = [2.38, 2.08, 2.15, 1.71, 1.42]

map_col, chart_col = st.columns([1.2, 1])

with map_col:
    m = folium.Map(location=[39.0, 35.2], zoom_start=6)
    for sehir, bilgi in sehir_verileri.items():
        renk = "green" if bilgi["veriler"][-1] >= 2.10 else "red"
        folium.Marker(location=[bilgi["enlem"], bilgi["boylam"]], tooltip=sehir, icon=folium.Icon(color=renk)).add_to(m)
    map_data = st_folium(m, width=650, height=400)

selected_city = None
if map_data and map_data.get("last_object_clicked"):
    lat, lng = map_data["last_object_clicked"]["lat"], map_data["last_object_clicked"]["lng"]
    for s, b in sehir_verileri.items():
        if abs(b["enlem"] - lat) < 0.1 and abs(b["boylam"] - lng) < 0.1:
            selected_city = s

with chart_col:
    chart_placeholder = st.empty()
    base_df = pd.DataFrame({'Yıl': yillar_main, 'Türkiye Ortalaması': turkiye_gercek})
    if selected_city:
        city_data = sehir_verileri[selected_city]["veriler"]
        for i in range(1, len(yillar_main) + 1):
            temp_df = base_df.copy()
            temp_df[selected_city] = city_data[:i] + [None] * (len(yillar_main) - i)
            chart_placeholder.line_chart(temp_df.set_index('Yıl'))
            time.sleep(0.1)
    else:
        chart_placeholder.line_chart(base_df.set_index('Yıl'))

st.markdown("---")

# --- BÖLÜM 3: AVRUPA BİRLİĞİ KIYASLAMASI ---
st.header("3. Türkiye vs Avrupa Birliği (2024 Karşılaştırması)")
st.write("Sol tarafta Türkiye sabit. Sağ taraftan bir AB üyesi seçerek kıyaslayın.")

# AB Verileri (Yaklaşık 2024 Değerleri)
ab_verileri = {
    "Fransa": 1.79, "Ispanya": 1.16, "Italya": 1.24, "Almanya": 1.36, 
    "Polonya": 1.26, "Yunanistan": 1.32, "Isvreç": 1.39, "Hollanda": 1.49,
    "Danimarka": 1.55, "Irlanda": 1.54
}

col_eu1, col_eu2 = st.columns(2)

with col_eu1:
    st.subheader("🇹🇷 Türkiye")
    st.metric("Doğurganlık Hızı", "1.42")
    st.write("Türkiye şu an AB ortalamasına yakın ancak yenilenme eşiğinin (2.10) altında.")

with col_eu2:
    st.subheader("🇪🇺 AB Üyesi Seçin")
    secilen_ulke = st.selectbox("Kıyaslamak istediğiniz ülkeyi seçin:", list(ab_verileri.keys()))
    ulke_hizi = ab_verileri[secilen_ulke]
    st.metric(f"{secilen_ulke} Hızı", ulke_hizi)

# Kıyaslama Grafiği (Yenilenme Eşiği Yeniden Eklendi ve Açıklama Alanı Düzenlendi)
st.subheader("Kıyaslama Grafiği")

kiyas_df = pd.DataFrame({
    'Ülke': ["Türkiye", secilen_ulke, "Yenilenme Eşiği"],
    'Doğurganlık Hızı': [1.42, ulke_hizi, 2.10]
})

# Sütunları daha ince ve estetik göstermek için alanı daraltıyoruz
grafik_sol, grafik_orta, grafik_sag = st.columns([1, 2, 1])

with grafik_orta:
    st.bar_chart(kiyas_df.set_index('Ülke'), y="Doğurganlık Hızı")

# Yenilenme Eşiği Bilgi Notu (Eklenti Açıklama)
st.caption("""
ℹ️ **Nüfusun Yenilenme Eşiği (2.10):** Bir ülkedeki nüfusun yapısal olarak azalmadan veya artmadan, sabit ve dengede kalabilmesi için kadın başına düşen ortalama doğum oranıdır. Çocuk ölümleri ve doğal cinsiyet dengesi sebebiyle bu oran tam olarak 2.10 kabul edilir.
""")
