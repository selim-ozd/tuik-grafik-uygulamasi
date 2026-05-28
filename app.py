import streamlit as st
import pandas as pd

st.title("TUIK Dogum Istatistikleri Simulasyonu")

st.sidebar.header("Parametreleri Degistirin")
tahmin_hiz = st.sidebar.slider("Sizce 2025 Dogurganlik Hizi Kac Olmaliydi?", 1.0, 3.0, 1.42, 0.01)

data = {
    'Yil': [2001, 2010, 2015, 2020, 2025],
    'Gercek Veri': [2.38, 2.08, 2.15, 1.71, 1.42]
}
df = pd.DataFrame(data)

df['Sizin Simulasyonunuz'] = [2.38, 2.08, 2.15, 1.71, tahmin_hiz]

st.write(f"Su anki seciminiz: **{tahmin_hiz}** (Nufusun kendini yenileme esigi: **2.10**)")
st.line_chart(df.set_index('Yil'))