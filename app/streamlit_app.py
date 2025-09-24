import streamlit as st
import sys
from pathlib import Path

# Agregar carpeta raíz al path para encontrar /scripts
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from scripts.data_prep import load_admin_level
from scripts.zonal_stats import compute_band_stats
from scripts.plotting import plot_distribution, top_bottom_ranking, plot_choropleth

st.set_page_config(page_title="Perú Tmin – Zonal Stats", layout="wide")

st.title("Perú Tmin – Zonal Statistics & Public Policy")


st.markdown("""
Explora estadísticas de temperatura mínima (Tmin) a nivel distrital, provincial o departamental, 
y conecta los resultados con propuestas de política pública.
""")

# --- Sidebar
level = st.sidebar.selectbox("Nivel territorial", ["district", "province", "department"])
band = st.sidebar.number_input("Banda del raster (1 = 2020, 2 = 2021, ...)", min_value=1, value=1)

# --- Cargar shapes
gdf = load_admin_level(level)

# --- Calcular estadísticas zonales
try:
    res = compute_band_stats(gdf, tif_name="tmin_peru.tif", band=band)
except FileNotFoundError:
    st.error("No se encontró el archivo raster en /data/raster/")
    st.stop()

st.subheader("Resultados (tabla)")
st.dataframe(
    res[["UBIGEO", "NAME", "mean", "min", "max", "std", "percentile_10", "percentile_90", "cold_margin"]]
    .sort_values("mean")
)

# --- Descargar resultados
st.download_button(
    "⬇️ Descargar CSV",
    data=res.to_csv(index=False),
    file_name=f"zonal_tmin_band{band}_{level}.csv",
    mime="text/csv",
)

# --- Distribución
st.subheader("Distribución de temperaturas promedio")
fig_dist = plot_distribution(res, col="mean")
st.pyplot(fig_dist)

# --- Ranking
st.subheader("Ranking de territorios")
topk, botk = top_bottom_ranking(res, col="mean", k=15)
col1, col2 = st.columns(2)
with col1:
    st.write("**Más fríos**")
    st.dataframe(topk[["UBIGEO", "NAME", "mean"]])
with col2:
    st.write("**Más cálidos**")
    st.dataframe(botk[["UBIGEO", "NAME", "mean"]])

# --- Mapa estático
st.subheader("Mapa estático")
fig_map = plot_choropleth(res, col="cold_margin")
st.pyplot(fig_map)

# --- Política pública
st.header("🧭 Propuestas de política pública")
st.markdown("""
- **Medida 1:** Vivienda térmica (ISUR).  
- **Medida 2:** Kits anti-helada para pequeños productores.  
- **Medida 3:** Calendario agro + alertas tempranas.
""")

