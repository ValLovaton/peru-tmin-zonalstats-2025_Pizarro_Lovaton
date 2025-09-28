import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import geopandas as gpd

# Ajuste de path para importar scripts
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from scripts.data_prep import load_admin_level
from scripts.zonal_stats import compute_band_stats
from scripts.plotting import plot_distribution, top_bottom_ranking, plot_choropleth

st.set_page_config(page_title="🧊 Perú Tmin Zonal Stats", layout="wide")

# --- Sidebar
st.sidebar.header("⚙️ Configuración")
level = st.sidebar.selectbox("Nivel territorial", ["district", "province", "department"])
band = st.sidebar.number_input("Banda del raster (1 = 2020, 2 = 2021...)", min_value=1, value=1)
k = st.sidebar.slider("Número de distritos en el ranking", 5, 30, 15)

uploaded_file = st.sidebar.file_uploader("Sube el raster Tmin (.tif)", type=["tif", "tiff"])

if uploaded_file is not None:
    import rasterio
    from tempfile import NamedTemporaryFile
    tmp = NamedTemporaryFile(delete=False, suffix=".tif")
    tmp.write(uploaded_file.read())
    tmp.close()
    raster_path = tmp.name
else:
    st.warning("⚠️ No se subió un raster. Descárgalo desde el link de Google Drive y súbelo aquí.")
    st.stop()

# --- Cargar shapes y calcular zonal stats
gdf = load_admin_level(level)
res = compute_band_stats(gdf, tif_name=raster_path, band=band)

st.title("🧊 Perú Tmin — Estadísticas Zonales & Políticas Públicas")

# --- KPIs en header
col1, col2, col3 = st.columns(3)
col1.metric("📉 Distrito más frío", res.loc[res['mean'].idxmin(), 'NAME'], f"{res['mean'].min():.1f} °C")
col2.metric("📈 Distrito más cálido", res.loc[res['mean'].idxmax(), 'NAME'], f"{res['mean'].max():.1f} °C")
col3.metric("📊 Promedio nacional", f"{res['mean'].mean():.1f} °C")

st.markdown("---")

# --- Tabs para secciones
tab1, tab2, tab3 = st.tabs(["📊 Distribución", "🏅 Ranking", "🗺️ Mapa"])

with tab1:
    st.subheader("Distribución de Tmin promedio")
    fig_dist = plot_distribution(res, col="mean")
    st.pyplot(fig_dist)
    st.markdown(
        f"📌 **Conclusión**: La temperatura mínima promedio en {level} "
        f"está centrada en {res['mean'].median():.1f} °C, "
        f"con valores extremos que bajan hasta {res['mean'].min():.1f} °C."
    )

with tab2:
    st.subheader(f"Top {k} territorios más fríos y más cálidos")
    topk, botk = top_bottom_ranking(res, col="mean", k=k)
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Más fríos**")
        st.dataframe(topk[["UBIGEO", "NAME", "mean"]])
    with col2:
        st.write("**Más cálidos**")
        st.dataframe(botk[["UBIGEO", "NAME", "mean"]])
    st.markdown(
        f"📌 **Conclusión**: El distrito más frío es **{res.loc[res['mean'].idxmin(), 'NAME']}** "
        f"({res['mean'].min():.1f} °C), mientras que el más cálido es "
        f"**{res.loc[res['mean'].idxmax(), 'NAME']}** ({res['mean'].max():.1f} °C)."
    )

with tab3:
    st.subheader("Mapa estático — Riesgo de helada")
    fig_map = plot_choropleth(res, col="cold_margin", title="Riesgo de helada (p10 vs 0°C)")
    st.pyplot(fig_map)
    st.markdown(
        f"📌 **Conclusión**: El mapa muestra que las zonas altoandinas concentran los riesgos "
        f"mayores (p10 < 0°C), mientras que la Amazonía tiene valores más templados."
    )

st.markdown("---")

# --- Descargar resultados
st.subheader("⬇️ Descargar resultados")
st.download_button(
    "Descargar CSV",
    data=res.to_csv(index=False),
    file_name=f"zonal_tmin_band{band}_{level}.csv",
    mime="text/csv",
)

st.header("🧭 Propuestas de política pública (borrador)")
st.markdown("""
- **Medida 1:** Vivienda térmica (ISUR).  
- **Medida 2:** Kits anti-helada para pequeños productores.  
- **Medida 3:** Calendario agro + alertas tempranas.
""")

